from copy import deepcopy
from rest_framework.views import exception_handler


MIN_LENGTH_ERROR = "این فیلد باید حداقل شامل {} کاراکتر باشد"
MAX_LENGTH_ERROR = "این فیلد باید حداکثر شامل {} کاراکتر باشد"
FIX_LENGTH_ERROR = "این فیلد باید {} کاراکتر باشد"
BLANK_ERROR = "این فیلد نباید خالی باشد"
REQUIRED_ERROR = "پر کردن این فیلد اجباری است"
INVALID_ERROR = "فرمت {} باید به صورت '{}' باشد"
INVALID_CHOICE_ERROR = "مقدار این فیلد می تواند تنها {} باشد"
MIN_VALUE_ERROR = "مقدار این فیلد باید از {} بزرگتر باشد"
UNIQUE_ERROR = "کاربری با این مشخصات قبلا ثبت نام کرده است"


