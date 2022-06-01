from pyexpat import model

from django.core.exceptions import ValidationError
from persiantools.jdatetime import JalaliDate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import IntegrityError
from watch.exception_handler import MIN_LENGTH_ERROR, MAX_LENGTH_ERROR, BLANK_ERROR, FIX_LENGTH_ERROR \
    , REQUIRED_ERROR, INVALID_ERROR, INVALID_CHOICE_ERROR, MIN_VALUE_ERROR, UNIQUE_ERROR
from watch.models import User, Contact, WatchCode


class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32, required=True, allow_blank=False, allow_null=False)
    new_password = serializers.CharField(max_length=32, min_length=8, required=True, allow_blank=False, allow_null=False)


class ModelUserSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    birthday = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'firstname', 'lastname', 'gender', 'watch_code', 'birthday']

    def get_gender(self, obj):
        if obj.gender:
            return 'زن'
        return 'مرد'

    def get_birthday(self, obj):
        return JalaliDate(obj.birthday).isoformat()


class SignUpSerializer(serializers.ModelSerializer):
    GENDER_CHOICES = (
        ('مرد', 'Male'),
        ('زن', 'Female'),
    )
    password = serializers.CharField(min_length=8, max_length=32, error_messages={"required": REQUIRED_ERROR,
                                                                                  "blank": BLANK_ERROR,
                                                                                  "min_length": MIN_LENGTH_ERROR.format(8),
                                                                                  "max_length": MAX_LENGTH_ERROR.format(32)})
    password_confirm = serializers.CharField(min_length=8, max_length=32, error_messages={"required": REQUIRED_ERROR,
                                                                                          "blank": BLANK_ERROR,
                                                                                          "min_length": MIN_LENGTH_ERROR.format(8),
                                                                                          "max_length": MAX_LENGTH_ERROR.format(32)})
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, error_messages={"invalid_choice": INVALID_CHOICE_ERROR.format("'مرد' یا 'زن'"),
                                                                             "required": REQUIRED_ERROR,
                                                                             "blank": BLANK_ERROR})
    birthday = serializers.RegexField("^(13[0-9][0-9])-([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$",
                                      error_messages={"invalid": INVALID_ERROR.format('تاریخ', 'روز-ماه-سال (به صورت 4 رقمی)'),
                                                      "blank": BLANK_ERROR})
    username = serializers.CharField(min_length=4, max_length=32,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message=UNIQUE_ERROR)]
                                     , error_messages={"required": REQUIRED_ERROR,
                                                       "blank": BLANK_ERROR,
                                                       "min_length": MIN_LENGTH_ERROR.format(4),
                                                       "max_length": MAX_LENGTH_ERROR.format(32)})
    watch_code = serializers.CharField(min_length=8, max_length=16,
                                       validators=[UniqueValidator(queryset=User.objects.all(), message=UNIQUE_ERROR)],
                                       error_messages={"required": REQUIRED_ERROR,
                                                       "blank": BLANK_ERROR,
                                                       "unique": UNIQUE_ERROR,
                                                       "max_length": MAX_LENGTH_ERROR.format(16),
                                                       "min_length": MIN_LENGTH_ERROR.format(8)})


    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'phone', 'email', 'firstname', 'lastname', 'gender',
                  'watch_code', 'birthday']
        extra_kwargs = {'phone': {'min_length': 11, 'error_messages': {"required": REQUIRED_ERROR,
                                                                       "blank": BLANK_ERROR,
                                                                       "min_length": FIX_LENGTH_ERROR.format(11),
                                                                       "max_length": FIX_LENGTH_ERROR.format(11)}},
                        'email': {'min_length': 6, 'error_messages': {"required": REQUIRED_ERROR,
                                                                      "blank": BLANK_ERROR,
                                                                      "min_length": MIN_LENGTH_ERROR.format(6),
                                                                      "max_length": MAX_LENGTH_ERROR.format(64),
                                                                      "invalid": INVALID_ERROR.format('ایمیل', "aa@bb.cc")}},
                        'firstname': {'min_length': 2, 'error_messages': {"required": REQUIRED_ERROR,
                                                                          "blank": BLANK_ERROR,
                                                                          "min_length": MIN_LENGTH_ERROR.format(2),
                                                                          "max_length": MAX_LENGTH_ERROR.format(32)}},
                        'lastname': {'min_length': 2, 'error_messages': {"required": REQUIRED_ERROR,
                                                                         "blank": BLANK_ERROR,
                                                                         "min_length": MIN_LENGTH_ERROR.format(2),
                                                                         "max_length": MAX_LENGTH_ERROR.format(32)}}}

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise ValidationError({'password_confirm': 'رمز عبور با تکرار آن یکسان نمی باشد'})
        if WatchCode.objects.filter(code=attrs.get('watch_code')).count() == 0:
            raise ValidationError({'watch_code': "این کد ساعت تعریف نشده است."})
        return attrs

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)
        date_str = validated_data.pop('birthday', None)
        date_elements = date_str.split('-')
        birthday = JalaliDate(int(date_elements[0]), int(date_elements[1]), int(date_elements[2])).to_gregorian()
        validated_data['birthday'] = birthday
        gender = validated_data.pop('gender', 'a')
        if gender == 'زن':
            validated_data['gender'] = True
        elif gender == 'مرد':
            validated_data['gender'] = False
        else:
            raise serializers.ValidationError({'gender': "مقدار این فیلد می تواند تنها 'مرد' یا 'زن' باشد"})

        instance = User.objects.create_user(username, password, **validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.password = validated_data['password']
        instance.phone = validated_data['phone']
        instance.email = validated_data['email']
        instance.firstname = validated_data['firstname']
        instance.lastname = validated_data['lastname']
        instance.gender = True if validated_data['gender'] == 'زن' else False
        instance.watch_code = validated_data['watch_code']
        date_str = validated_data['birthday']
        date_elements = date_str.split('-')
        birthday = JalaliDate(int(date_elements[0]), int(date_elements[1]), int(date_elements[2])).to_gregorian()
        instance.birthday = birthday


class UpdateUserSerializer(serializers.Serializer):
    GENDER_CHOICES = (
        ('مرد', 'Male'),
        ('زن', 'Female'),
    )

    username = serializers.CharField(min_length=4, max_length=32, allow_blank=False, required=False, allow_null=False,
                                     error_messages={'min_length': MIN_LENGTH_ERROR.format(4),
                                                     'max_length': MAX_LENGTH_ERROR.format(32),
                                                     'blank': BLANK_ERROR,
                                                     'unique': UNIQUE_ERROR})
    password = serializers.CharField(min_length=8, max_length=32, allow_blank=False, required=False, allow_null=False,
                                     error_messages={'min_length': MIN_LENGTH_ERROR.format(8),
                                                     'max_length': MAX_LENGTH_ERROR.format(32),
                                                     'blank': BLANK_ERROR})
    password_confirm = serializers.CharField(min_length=8, max_length=32, allow_blank=False, required=False, allow_null=False,
                                     error_messages={'min_length': MIN_LENGTH_ERROR.format(8),
                                                     'max_length': MAX_LENGTH_ERROR.format(32),
                                                     'blank': BLANK_ERROR})
    phone = serializers.CharField(min_length=11, max_length=11, allow_blank=False, required=False, allow_null=False,
                                  error_messages={'min_length': FIX_LENGTH_ERROR.format(11),
                                                  'max_length': FIX_LENGTH_ERROR.format(11),
                                                  'blank': BLANK_ERROR})
    email = serializers.EmailField(min_length=6, max_length=64, allow_blank=False, required=False, allow_null=False,
                                   error_messages={'min_length': MIN_LENGTH_ERROR.format(6),
                                                   'max_length': MAX_LENGTH_ERROR.format(64),
                                                   'blank': BLANK_ERROR,
                                                   'invalid': INVALID_ERROR.format('ایمیل', 'aa@bb.cc')})
    firstname = serializers.CharField(min_length=2, max_length=32, allow_blank=False, required=False, allow_null=False,
                                      error_messages={'min_length': MIN_LENGTH_ERROR.format(2),
                                                      'max_length': MAX_LENGTH_ERROR.format(32),
                                                      'blank': BLANK_ERROR})
    lastname = serializers.CharField(min_length=2, max_length=32, allow_blank=False, required=False, allow_null=False,
                                      error_messages={'min_length': MIN_LENGTH_ERROR.format(2),
                                                      'max_length': MAX_LENGTH_ERROR.format(32),
                                                      'blank': BLANK_ERROR})
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=False, allow_null=False, allow_blank=False,
                                     error_messages={"invalid_choice": INVALID_CHOICE_ERROR.format("'مرد' یا 'زن'"),
                                                     "blank": BLANK_ERROR})
    watch_code = serializers.CharField(allow_null=False, required=False, max_length=16, min_length=8,
                                          error_messages={"required": REQUIRED_ERROR,
                                                          "blank": BLANK_ERROR,
                                                          'unique': UNIQUE_ERROR,
                                                          'max_length': MAX_LENGTH_ERROR.format(16),
                                                          'min_length': MIN_LENGTH_ERROR.format(8)})
    birthday = serializers.RegexField("^(13[0-9][0-9])-([1-9]|0[1-9]|1[0-2])-([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$", required=False, allow_null=False, allow_blank=False,
                                      error_messages={"invalid": INVALID_ERROR.format('تاریخ', "روز-ماه-سال (به صورت 4 رقمی)"),
                                                      "blank": BLANK_ERROR})

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise ValidationError({'password_confirm': 'رمز عبور با تکرار آن یکسان نمی باشد'})
        watch_code = attrs.get('watch_code')
        if WatchCode.objects.filter(code=watch_code).count() == 0:
            raise ValidationError({'watch_code': 'این کد ساعت تعریف نشده است.'})
        return attrs

    def update(self, instance, validated_data):
        watch_code = validated_data.get('watch_code')
        if watch_code != instance.watch_code and User.objects.filter(watch_code=watch_code).count() > 0:
            raise IntegrityError()
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.email = validated_data.get('email', instance.email)
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.gender = True if validated_data.get('gender', 'زن' if instance.gender else 'مرد') == 'زن' else False
        instance.watch_code = validated_data.get('watch_code', instance.watch_code)
        date_str = validated_data.get('birthday', None)
        if date_str is not None:
            date_elements = date_str.split('-')
            birthday = JalaliDate(int(date_elements[0]), int(date_elements[1]), int(date_elements[2])).to_gregorian()
            instance.birthday = birthday
        instance.set_password(validated_data.get('password'))
        instance.save()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32, required=True, allow_blank=False, min_length=4,
                                     error_messages={"required": REQUIRED_ERROR,
                                                     "blank": BLANK_ERROR,
                                                     "max_length": MAX_LENGTH_ERROR.format(32),
                                                     "min_length": MIN_LENGTH_ERROR.format(4)})
    password = serializers.CharField(min_length=8, max_length=32, required=True,
                                     error_messages={"blank": BLANK_ERROR,
                                                     "min_length": MIN_LENGTH_ERROR.format(8),
                                                     "max_length": MAX_LENGTH_ERROR.format(32)})


