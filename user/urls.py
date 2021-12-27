from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  (
    #Register
     signup,
    #  update_profile,
     profile,
     ProfileUpdateView,
     ProfileDeleteView,
     VerificationView
)    

app_name = 'user'

urlpatterns = [
    path('register/', signup, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/<int:pk>/<str:username>', profile, name='profile'),
    path('profile/<int:pk>/<str:username>/update', ProfileUpdateView.as_view(), name='update'),
    path('profile/<int:pk>/<str:username>/delete', ProfileDeleteView.as_view(), name='delete'),
    # path('profile/update', update_profile, name='update'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate')
]