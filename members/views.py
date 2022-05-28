from django.shortcuts import render
from django.views import generic
from .forms import registerForm, editUserForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
# Create your views here.
class user_register_view(generic.CreateView):
    form_class = registerForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

class user_edit_view(LoginRequiredMixin, generic.UpdateView):
    form_class = editUserForm
    template_name = 'registration/edit_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class passwords_change_view(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    #messages.info(request, "Account password updated successfully")
    success_url = reverse_lazy('home')
