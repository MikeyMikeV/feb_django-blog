from django.urls import path
from user import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("user/create", views.create_user, name="create_user"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("activate/<user_id>/<token>/",views.activate, name='activate'),
]