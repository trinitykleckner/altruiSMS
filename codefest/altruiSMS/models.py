from django.db import models

# Create your models here.
class Beneficiary(models.Model):
    phone_num = models.CharField(primary_key=True, max_length=12)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.phone_num)