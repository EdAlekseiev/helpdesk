from django.test import TestCase

from users.utils.otp import generate_otp


class GenerateOTPTestCase(TestCase):

    def test_default_length(self):
        otp = generate_otp()
        self.assertEqual(len(otp), 6)

    def test_custom_length(self):
        otp = generate_otp(length=8)
        self.assertEqual(len(otp), 8)

    def test_custom_symbols(self):
        otp = generate_otp(symbols="ABCDEF", length=4)
        self.assertTrue(all(char in "ABCDEF" for char in otp))

    def test_empty_symbols(self):
        with self.assertRaises(IndexError):
            generate_otp(symbols="")

    def test_numeric_otp(self):
        otp = generate_otp()
        self.assertTrue(otp.isdigit())
