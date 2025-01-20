from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    TOWN_CHOICES = [
        ('Nairobi', 'Nairobi'),
        ('Mombasa', 'Mombasa'),
        ('Kisumu', 'Kisumu'),
        ('Nakuru', 'Nakuru'),
        ('Eldoret', 'Eldoret'),
        ('Thika', 'Thika'),
        ('Nyeri', 'Nyeri'),
        ('Machakos', 'Machakos'),
        ('Naivasha', 'Naivasha'),
        ('Meru', 'Meru'),
        ('Kakamega', 'Kakamega'),
        ('Embu', 'Embu'),
        ('Kericho', 'Kericho'),
        ('Malindi', 'Malindi'),
        ('Kitale', 'Kitale'),
        ('Garissa', 'Garissa'),
        ('Nanyuki', 'Nanyuki'),
        ('Isiolo', 'Isiolo'),
        ('Lamu', 'Lamu'),
        ('Wajir', 'Wajir'),
        ('Narok', 'Narok'),
        ('Kilifi', 'Kilifi'),
        ('Bungoma', 'Bungoma'),
        ('Voi', 'Voi'),
        ('Homa Bay', 'Homa Bay'),
        ('Marsabit', 'Marsabit'),
        ('Moyale', 'Moyale'),
        ('Mandera', 'Mandera'),
        ('Lodwar', 'Lodwar'),
        ('Bomet', 'Bomet'),
        ('Busia', 'Busia'),
        ('Siaya', 'Siaya'),
        ('Migori', 'Migori'),
        ('Makueni', 'Makueni'),
        ('Taveta', 'Taveta'),
        ('Nyahururu', 'Nyahururu'),
        ('Sotik', 'Sotik'),
        ('Kapenguria', 'Kapenguria'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    zipcode = models.IntegerField(blank=True, default=0)
    town = models.CharField(max_length=100, choices=TOWN_CHOICES, blank=True)
    old_cart = models.TextField(max_length=5000, blank=True)

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        new_profile = Profile(user=instance)
        new_profile.save()