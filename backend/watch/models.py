from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from watch.manager import UserManager
from watch.validators import check_phone


class User(AbstractBaseUser, PermissionsMixin):
    firstname = models.CharField('firstname', max_length=32, null=False, blank=False)
    lastname = models.CharField('lastname', max_length=32, null=False)
    phone = models.CharField('phone', max_length=11, validators=[check_phone], null=False, blank=False)
    email = models.EmailField('email', max_length=64, null=False, blank=False)
    birthday = models.DateField('birthday', null=False, blank=False, default=datetime.now)
    gender = models.BooleanField('gender', null=False)
    username = models.CharField('username', max_length=32, unique=True)
    watch_code = models.CharField('watch_code', max_length=16, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Contact(models.Model):
    user = models.ForeignKey("watch.User", on_delete=models.CASCADE, unique=True)
    contact_1 = models.CharField('contact_1', max_length=32, null=True)
    phone_1 = models.CharField('phone_1', max_length=11, validators=[check_phone], null=True)
    contact_2 = models.CharField('contact_2', max_length=32, null=True)
    phone_2 = models.CharField('phone_2', max_length=11, validators=[check_phone], null=True)
    contact_3 = models.CharField('contact_3', max_length=32, null=True)
    phone_3 = models.CharField('phone_3', max_length=11, validators=[check_phone], null=True)
    contact_4 = models.CharField('contact_4', max_length=32, null=True)
    phone_4 = models.CharField('phone_4', max_length=11, validators=[check_phone], null=True)
    contact_5 = models.CharField('contact_5', max_length=32, null=True)
    phone_5 = models.CharField('phone_5', max_length=11, validators=[check_phone], null=True)

    def __str__(self):
        return f"{self.user} contacts"


class Config(models.Model):
    key = models.CharField('key', max_length=32)
    value = models.CharField('value', max_length=32)

    def __str__(self):
        return self.key + " : " + self.value


class WatchCode(models.Model):
    code = models.CharField('code', max_length=16, unique=True)

    def __str__(self):
        return self.code


class AcceleratorData(models.Model):
    user = models.ForeignKey("watch.User", on_delete=models.CASCADE)
    event = models.SmallIntegerField('event')
    x = models.FloatField('x')
    y = models.FloatField('y')
    z = models.FloatField('z')
    situation = models.CharField(max_length=5, null=True)


class HeartRateData(models.Model):
    user = models.ForeignKey("watch.User", on_delete=models.CASCADE)
    heartrate = models.IntegerField('heart_rate')

    def __str__(self):
        return self.user.username + " , " + str(self.heartrate)


class GPSData(models.Model):
    user = models.ForeignKey("watch.User", on_delete=models.CASCADE)
    lat = models.FloatField("latitude")
    long = models.FloatField("longitude")

    def __str__(self):
        return self.user.username + " : " + str(self.lat) + " , " + str(self.long)