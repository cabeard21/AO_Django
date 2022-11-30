import os

from django import setup
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AO_Django.settings")
setup()


class TestSimPy(TestCase):

    def test_can_simulate_equipment_set_with_rotation(self):
        # Select equipment set

        # Select an ability rotation

        # Simulate the set with the rotation

        # See output stats like dps, TTL, debuff/buff uptimes, etc
        assert False, "Finish the test!!"