class TokenSerializer(serializers.Serializer):
    jwt_access_token = serializers.CharField(max_length=400, required=False)
    jwt_refresh_token = serializers.CharField(max_length=400, required=False)
    id = serializers.IntegerField(required=False)


class UpdateContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('contact_1', 'phone_1', 'contact_2', 'phone_2', 'contact_3', 'phone_3', 'contact_4', 'phone_4', 'contact_5', 'phone_5')
        extra_kwargs = {
            'contact_1': {'allow_null': True, 'allow_blank': True},
            'contact_2': {'allow_null': True, 'allow_blank': True},
            'contact_3': {'allow_null': True, 'allow_blank': True},
            'contact_4': {'allow_null': True, 'allow_blank': True},
            'contact_5': {'allow_null': True, 'allow_blank': True},
            'phone_1': {'allow_null': True, 'allow_blank': True},
            'phone_2': {'allow_null': True, 'allow_blank': True},
            'phone_3': {'allow_null': True, 'allow_blank': True},
            'phone_4': {'allow_null': True, 'allow_blank': True},
            'phone_5': {'allow_null': True, 'allow_blank': True},
        }

    def validate(self, attrs):
        all_null = True
        if (attrs.get("contact_1", '') == '' or attrs.get("contact_1", '') is None) or \
            (attrs.get("phone_1", '') == '' or attrs.get("phone_1", '') is None):
            raise ValidationError({"contact_1": "این مخاطب به همراه شماره اش باید وارد شود."})
        for i in range(2, 6):
            if attrs.get(f"phone_{i}", '') != '' and attrs.get(f"phone_{i}", '') is not None:
                raise ValidationError({f"phone_{i}": "در حالت رایگان، تنها از مخاطب اول می توان استفاده کرد"})
            if attrs.get(f"contact_{i}", '') != '' and attrs.get(f"contact_{i}", '') is not None:
                raise ValidationError({f"contact_{i}": "در حالت رایگان، تنها از مخاطب اول می توان استفاده کرد"})
        return attrs

    def create(self, validated_data):
        contact = Contact.objects.create(**validated_data)
        return contact


class ViewContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('contact_1', 'phone_1', 'contact_2', 'phone_2', 'contact_3', 'phone_3', 'contact_4', 'phone_4', 'contact_5', 'phone_5')
        extra_kwargs = {"contact_1": {"required": False, "allow_null": True, "allow_blank": True},
                        "contact_2": {"required": False, "allow_null": True, "allow_blank": True},
                        "contact_3": {"required": False, "allow_null": True, "allow_blank": True},
                        "contact_4": {"required": False, "allow_null": True, "allow_blank": True},
                        "contact_5": {"required": False, "allow_null": True, "allow_blank": True},
                        "phone_1": {"required": False, "allow_null": True, "allow_blank": True},
                        "phone_2": {"required": False, "allow_null": True, "allow_blank": True},
                        "phone_3": {"required": False, "allow_null": True, "allow_blank": True},
                        "phone_4": {"required": False, "allow_null": True, "allow_blank": True},
                        "phone_5": {"required": False, "allow_null": True, "allow_blank": True}}


class AcceleratorDataSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    acc = serializers.ListSerializer(child=serializers.ListSerializer(child=serializers.FloatField()))
    heartRate = serializers.IntegerField()
    gpsData = serializers.CharField(max_length=64)


class GPSDataSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()