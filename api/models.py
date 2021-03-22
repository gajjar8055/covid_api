from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return '%s - (%s)' % (self.name, self.code)


class User(AbstractUser):
    """Using the AbstactUser class we will modify the User class to change consider email field as Username field."""

    username = None
    email = models.EmailField('email address', unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    # Here we define indexing that can improve performance while fetching data.
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['email'], name='email_idx'),
        ]


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
