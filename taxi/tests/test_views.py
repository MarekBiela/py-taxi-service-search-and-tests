from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_creation_user(self):
        self.assertEqual(self.user.username, "user1")

    def test_validation_password(self):
        self.assertTrue(self.user.check_password("test123"))


class ManufacturerListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="test123",
        )
        Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="Honda")
        self.client.force_login(self.user)

    def test_search_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Audi"}
        )

        self.assertContains(response, "Audi")
        self.assertNotContains(response, "Toyota")
        self.assertNotContains(response, "Honda")


class DriverListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="test123",
        )
        Driver.objects.create(
            username="user5",
            license_number="ABC12345"
        )
        Driver.objects.create(
            username="user6",
            license_number="ABC12346"
        )
        Driver.objects.create(
            username="user7",
            license_number="ABC12347"
        )
        self.client.force_login(self.user)

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "user5"}
        )

        self.assertContains(response, "user5")
        self.assertNotContains(response, "user6")
        self.assertNotContains(response, "user7")


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="test123",
        )
        manufacturer = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(model="Corolla", manufacturer=manufacturer)
        Car.objects.create(model="RAV4", manufacturer=manufacturer)
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.client.force_login(self.user)

    def test_search_car(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Corolla"}
        )

        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "RAV4")
        self.assertNotContains(response, "Camry")
