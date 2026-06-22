from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

COUNTIES = [('Nairobi', 'Nairobi'),
            ('Kiambu', 'Kiambu'),
            ('Nakuru', 'Nakuru'),
            ('Mombasa', 'Mombasa'),
            ('Meru', 'Meru'),
            ('Nyeri', 'Nyeri'),
            ('Eldoret', 'Uasin Gishu'),
            ('Kakamega', 'Kakamega'),
            ('Nyeri', 'Nyeri'),
            ('Bungoma', 'Bungoma'),
            ('Migori', 'Migori'),
            ('Kisii', 'Kisii')

    ]

class Property(models.Model):
    """Model for rental properties/houses"""

    # House Details
    title = models.CharField(max_length=200, verbose_name="Tittle")
    description = models.TextField(verbose_name="Description")


    # Location (Kenya specific)
    county = models.CharField(max_length=100, verbose_name="County")
    town = models.CharField(max_length=100, verbose_name="Town")
    location = models.CharField(max_length=300, verbose_name="Exact location")

    # Property Specs
    bedrooms = models.IntegerField(verbose_name="Bedrooms")
    bathrooms = models.IntegerField(verbose_name="Bathrooms")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Rent per Month (Ksh)")

    #Status
    is_available = models.BooleanField(default=True, verbose_name="Available?")

    # Owner/Who posted it
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    image = models.ImageField(upload_to='properties/', blank=True, null=True, verbose_name="House Photo")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} - {self.town} ({self.county})"

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")

    def __str__(self):
        return f"{self.user.username}'s Profile"
