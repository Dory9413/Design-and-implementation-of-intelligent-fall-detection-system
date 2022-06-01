from django.urls import path

from watch import views

app_name = 'app'

urlpatterns = [
    path('app/view-user/', views.UserView.as_view(), name='view_user'),
    path('app/signup/', views.SignUp.as_view(), name='signup'),
    path('app/update-user/', views.UpdateUser.as_view(), name='update_user'),
    path('app/login/', views.Login.as_view(), name='login'),
    path('app/update-contacts/', views.UpdateContacts.as_view(), name='update_contacts'),
    path('app/view-contacts/', views.ViewContacts.as_view(), name='view_contacts'),
    path('app/get-contacts/', views.GetPhoneNumber.as_view(), name='get_contacts'),
    path('app/save-acc-data/', views.SaveAccData.as_view(), name='save_accelerator_data'),
    path('app/get-gps/', views.GetLocation.as_view(), name='get_location'),
]