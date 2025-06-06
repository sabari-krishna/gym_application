from rest_framework import generics, status
from rest_framework.response import Response
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingCreateSerializer, BookingDisplaySerializer
from .logger import create_logger

logger = create_logger(__name__)

class TimezoneContext:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['timezone'] = self.request.query_params.get('timezone', 'Asia/Kolkata')
        return context

#view class for listing the fitness classes
class FitnessClassListView(TimezoneContext, generics.ListAPIView):
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        logger.info("List fitness class view")
        return FitnessClass.objects.all().order_by('datetime_ist')

#view class for booking a fitness class
class BookClassView(generics.CreateAPIView,TimezoneContext):
    serializer_class = BookingCreateSerializer

    def create(self, request):
        logger.info("start of Booking Fitness class view")
        serializer = self.get_serializer(data=request.data)
        print(str(serializer))
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        display_serializer = BookingDisplaySerializer(booking)
        return Response(display_serializer.data, status=status.HTTP_201_CREATED)

#view class to list the booked class
class BookingListView(TimezoneContext, generics.ListAPIView):
    serializer_class = BookingDisplaySerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email:
            return Booking.objects.filter(user__email=email)
        return Booking.objects.none()