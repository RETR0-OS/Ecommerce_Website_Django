from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import user_register_view, user_edit_view, passwords_change_view

app_name = "members"

urlpatterns = [
    path('register/', user_register_view.as_view(), name="register"),
    path('edit_account/', user_edit_view.as_view(), name="edit_account"),
    path('password/', passwords_change_view.as_view(template_name="registration/change_password.html"), name="change_password"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
