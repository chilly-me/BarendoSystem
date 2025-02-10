import uuid

from django.contrib.auth.models import User
from django.db import models

from django.conf import settings
from django.utils import timezone

from store.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_DATE_CHOICES = [
        ('now', 'Pay now'),
        ('on_delivery', 'Pay upon delivery'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'Mpesa'),
        ('paypal', 'Paypal'),
        ('credit/debit', 'Credit/debit card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipped = models.BooleanField(null=True, blank=True, default=False )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    cancelled_date = models.DateTimeField(null=True, blank=True)
    receipt_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # New fields for payment
    payment_date = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)

    def update_status(self, new_status):
        if new_status in dict(self.STATUS_CHOICES):
            self.status = new_status
            # Automatically set the corresponding date field based on the new status
            if new_status == 'Shipped':
                self.shipped_date = timezone.now()
            elif new_status == 'Delivered':
                self.delivered_date = timezone.now()
            elif new_status == 'Cancelled':
                self.cancelled_date = timezone.now()
            # Save changes to the database
            self.save()
        else:
            raise ValueError("Invalid status")

    def update_total_cost(self, total_cost):
        self.total_price = total_cost
        self.save()

    def save(self, *args, **kwargs):
        # Populate phone, address, and town from the user's profile if they exist
        if not self.phone or not self.address or not self.town:
            profile = getattr(self.user, 'profile', None)
            if profile:
                self.phone = profile.phone
                self.address = profile.address
                self.town = profile.town
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
