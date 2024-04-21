from django.urls import path
from smartui.medicals.api.v1.views import (
    DoctorsAPIView,
    UserMedicalRecordAPIView,
    MedicalRecordsAPIView,
    ReviewMedicalRecord,
    MedicalRecordsToBeReviewedByDoctorAPIVIew,
    ExternalProviderAPIView,
    ExternalProviderStaffAPIView,
    UserConsentMedicalRecordForExternalProviderAPIView,
    CreateExternalProvidersMedicalFileAccessAPIView,
    AppointmentAPIView,
    ModifyAppointMentAPIView,
    PatientAppointmentAPIView,
    StaffAppointmentAPIView,
)

app_name = "medicals"

urlpatterns = [
    
    path('doctor/', DoctorsAPIView.as_view(), name='doctor'),
    path('user-medical-record/', UserMedicalRecordAPIView.as_view(), name='user_medical_record'),
    path('medical-records/<str:username>/', MedicalRecordsAPIView.as_view(), name='medical_record'), # For doctors
    path('review-user-medical-records/<uuid:id>/', ReviewMedicalRecord.as_view(), name='review_medical_record'),
    path('medical-reports-to-be-reviewed/', MedicalRecordsToBeReviewedByDoctorAPIVIew.as_view(), name='medical_reports_to_be_reviewed'),
    path('external-provider/', ExternalProviderAPIView.as_view(), name='external_provider'),
    path('external-provider-staff/', ExternalProviderStaffAPIView.as_view(), name='external_provider_staff'),
    path('user-consent-medical-record-for-external-provider/<uuid:medical_record_id>/', UserConsentMedicalRecordForExternalProviderAPIView.as_view(), 
         name='user_consent_medical_record_for_external_provider'),

    path('external-provider-medical-file-access/', 
         CreateExternalProvidersMedicalFileAccessAPIView.as_view(),
         name='external_providers_medical_file_access'
         ),

    path('appointment/', AppointmentAPIView.as_view(), name='appointment'),
    path('modify-appointment/<uuid:appointment_id>/', ModifyAppointMentAPIView.as_view(), name='modify-appointment'),
    path('patient-appointments/', PatientAppointmentAPIView.as_view(), name='patient_appointments'),
    path('staff-appointments/', StaffAppointmentAPIView.as_view(), name='staff_appointments')
    
]
