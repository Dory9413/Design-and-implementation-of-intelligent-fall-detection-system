from django.core.exceptions import ValidationError


def check_phone(value):
    if value.isnumeric() and len(value) == 11 and value.startswith("09"):
        pass
    else:
        raise ValidationError("فرمت شماره تلفن اشباه است")
