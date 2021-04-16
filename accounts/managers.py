"""
Custom Manager
"""
# third party imports
from django.db import models


class BedManager(models.Manager):
    """
    Manager for genre model.
    """

    def active_beds(self):
        """
        To check if bed is active
        :return: boolean true
        """
        return self.filter(is_active=True)
