from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

# Create your models here.
class Aadhar(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, related_name='aadhar_user',null = True, blank = True)
    aadhar_number   = models.CharField(max_length = 100,primary_key=True)
    active          = models.BooleanField(default=False)

    def __str__(self):
        return self.aadhar_number

    class Meta:
        ordering = ['aadhar_number']
        verbose_name_plural = "Aadhar"

class Address(models.Model):
    user            = models.ForeignKey(Aadhar,on_delete = models.CASCADE, related_name='address_user',null = True, blank = True)
    street          = models.CharField(max_length = 100)
    city            = models.CharField(max_length = 100)
    state           = models.CharField(max_length = 100)
    pincode         = models.CharField(max_length = 100)

    def __str__(self):
        return self.user.aadhar_number + " address"

    class Meta:
        verbose_name_plural = "Address"



class Qualification(models.Model):
    user            = models.ForeignKey(Aadhar,on_delete = models.CASCADE, related_name='qualification_user',null = True, blank = True)
    name_of_college = models.CharField(max_length = 100)
    year_of_passing = models.PositiveIntegerField()
    percentage      = models.DecimalField(max_digits = 7, decimal_places = 2)

    def __str__(self):
        return self.user.aadhar_number + " qualification"

    class Meta:
        ordering = ['year_of_passing']

class Bank(models.Model):
    user            = models.ForeignKey(Aadhar,on_delete = models.CASCADE, related_name='bank_user',null = True, blank = True)
    account_no      = models.CharField(max_length = 100)
    bank_name       = models.CharField(max_length = 100)
    IFSC_code       = models.CharField(max_length = 100)

    def __str__(self):
        return self.user.aadhar_number + " bank"

    class Meta:
        ordering = ['bank_name']

class PersonalDetails(models.Model):
    user            = models.ForeignKey(Aadhar,on_delete = models.CASCADE, related_name='personal_details_user',null = True, blank = True)
    email           = models.CharField(max_length = 100)
    contact         = models.CharField(max_length = 100)

    def __str__(self):
        return self.user.aadhar_number + " Personal Details"

    class Meta:
        verbose_name_plural = "Personal Details"

class PastJobExperience(models.Model):
    user            = models.ForeignKey(Aadhar,on_delete = models.CASCADE, related_name='past_job_experience_user',null = True, blank = True)
    company_name    = models.CharField(max_length = 100)
    job_role        = models.CharField(max_length = 100)
    year_experience = models.DecimalField(max_digits = 7, decimal_places = 2)

    def __str__(self):
        return self.user.aadhar_number + " PastJobExperience"

    class Meta:
        ordering = ['year_experience']
        verbose_name_plural = "Past Job Experience"