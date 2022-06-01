from django.contrib.auth import authenticate
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
import numpy as np
import watch.utils
from watch.models import User, Contact, Config, AcceleratorData, HeartRateData, GPSData
from watch.serializers import ModelUserSerializer, SignUpSerializer, LoginSerializer, TokenSerializer, \
    UpdateContactSerializer, ViewContactsSerializer, UpdateUserSerializer, AcceleratorDataSerializer, GPSDataSerializer, \
    ChangePasswordSerializer
from django.core.exceptions import ValidationError
import torch
from watch.utils import GRUNet, input_dim, hidden_dim, output_dim, n_layers, MODEL_PATH
import os
from django.db import transaction
from urllib.request import urlopen


class SaveAccData(APIView):
    @swagger_auto_schema(operation_description="Signup API", request_body=AcceleratorDataSerializer,
                         responses={200: "Fall", 201: "ADL", 400: "BAD REQUEST"}, security=[])
    def post(self, request):
        WRITE_API = Config.objects.get(key="API_KEY").value
        BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)
        try:
            os.environ['CUDA_VISIBLE_DEVICES'] = ""
            if watch.utils.fall_detection_model is None:
                watch.utils.fall_detection_model = GRUNet(input_dim, hidden_dim, output_dim, n_layers)
                watch.utils.fall_detection_model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
            device = torch.device('cpu')
            torch.cuda.is_available = lambda: False
            watch.utils.fall_detection_model.to(device)
            request_ser = AcceleratorDataSerializer(data=request.data)
            request_ser.is_valid(raise_exception=True)
            returned_user_username = Config.objects.get(key='returned_user_username').value
            user = User.objects.get(username=returned_user_username)
            samples = request_ser.data.get('acc')
            samples = samples[:(len(samples) // 40) * 40]
            samples = np.asarray(samples).reshape(-1, 40, 3)
            fall = False
            with transaction.atomic():
                with torch.no_grad():
                    for sample in samples:
                        sensor_input = torch.Tensor(np.array([sample]))
                        X = sensor_input.cpu()
                        output = watch.utils.fall_detection_model(X)
                        pred = output.max(1, keepdim=True)[1]
                        situation = "Fall" if pred.item() else "ADL"
                        if situation == "Fall":
                            fall = True
                        for row in sample:
                            AcceleratorData(user=user, x=row[0], y=row[1], z=row[2],
                                            event=request_ser.data.get('event'), situation=situation).save()
                    heartRate = request_ser.data.get('heartRate')
                    HeartRateData(user=user, heartrate=heartRate).save()
                    gps_data = request_ser.data.get('gpsData')
                    if gps_data == 'no fix':
                        last_gps = GPSData.objects.filter(user=user)
                        if last_gps.count() > 0:
                            GPSData(user=user, lat=last_gps.latest('id').lat, long=last_gps.latest('id').long).save()
                        else:
                            default_lat = float(Config.objects.get(key='MAP_DEFAULT_LAT').value)
                            default_long = float(Config.objects.get(key='MAP_DEFAULT_LONG').value)
                            GPSData(user=user, lat=default_lat, long=default_long).save()
                    else:
                        gps_loc = gps_data.split(',')
                        GPSData(user=user, lat=gps_loc[0], long=gps_loc[1]).save()
            HeartRate = heartRate
            thingspeakHttp = BASE_URL + "&field1={:.2f}".format(HeartRate)
            conn = urlopen(thingspeakHttp)
            conn.close()
            if fall:
                return Response(status=status.HTTP_200_OK, data="Fall")
            else:
                return Response(status=status.HTTP_201_CREATED, data="ADL")
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Validation Error")
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))


class GetLocation(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_description="This API will get last GPS",
                         responses={200: "SUCCESS", 400: "BAD REQUEST", 401: "UNAUTHORIZED"})
    def get(self, request, *args, **kwargs):
        try:
            returned_user_username = Config.objects.get(key='returned_user_username').value
            zoom_level = float(Config.objects.get(key='MAP_ZOOM').value)
            if Config.objects.get(key='MAP_UPDATE').value == 'y':
                user = User.objects.get(username=returned_user_username)
                last_gps = GPSData.objects.filter(user=user).latest('id')
                url = f"http://www.openstreetmap.org/export/embed.html?bbox={last_gps.lat - zoom_level}%2C{last_gps.long - zoom_level}%2C{last_gps.lat + zoom_level}%2C{last_gps.long + zoom_level}&marker={last_gps.long}%2C{last_gps.lat}&layers=ND"
                return Response(status=status.HTTP_200_OK, data=url)
            else:
                lat = float(Config.objects.get(key='MAP_DEFAULT_LAT').value)
                long = float(Config.objects.get(key='MAP_DEFAULT_LONG').value)
                url = f"http://www.openstreetmap.org/export/embed.html?bbox={lat - zoom_level}%2C{long - zoom_level}%2C{lat + zoom_level}%2C{long + zoom_level}&marker={long}%2C{lat}&layers=ND"
                return Response(status=status.HTTP_200_OK, data=url)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))


