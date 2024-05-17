from rest_framework import generics, permissions, status
from smartui.medicals.api.v1.serializers import (
    UserMedicalRecordSerializer,
    MedicalRecordsSerializer,
    ReviewMedicalRecordSerializer,
    MedicalRecordsToBeReviewedByDoctorSerializer,
    ExternalProviderSerializer,
    ExternalProviderStaffSerializer,
    UserConsentMedicalRecordForExternalProviderSerializer,
    DoctorConsentMedicalRecordForExternalProviderSerializer,
    CreateExternalProvidersMedicalFileAccessSerializer,
    AppointmentSerializer,
    ModifyAppointmentSerializer,
    StaffAppointmentSerializer
)
from smartui.medicals.api.v1.permissions import (
    IsDoctor, 
    IsAdmin,
    IsDoctorOrExternalProvider
)
from smartui.accounts.api.v1.serializers import(
    ProfileSerializer
)
from smartui.medicals.models import (
MedicalRecords, 
ExternalProviders,
MedicalRecordForExternalProvider,
Appointment
)
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.response import Response

User = get_user_model()


class DoctorsAPIView(generics.ListAPIView):
    """This is for retrieving doctors on SMARTUI platform"""

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        doctors_queryset = User.objects.filter(role='doctor').all()
        return doctors_queryset

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class UserMedicalRecordAPIView(generics.ListCreateAPIView):
    """This allows users to upload there medical records and also retrieve there medical records"""

    serializer_class = UserMedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_medical_records = MedicalRecords.objects.filter(user=self.request.user).all()
        return user_medical_records
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MedicalRecordsAPIView(generics.ListAPIView):
    """This is for doctors to view user's medical records"""
    
    serializer_class = MedicalRecordsSerializer    
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs['username']).first()
        medical_records = MedicalRecords.objects.filter(user=user).order_by('-created_at')
        return medical_records

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class ReviewMedicalRecord(generics.RetrieveUpdateAPIView):
    """This allows doctors to review user records"""

    serializer_class = ReviewMedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_object(self):
        medical_record = MedicalRecords.objects.filter(
            id=self.kwargs['id']
            ).first()
        return medical_record
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class MedicalRecordsToBeReviewedByDoctorAPIVIew(generics.ListAPIView):

    serializer_class = MedicalRecordsToBeReviewedByDoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    
    def get_queryset(self):
        medical_reports_to_be_reviewed_by_doctor = MedicalRecords.objects.filter(
            to_be_reviewed_by=self.request.user
            )
        return medical_reports_to_be_reviewed_by_doctor

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExternalProviderAPIView(generics.ListCreateAPIView):
    """This allows Admins to add external providers to the SMARTUI"""

    serializer_class = ExternalProviderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]  
    queryset = ExternalProviders.objects.all()

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExternalProviderStaffAPIView(generics.ListCreateAPIView):    
    serializer_class = ExternalProviderStaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin] 

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserConsentMedicalRecordForExternalProviderAPIView(generics.RetrieveUpdateAPIView):
    """This is for user to consent there records for external providers"""
    
    serializer_class =  UserConsentMedicalRecordForExternalProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        medical_record = MedicalRecords.objects.filter(
            id=self.kwargs['medical_record_id'],
            user = self.request.user # user is the patient
            ).first()
        
        return medical_record
        
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class DoctorConsentRecordForExternalProviderAPIView(generics.RetrieveUpdateAPIView):
    """This is for Doctor's to consent user's record to be viewed by external provider"""

    serializer_class = DoctorConsentMedicalRecordForExternalProviderSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]


    def get_object(self):
        medical_record = MedicalRecords.objects.filter(
            id=self.kwargs['medical_record_id'],
            reviewed_by=self.request.user
        )

        return medical_record
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class CreateExternalProvidersMedicalFileAccessAPIView(generics.CreateAPIView):
    serializer_class = CreateExternalProvidersMedicalFileAccessSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class AppointmentAPIView(generics.CreateAPIView):
    """This allows Doctors to create appointment with patients"""

    serializer_class = AppointmentSerializer 
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrExternalProvider]
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ModifyAppointMentAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ModifyAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrExternalProvider]


    def get_object(self):
        appointment_obj = Appointment.objects.filter(id=self.kwargs['appointment_id']).first()
        return appointment_obj

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    

class PatientAppointmentAPIView(generics.ListAPIView):
    """This allows patients know the appointments they have to attend to"""

    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_appointments = Appointment.objects.filter(patient=self.request.user)
        return patient_appointments
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class StaffAppointmentAPIView(generics.ListAPIView):
    serializer_class = StaffAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrExternalProvider]

    def get_queryset(self):
        staff_appointments = Appointment.objects.filter(staff=self.request.user)
        return staff_appointments
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
