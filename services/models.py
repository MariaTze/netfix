from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Company, Customer
from django.conf import settings
from django.db.models import Avg

class Service(models.Model):
    FIELD_CHOICES = (
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('Housekeeping', 'Housekeeping'),  # Fixed spelling!
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_per_hour = models.DecimalField(decimal_places=2, max_digits=6)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    field = models.CharField(max_length=30, choices=FIELD_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def avg_rating(self):
        return self.requests.aggregate(Avg('rating'))['rating__avg']

class ServiceRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE , related_name = 'requests')
    address = models.CharField(max_length=255)
    hours = models.PositiveIntegerField()
    requested_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.user.username} requests {self.service.name} @ {self.requested_at:%Y-%m-%d %H:%M}"
