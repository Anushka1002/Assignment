"""
File is used to make urls for analysis
"""
# third party import
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# local import
from accounts.views.views import AdmitPatient, ReleasePatient, Patient, BedAvailability, BedStatusViewSet


class OptionalSlashRouter(DefaultRouter):
    """
    optional slash router class
    """
    def __init__(self):
        """
            explicitly appending '/' in urls if '/' doesn't exists for making common url patterns .
        """
        super(OptionalSlashRouter, self).__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
beds_router = OptionalSlashRouter()

# patient routes
router.register(r'^', Patient, basename='patient')
router.register(r'admit', AdmitPatient, basename='admit')
router.register(r'release', ReleasePatient, basename='release')

# bed routes
beds_router.register(r'status', BedStatusViewSet, basename='bed_status')
beds_router.register(r'available', BedAvailability, basename='available')

urlpatterns = [
    path(r'patient/', include(router.urls)),
    path(r'beds/', include(beds_router.urls))
]
