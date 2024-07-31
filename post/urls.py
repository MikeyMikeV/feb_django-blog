from django.urls import path
from post import views

urlpatterns = [
    path("<int:post_id>", views.post_detail, name="post_detail"),
    path("new", views.post_new, name="post_new"),
    path("<int:post_id>/edit", views.post_edit, name="post_edit"),
    path("<int:post_id>/confirm_delete", views.post_confirm_delete, name="post_confirm_delete"),
    path("<int:post_id>/delete", views.post_delete, name="post_delete"),
]