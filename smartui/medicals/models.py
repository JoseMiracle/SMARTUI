from django.db import models
from django.contrib.auth import get_user_model
from smartui.utils.base_class import BaseModel

User = get_user_model()
# Create your models here.

def medical_files_upload_location(instance, filename: str) -> str:
    """Get Location for user profile photo upload."""
    return f"medicals/files/{filename}"


class MedicalRecords(BaseModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    medical_report_file = models.FileField(upload_to=medical_files_upload_location, blank=True)
    to_be_reviewed_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, blank=False, related_name='to_be_reviewed_by')
    reviewed_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name='reveiwed_by')
    message = models.CharField(max_length=250, blank=True, null=True)
    reviewed = models.BooleanField(default=False)
    user_consent_for_external_provider = models.BooleanField(default=False)
    doctor_consent_for_external_provider = models.BooleanField(default=False)
   

class ExternalProviders(BaseModel):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    location = models.TextField()
    description = models.TextField()

class ExternalProviderStaff(BaseModel):
    external_provider = models.ForeignKey(ExternalProviders, on_delete=models.CASCADE, related_name='external_providers')
    staff = models.ForeignKey(User, on_delete=models.CASCADE)


class MedicalRecordForExternalProvider(BaseModel):
    medical_record = models.ForeignKey(MedicalRecords, on_delete=models.CASCADE)
    external_provider = models.ForeignKey(ExternalProviders, on_delete=models.CASCADE)


class Appointment(BaseModel):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_appointment")
    staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="staff_appointment")
    location = models.TextField(blank=False, null=False)
    duration = models.CharField(max_length= 30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField()
    




    
