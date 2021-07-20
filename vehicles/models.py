from django.db import models

# Create your models here.


class Regveh(models.Model):
    vn = models.CharField(
        max_length=20, verbose_name="Vehicle Number", primary_key=True)
    name = models.CharField(max_length=20, verbose_name="Owner Name")
    post = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Registered Vehicle"
        verbose_name_plural = "Registered Vehicles"

    def __str__(self):
        return self.vn


class Gesveh(models.Model):
    vn = models.CharField(max_length=20, verbose_name="Vehicle Number")
    name = models.CharField(max_length=20, verbose_name="Entrant Name")
    contact = models.CharField(max_length=20, verbose_name="Entrant Contact")
    nod = models.IntegerField(verbose_name="Permission Time", default=1)
    firstentry = models.DateTimeField(
        auto_now_add=True, verbose_name="First Entry time")

    class Meta:
        verbose_name = "Guest Vehicle"
        verbose_name_plural = "Guest Vehicles"

    def __str__(self):
        return self.vn


class Flow(models.Model):
    vn = models.CharField(max_length=20, verbose_name="Vehicle Number")
    timein = models.DateTimeField(auto_now_add=True)
    timeout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.vn
