""""
accounts serializer
"""
from django.db import transaction
from rest_framework import serializers

from accounts.constants import TOTAL_BEDS
from accounts.helper import get_bed
from accounts.models import MyUser, Bed, UserBed
from common.messages import ERROR_CODE


class AdmitPatientSerializer(serializers.ModelSerializer):
    """
    serializer class fr eom lc
    """
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=100, required=True)
    bed_type = serializers.IntegerField(required=False, min_value=1, max_value=3, error_messages={
        "invalid": ERROR_CODE["2004"],
        'max_value': ERROR_CODE["2004"],
        'min_value': ERROR_CODE["2004"],
    })

    class Meta:
        """
        serializer meta class
        """
        model = MyUser
        fields = ("email", "name", "bed_type", )

    def validate(self, attrs):
        """
        validate request data
        """
        if MyUser.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"detail": ERROR_CODE["2000"]})

        if "bed_type" in attrs and not (
                Bed.objects.filter(bed_type=attrs["bed_type"], is_active=True, is_available=True).exists()):
            raise serializers.ValidationError({"detail": ERROR_CODE["2001"]})

        return attrs

    def create(self, validated_data):
        """
        method to create or update eom lc
        :param validated_data:
        :return:
        """
        bed_type = validated_data.get("bed_type", None)
        with transaction.atomic():
            user = MyUser.objects.create(first_name=validated_data["name"], email=validated_data["email"])
            bed = get_bed(bed_type=bed_type)
            UserBed.objects.create(
                user=user,
                bed=bed
            )
            bed.is_available = False
            bed.save()
            return bed


class BedSerializer(serializers.ModelSerializer):
    """
    serializer class fr eom lc
    """

    class Meta:
        """
        serializer meta class
        """
        model = Bed
        fields = ("bed_number", "bed_type", "is_available", )


class PatientSerializer(serializers.ModelSerializer):
    """
    serializer class fr eom lc
    """

    class Meta:
        """
        serializer meta class
        """
        model = MyUser
        fields = ("id", "first_name", "email", )


class PatientBedsSerializer(serializers.ModelSerializer):
    """
    serializer class fr eom lc
    """
    user = PatientSerializer()
    bed = BedSerializer()

    class Meta:
        """
        serializer meta class
        """
        model = UserBed
        fields = ("user", "bed", )


class ReleasePatientSerializer(serializers.ModelSerializer):
    """
    serializer class fr eom lc
    """
    bed_number = serializers.IntegerField(
        required=True, error_messages={
            "invalid": "Please enter correct bed number"
        }, min_value=0, max_value=TOTAL_BEDS
    )

    def validate(self, attrs):
        """
        Method to validate request data
        """
        if Bed.objects.active_beds().filter(bed_number=attrs["bed_number"], is_available=True).exists():
            raise serializers.ValidationError({"detail": ERROR_CODE["2003"]})
        return attrs

    class Meta:
        """
        serializer meta class
        """
        model = UserBed
        fields = ("bed_number", )

    def create(self, validated_data):
        """
        method to create or update eom lc
        :param validated_data:
        :return:
        """
        bed_number = validated_data["bed_number"]
        UserBed.objects.filter(bed__bed_number=bed_number).update(is_active=False)
        Bed.objects.active_beds().filter(bed_number=bed_number).update(is_available=True)

        return bed_number


class BedDetailsSerializer(serializers.ModelSerializer):
    """
    serializer class fr eom lc
    """
    patient = serializers.SerializerMethodField()

    @staticmethod
    def get_patient(obj):
        """
        method to get patient details
        """
        patient = None
        if obj.bed_patient.exists():
            patient = PatientSerializer(obj.bed_patient.last().user).data
        return patient

    class Meta:
        """
        serializer meta class
        """
        model = Bed
        fields = ("bed_number", "bed_type", "is_available", "is_active", "patient", )
