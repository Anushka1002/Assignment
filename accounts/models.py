"""
account related models
"""

# third party imports
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import BedManager

GENERAL = "1"
SEMI_PRIVATE = "2"
PRIVATE = "3"

# bed status choices
BED_STATUS_CHOiCES = (
    (GENERAL, "General"),
    (SEMI_PRIVATE, "Semi Private"),
    (PRIVATE, "Private"),
)


class BaseDateModel(models.Model):
    """
    Common BaseData model for all the models in the project.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        Meta class of BaseDate Model.
        """
        abstract = True


class MyUser(BaseDateModel):
    """
    An base class implementing a fully featured User model with
    admin-compliant permissions.

    Email, password and role are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), unique=False)
    first_name = models.CharField(_('first name'), max_length=128, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.first_name)

    class Meta:
        """
        Meta class of User model.
        """
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Bed(BaseDateModel):
    """
    model to store bed info
    """
    bed_number = models.IntegerField(default=0)
    bed_type = models.CharField(choices=BED_STATUS_CHOiCES, max_length=1)
    is_available = models.BooleanField(default=False)

    objects = BedManager()

    def __str__(self):
        return str(self.bed_number)

    class Meta:
        """
        Meta class of Beds model.
        """
        verbose_name = _('beds')
        verbose_name_plural = _('beds')


class UserBed(BaseDateModel):
    """
    models to store user- beds relations
    """
    user = models.ForeignKey(MyUser, related_name="patient_bed", on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, related_name="bed_patient", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    class Meta:
        """
        Meta class of Beds model.
        """
        verbose_name = _('Patients Beds')
