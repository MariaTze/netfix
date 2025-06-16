from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.CharField(max_length=100, unique=True)

User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="customer_profile",
    )
    # date of birth
    birth = models.DateField(verbose_name="Date of Birth")
    avatar_index = models.CharField(
        max_length= 2,
        default= '1',
        choices=[(str(i), f"Avatar {i}") for i in "123456789ABCDEFGHIJK"]
    )

    def __str__(self):
        return f"{self.user.username} (Customer)"


class Company(models.Model):
    FIELD_CHOICES = [
        ("Air Conditioner", "Air Conditioner"),
        ("All in One",      "All in One"),
        ("Carpentry",       "Carpentry"),
        ("Electricity",     "Electricity"),
        ("Gardening",       "Gardening"),
        ("Home Machines",   "Home Machines"),
        ("Housekeeping",    "Housekeeping"),
        ("Interior Design", "Interior Design"),
        ("Locks",           "Locks"),
        ("Painting",        "Painting"),
        ("Plumbing",        "Plumbing"),
        ("Water Heaters",   "Water Heaters"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="company_profile"
    )
    field_of_work = models.CharField(
        max_length=30,
        choices=FIELD_CHOICES,
        default="All in One",
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
    )
    avatar_index = models.CharField(
        max_length=2,
        default='1',
        choices=[(str(i), f"Avatar {i}") for i in "123456789ABCDEFGHIJK"]
    )

    def __str__(self):
        return f"{self.user.username} ({self.field_of_work})"
