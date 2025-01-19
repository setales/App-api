"""
Sample tests
"""
from django.test import SimpleTestCase

from app import calc

class ClacTests(SimpleTestCase):
    """Test calc module"""

    def test_add_number(self):
        """Test adding numbers together"""
        result = calc.add(5,5)

        self.assertEqual(result, 10)

    def test_substract_numbers(self):
        """Test substrackting numbers"""
        result = calc.subtract(10, 15)

        self.assertEqual(result, 5)