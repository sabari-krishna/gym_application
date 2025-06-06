import pytest
from django.urls import reverse
from api.models import FitnessClass, Booking, User
from django.utils import timezone
import pytz


@pytest.fixture
def fitness_class():
    return FitnessClass.objects.create(
        name="Evening Pilates",
        instructor="Anjali",
        datetime_ist=timezone.now(),
        available_slots=2
    )


@pytest.mark.django_db
def test_successful_booking(client, fitness_class):
    url = reverse("book-class")
    email = "sabari@example.com"

    response = client.post(url, {
        "class_id": str(fitness_class.id),
        "email": email,
        "client_name":"sabari"
    })

    assert response.status_code == 201
    assert Booking.objects.count() == 1
    assert User.objects.count() == 1
    assert FitnessClass.objects.get(id=fitness_class.id).available_slots == 1


@pytest.mark.django_db
def test_prevent_double_booking(client, fitness_class):
    url = reverse("book-class")
    email = "sabari@example.com"

    client.post(url, {
        "class_id": str(fitness_class.id),
        "email": email,
        "client_name":"sabari"
    })
    response = client.post(url, {
        "class_id": str(fitness_class.id),
        "email": email,
        "client_name":"sabari"
    })
    assert response.status_code == 400
    assert "already booked" in response.json()["non_field_errors"][0]
    assert Booking.objects.count() == 1


@pytest.mark.django_db
def test_slot_full(client, fitness_class):
    url = reverse("book-class")

    client.post(url, {
        "class_id": str(fitness_class.id),
        "email": "a@example.com",
        "client_name":"sabari1"
    })
    client.post(url, {
        "class_id": str(fitness_class.id),
        "email": "b@example.com",
        "client_name":"sabari2"
    })
    response = client.post(url, {
        "class_id": str(fitness_class.id),
        "email": "c@example.com",
        "client_name":"sabari3"
    })

    assert response.status_code == 400
    assert "Slot is full" in response.json()["non_field_errors"][0]
    assert Booking.objects.count() == 2
