"""
common helper methods
"""
from accounts.models import Bed


def get_bed(bed_type=None):
    """
    method to get bed for patient
    """
    beds = Bed.objects.filter(is_active=True, is_available=True)

    if bed_type:
        beds = beds.filter(bed_type=bed_type)

    return beds.order_by("bed_number").last()
