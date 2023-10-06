from django.urls import path
from account import views
from account.views import UserLoginView,UserRegistrationView,UserProfileView,UserChangePasswordView
from .views import save_event_api


urlpatterns = [
    path('', views.index, name='index'), 
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('event/save/', save_event_api, name='save_event_api'),
    path("event/get", views.get_event_details),

]