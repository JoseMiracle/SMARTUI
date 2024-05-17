from django.db import models
from django.contrib.auth import get_user_model
from smartui.utils.base_class import BaseModel

User = get_user_model()
# Create your models here.

def medical_files_upload_location(instance, filename: str) -> str:
    """Get Location for user profile photo upload."""
    return f"medicals/files/{filename}"


class MedicalRecords(BaseModel):
    """
    Represents the medical records associated with a user within the system.

    Attributes:
        user (ForeignKey): Reference to the User who owns these medical records. Restricted deletion.
        medical_report_file (FileField): An optional field to upload medical report files.
        to_be_reviewed_by (ForeignKey): Designates which User needs to review these medical records. Cannot be null.
        reviewed_by (ForeignKey): Reference to the User who reviewed the medical records. Can be null initially.
        message (CharField): Optional notes or messages associated with the medical record review.
        reviewed (BooleanField): Status flag indicating whether the medical records have been reviewed.
        user_consent_for_external_provider (BooleanField): Flag to indicate user's consent for sharing records with external providers.
        doctor_consent_for_external_provider (BooleanField): Flag to indicate doctor's consent for sharing records with external providers.
    """

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
    """
    Represents an appointment scheduled in the system.

    Attributes:
        patient (ForeignKey): Reference to the User who is the patient for this appointment. Deletes cascade.
        staff (ForeignKey): Reference to the User from the staff who will attend to the appointment. Restricted on delete.
        location (TextField): The location where the appointment is scheduled to take place.
        duration (CharField): The duration of the appointment in minutes or a descriptive format.
        status (CharField): The current status of the appointment (scheduled, cancelled, completed).
        date (DateField): The scheduled date of the appointment.
        time (TimeField): The scheduled time of the appointment.
        notes (TextField): Optional detailed notes or remarks about the appointment.
    """

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
    




    
