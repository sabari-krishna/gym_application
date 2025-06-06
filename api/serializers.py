from rest_framework import serializers
from .models import FitnessClass, Booking, User
import pytz
from django.db import transaction
from .logger import create_logger


logger = create_logger(__name__)
# Util to format datetime based on tz
class Timezone:
    def get_datetime_with_timezone(self, dt_obj, context):
        tz_name = context.get('timezone', 'Asia/Kolkata')
        try:
            tz = pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            tz = pytz.timezone('Asia/Kolkata')
        return dt_obj.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')

#Serializer to list the fitness class
class FitnessClassSerializer(serializers.ModelSerializer, Timezone):
    datetime = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'instructor', 'datetime', 'available_slots']

    def get_datetime(self, obj):
        return self.get_datetime_with_timezone(obj.datetime_utc(), self.context)

#serializer to create the booking
class BookingCreateSerializer(serializers.ModelSerializer):
    class_id = serializers.UUIDField(write_only=True)
    email= serializers.EmailField()
    client_name = serializers.CharField()

    class Meta:
        model = Booking
        fields = ['class_id','email','client_name']
    #validating the input data
    def validate(self, data):
        logger.info("Validating book api call")
        email = data.get('email')
        class_id = data.get('class_id')
        client_name = data.get('client_name')
        if not email:
            logger.error(f"Email field is required - {email}")
            raise serializers.ValidationError("Email is required")

        logger.info("Fetching the user details")
        user,_ = User.objects.get_or_create(
        email=email, defaults={'username': client_name}
        )
        data['user'] = user
        logger.info(f"Fetching fitness class with ID: {class_id}")
        try:
            fitness_class = FitnessClass.objects.select_for_update().get(id=class_id)
            logger.info(f"Found fitness class: {fitness_class.name} with {fitness_class.available_slots} available slots")
        except FitnessClass.DoesNotExist:
            logger.error(f"Fitness class with ID {class_id} does not exist")
            raise serializers.ValidationError("Fitness class does not exist.")


        if Booking.objects.filter(fitness_class=fitness_class, user=user).exists():
            logger.info(f"User {email} already booked class {fitness_class.name}")
            raise serializers.ValidationError("User already booked this class.")

        if fitness_class.available_slots <= 0:
            logger.info(f"Class {fitness_class.name} is full (available slots: {fitness_class.available_slots})")
            raise serializers.ValidationError("Slot is full.")

        data['fitness_class'] = fitness_class
        logger.info("Validation completed successfully")
        return data
    # create the fitness class booking
    def create(self, validated_data):
        user = validated_data['user']
        fitness_class = validated_data['fitness_class']

        with transaction.atomic():
            logger.info("Entering atomic transaction for booking creation")

            fitness_class = FitnessClass.objects.select_for_update().get(id=fitness_class.id)
            logger.info(f"Re-fetched fitness class with {fitness_class.available_slots} available slots")
            if fitness_class.available_slots <= 0:
                logger.error(f"Slot became full during transaction for class {fitness_class.name}")
                raise serializers.ValidationError("Slot is full.")
            logger.info(f"Decreasing available slots from {fitness_class.available_slots} to {fitness_class.available_slots - 1}")
            fitness_class.available_slots -= 1
            fitness_class.save()
            logger.info("Fitness class slots updated successfully")
            logger.info(f"Booking created successfully")
            return Booking.objects.create(fitness_class=fitness_class, user=user)


#Serializer to display the class details after booking
class BookingDisplaySerializer(serializers.ModelSerializer, Timezone):
    class_name = serializers.CharField(source='fitness_class.name')
    instructor = serializers.CharField(source='fitness_class.instructor')
    datetime = serializers.SerializerMethodField()
    client_name = serializers.CharField(source='user.username')
    client_email = serializers.EmailField(source='user.email')

    class Meta:
        model = Booking
        fields = ['id', 'class_name', 'instructor', 'datetime', 'client_name', 'client_email', 'booked_at']

    def get_datetime(self, obj):
        logger.info(f"Getting formatted datetime for booking: {obj.id}")
        return self.get_datetime_with_timezone(obj.fitness_class.datetime_utc(), self.context)