class ChangePassword(APIView):
    @swagger_auto_schema(operation_description="Change password",
                         responses={200: "SUCCESS", 404: "NOT FOUND"})
    def post(self, request):
        request_ser = ChangePasswordSerializer(data=request.data)
        request_ser.is_valid(raise_exception=True)
        try:
            user = User.objects.get(username=request_ser.username)
            user.set_password(request_ser.new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)



class GetPhoneNumber(APIView):
    @swagger_auto_schema(operation_description="This API will get user phone",
                         responses={200: "SUCCESS"})
    def get(self, request, *args, **kwargs):
        try:
            returned_user_username = Config.objects.get(key='returned_user_username').value
            user = User.objects.get(username=returned_user_username)
            contacts = Contact.objects.get(user=user)
            phones = ""
            if contacts.phone_1 is not None and contacts.phone_1 != '':
                phones = contacts.phone_1
            return Response(status=status.HTTP_200_OK, data=phones)
        except Exception as e:
            return Response(status=status.HTTP_200_OK, data="SERVER ERROR")


class UserView(APIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()

    @swagger_auto_schema(operation_description="This API will show login user's info",
                         responses={200: ModelUserSerializer, 401: "UNAUTHORIZED"})
    def get(self, request, *args, **kwargs):
        user = request.user
        ser = ModelUserSerializer(user)
        return Response(status=status.HTTP_200_OK, data=ser.data)


class SignUp(APIView):

    @swagger_auto_schema(operation_description="Signup API", request_body=SignUpSerializer,
                         responses={200: TokenSerializer, 400: "BAD REQUEST"}, security=[])
    def post(self, request):
        request_ser = SignUpSerializer(data=request.data)
        request_ser.is_valid(raise_exception=True)
        user = request_ser.save()
        response_ser = TokenSerializer(data={})
        response_ser.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        response_ser.validated_data['jwt_refresh_token'] = str(refresh)
        response_ser.validated_data['jwt_access_token'] = str(access)
        response_ser.validated_data['id'] = user.id
        return Response(response_ser.data, status=status.HTTP_200_OK)


class UpdateUser(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_description="Update User API", request_body=UpdateUserSerializer,
                         responses={200: "SUCCESS", 400: "BAD REQUEST", 409: "CONFLICT"})
    def post(self, request):
        request_ser = UpdateUserSerializer(data=request.data)
        request_ser.is_valid(raise_exception=True)
        try:
            request_ser.update(request.user, request_ser.validated_data)
        except IntegrityError as e:
            return Response(status=status.HTTP_409_CONFLICT, data={'message': 'کاربری با این اطلاعات قبلا ثبت نام کرده است'})
        return Response(status=status.HTTP_200_OK)


class Login(TokenObtainPairView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(operation_description="Login", responses={200: TokenSerializer,
                                                                403: "FORBIDDEN"}, security=[])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_ser = TokenSerializer(data={})
        response_ser.is_valid(raise_exception=True)
        user = authenticate(request, username=serializer.data.get('username'), password=serializer.data.get('password'))
        if user is None:
            return Response(status=status.HTTP_403_FORBIDDEN, data="نام کاربری یا رمز عبور اشتباه است")
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        response_ser.validated_data['jwt_refresh_token'] = str(refresh)
        response_ser.validated_data['jwt_access_token'] = str(access)
        response_ser.validated_data['id'] = user.id
        return Response(response_ser.data, status=status.HTTP_200_OK)


class UpdateContacts(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_description="Create or update contacts of user",
                         request_body=UpdateContactSerializer, responses={200: "OK", 401: "UNAUTHORIZED",
                                                                          400: "BAD REQUEST"})
    def post(self, request):
        user = request.user
        if Contact.objects.filter(user=user).count() == 0:
            req_serializer = UpdateContactSerializer(data=request.data)
            req_serializer.is_valid(raise_exception=True)
            req_serializer.save(**{'user': user})
            return Response(status=status.HTTP_200_OK)
        else:
            req_serializer = UpdateContactSerializer(data=request.data)
            req_serializer.is_valid(raise_exception=True)
            Contact.objects.filter(user_id=request.user.id).delete()
            req_serializer.save(**{'user': user})
            return Response(status=status.HTTP_200_OK)


class ViewContacts(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_description="View Contacts",
                         responses={200: ViewContactsSerializer, 401: "UNAUTHORIZED"})
    def get(self, request):
        user = request.user
        if Contact.objects.filter(user=user).count() == 0:
            data = {}
            for i in range(1, 5):
                data[f"contact_{i}"] = ''
                data[f"phone_{i}"] = ''
            data = [data, ]
            response_serializer = ViewContactsSerializer(data)
            return Response(status=status.HTTP_200_OK, data=response_serializer.data)
        else:
            response_serializer = ViewContactsSerializer(Contact.objects.get(user=user))
            return Response(status=status.HTTP_200_OK, data=response_serializer.data)



