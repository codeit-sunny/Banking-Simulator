import random

def captcha():
    nums = list("0123456789")
    letters = list("abcdefghijklmnopqrstuvwxyz")
    cap = random.choices(nums + nums + nums + letters,k=4)
    return " ".join(cap)


def password():
    nums = list("0123456789")
    lower = list("abcdefghijklmnopqrstuvwxyz")
    upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    symbols = list("@#$%&*!?")

    password = random.choices(
        nums + lower + upper + symbols,
        k=8
    )

    return "".join(password)

def close_otp():
    otp = random.randint(1000,9999)
    return otp

def forgot_otp():
    otp = random.randint(1000,9999)
    return otp

