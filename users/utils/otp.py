import random


def generate_otp(symbols: str = "0123456789", length: int = 6) -> str:
    """
    Returns a random OTP
    """
    otp = ""
    for _ in range(length):
        otp += random.choice(symbols)
    return otp
