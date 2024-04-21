from django.contrib.auth import get_user_model

from smartui.medicals.models import (
    MedicalRecords, 
    ExternalProviders,
    ExternalProviderStaff,
    MedicalRecordForExternalProvider,
    Appointment
)
from rest_framework import serializers

from smartui.accounts.api.v1.serializers import (
    ProfileSerializer,
)

User = get_user_model()

class UserMedicalRecordSerializer(serializers.ModelSerializer):
    reviewed = serializers.ReadOnlyField()
    reviewed_by = ProfileSerializer(read_only=True)

    class Meta:
        model = MedicalRecords
        fields = [
            'medical_report_file',
            'reviewed',
            'reviewed_by',
            'to_be_reviewed_by'   
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context['request'].user 
        return super().create(validated_data) 



class MedicalRecordsSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    
    class Meta:
        model = MedicalRecords    
        fields = [
            'id',
            'user',
            'medical_report_file',
            'reviewed',
        ]



class ReviewMedicalRecordSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    reviewed_by = ProfileSerializer(read_only=True)

    class Meta:
        model = MedicalRecords
        fields = [
            'user',
            'medical_report_file',
            'reviewed',
            'message',
            'reviewed_by'
        ]
    
    def update(self, instance, validated_data):
        validated_data['reviewed_by'] = self.context['request'].user
        return super().update(instance, validated_data)


class MedicalRecordsToBeReviewedByDoctorSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = MedicalRecords
        fields = [
            'user',
            'reviewed',
        ]


class ExternalProviderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    description = serializers.CharField(required=True)

    class Meta:
        model = ExternalProviders
        fields = ['id', 'provider_name', 'description']

    def create(self, validated_data):
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)
    

class ExternalProviderStaffSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)
    external_provider = serializers.UUIDField()
    message = serializers.ReadOnlyField()


    def validate(self, attrs):
        staff = User.objects.filter(email=attrs['email']).first()
        external_staff_provider_obj = ExternalProviderStaff.objects.filter(
                external_provider_id = attrs['external_provider'],
                staff = staff
            )
        if external_staff_provider_obj.exists():
            raise serializers.ValidationError({
                "message": "staff linked with external provider already"
            })
        
        return super().validate(attrs)

    def create(self, validated_data):
        staff = User.objects.filter(email=validated_data['email']).first()
        external_provider = ExternalProviders.objects.filter(id=validated_data['external_provider']).first()
        
        
        if staff is not None:
            external_staff_provider = ExternalProviderStaff.objects.create(
                external_provider = external_provider,
                staff = staff
            )
            return {
                "email": validated_data['email'],
                "external_provider": external_provider.provider_name,
                "message" : "staff added"
            }
        
        else:
            raise serializers.ValidationError({
                "message": "staff doesn't exist"
            })

    
class UserConsentMedicalRecordForExternalProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalRecords
        fields = [
            'user_consent_for_external_provider',
        ]
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
class DoctorConsentMedicalRecordForExternalProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalRecords
        fields = [
            'doctor_consent_for_external_provider',
        ]
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class CreateExternalProvidersMedicalFileAccessSerializer(serializers.Serializer):
    external_provider = serializers.ListField(child=serializers.CharField())
    medical_record = serializers.UUIDField(required=True)
    message = serializers.ReadOnlyField()


    def validate(self, attrs):
        external_providers = attrs['external_provider']
        medical_record_id = attrs['medical_record']
        
        # Check if extener provider exist
        for external_provider_id in external_providers:
            if not ExternalProviders.objects.filter(id=external_provider_id).exists():
                raise serializers.ValidationError({
                    "message" : f"{external_provider_id} doesn't exist ." 
                })
        
        # Checks if file exists for external provider already
        for external_provider_id in external_providers:
            if MedicalRecordForExternalProvider.objects.filter(
                external_provider_id = external_provider_id,
                medical_record_id = medical_record_id
            ).exists():
                raise serializers.ValidationError({
                    "message": "File exists for external provider already"
                })
            
        if MedicalRecords.objects.filter(id=medical_record_id).first() is None:
            raise serializers.ValidationError({
                "message": f"{medical_record_id} doesn't exist ."
            })
        

            

        return super().validate(attrs)

    def create(self, validated_data):
        external_providers = validated_data.pop('external_provider')
        medical_record_id = validated_data["medical_record"]

        for external_provider in external_providers:
            print("error")
            MedicalRecordForExternalProvider.objects.create(
                external_provider_id = external_provider,
                medical_record_id = medical_record_id
            )

        return {
            "external_provider" : [external_provider],
            "medical_record": medical_record_id,
            "message" : "success"
        }
    

class AppointmentSerializer(serializers.ModelSerializer):
    
    notes = serializers.CharField(required=False)
    location = serializers.CharField(required=True)
    staff = ProfileSerializer(required=False)
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'staff',
            'location',
            'duration',
            'status',
            'date',
            'time',
            'notes'
        ]


    def create(self, validated_data):
        validated_data["staff"] = self.context['request'].user
        return super().create(validated_data)



class ModifyAppointmentSerializer(serializers.ModelSerializer):
    notes = serializers.CharField(required=False)
    
    class Meta:
        model = Appointment
        fields = [
            'status',
            'date',
            'time',
            'notes'
        ]


class StaffAppointmentSerializer(serializers.ModelSerializer):
    patient = ProfileSerializer()
    staff = ProfileSerializer()
    
    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'staff',
            'location',
            'duration',
            'status',
            'date',
            'time',
            'notes'
        ]
