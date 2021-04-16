"""
logic controller
"""
import django_filters.rest_framework
from rest_framework import status

from accounts.models import MyUser, UserBed, Bed
from accounts.serializers.serializers import (
    AdmitPatientSerializer, PatientBedsSerializer, ReleasePatientSerializer, BedSerializer, BedDetailsSerializer
)
from common.messages import SUCCESS_CODE
from common.viewsets import CustomModelViewSet, custom_response, custom_error_response


class Patient(CustomModelViewSet):
    """
    method to check of analysis is calculated or not
    """
    http_method_names = ("get", )
    model = MyUser
    serializer_class = PatientBedsSerializer

    def get_queryset(self):
        """
        method to get patients queryset
        """
        bed_type = self.request.query_params.get("bed_type")
        queryset = UserBed.objects.filter(is_active=True)
        if bed_type:
            queryset = queryset.filter(bed__bed_type=bed_type)
        return queryset


class AdmitPatient(CustomModelViewSet):
    """
    method to check of analysis is calculated or not
    """
    http_method_names = ("post", "get", )
    model = MyUser
    serializer_class = AdmitPatientSerializer

    def get_queryset(self):
        """
        method to get patients queryset
        """
        queryset = UserBed.objects.filter(is_active=True)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        method to get list of patients
        """
        queryset = self.get_queryset()
        serialized_data = PatientBedsSerializer(queryset, many=True)
        return custom_response(status=status.HTTP_200_OK, data=serialized_data, detail="")

    def create(self, request, *args, **kwargs):
        """
        method for eom dashboard listing
        :param request: request object
        :param args: args
        :param kwargs: kwargs
        :return: list
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                status=status.HTTP_200_OK,
                data="",
                detail=SUCCESS_CODE["1001"].format(serializer.instance.bed_number)
            )
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=list(serializer.errors.values())[0][0])


class ReleasePatient(CustomModelViewSet):
    """
    method to check of analysis is calculated or not
    """
    http_method_names = ("post", "get", )
    model = MyUser
    serializer_class = ReleasePatientSerializer

    def create(self, request, *args, **kwargs):
        """
        method for eom dashboard listing
        :param request: request object
        :param args: args
        :param kwargs: kwargs
        :return: list
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(status=status.HTTP_200_OK, data={}, detail=SUCCESS_CODE["1002"])
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=list(serializer.errors.values())[0][0])


class BedStatusViewSet(CustomModelViewSet):
    """
    method to check of analysis is calculated or not
    """
    http_method_names = ("get", )
    model = Bed
    serializer_class = BedDetailsSerializer

    def get_queryset(self):
        """
        method to get patients queryset
        """
        bed_number = self.request.query_params.get("bed_number")
        queryset = Bed.objects.active_beds()
        if bed_number:
            queryset = queryset.filter(bed_number=bed_number)
        return queryset


class BedAvailability(CustomModelViewSet):
    """
    method to check of analysis is calculated or not
    """
    http_method_names = ("get", )
    model = Bed
    serializer_class = BedSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['bed_number', "bed_type"]

    def get_queryset(self):
        """
        method to get patients queryset
        """
        queryset = self.filter_queryset(Bed.objects.active_beds())
        return queryset
