from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import Staff_Login_Form, PendingOrdersFilterForm, PendingRefundsFilterForm
from django.contrib.auth import *
from django.contrib.auth.mixins import LoginRequiredMixin
from ecommerce.models import Order, Refund
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
#from django.views import GroupRequiredMixin
# Create your views here.

#@staff_member_required
def staff_home(request):
    if not request.user.is_staff:
        return redirect("/")
    else:
        if request.user.groups.filter(name='Delivery_staff_admin').exists() or request.user.is_superuser:
            return redirect("staff:pending_orders")
        elif request.user.groups.filter(name='Preprosessing_staff_admin').exists():
            return redirect("staff:pending_preprocessing")
        else:
            messages.warning(request, "You do not have permission to access this resource!")
            return redirect("home")

class staff_login(generic.View):
    def get(self, *args, **kwargs):
        staff_login_form = Staff_Login_Form()
        context = {
            "login_form": staff_login_form
        }
        return render(self.request, "staff/staff_login.html", context)
    def post(self, *args, **kwargs):
        form = Staff_Login_Form(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request, username=username, password=password)
            if user is not None and user.is_staff:
                login(self.request, user)
                return redirect("staff:staff_home")
            elif user is not None and not user.is_staff:
                messages.warning(self.request, "You do not have permission to access this resource!")
                return redirect("/")
            else:
                messages.info(self.request, "User does not exist!")
                return redirect("/")


#@staff_member_required
class delivery_staff_view_pending_orders(LoginRequiredMixin, generic.View):
     def get(self, *args, **kwargs):
         if self.request.user.groups.filter(name='Delivery_staff_admin').exists() or self.request.user.is_superuser:
             pending_orders = Order.objects.filter(preproccessed=True, ordered=True, delivered=False)
             filter_form = PendingOrdersFilterForm()
             context= {
                "pending_orders_list": pending_orders,
                "filter_form": filter_form
             }
             return render(self.request, "staff/delivery/pending_orders.html", context)
         else:
             messages.warning(self.request, "You do not have permission to access this resource!")
             return redirect("/")
     def post(self, *args, **kwargs):
        my_form = PendingOrdersFilterForm(self.request.POST)
        if my_form.is_valid():
            filter_form = PendingOrdersFilterForm()
            filter_option = my_form.cleaned_data.get("filter_by")
            if filter_option =="Not_Delivered":
                try:
                    pending_orders = Order.objects.filter(preproccessed=True, ordered=True, delivered=False)
                except ObjectDoesNotExist:
                    messages.info(self.request, "No such orders")
            elif filter_option =="Delivered":
                try:
                    pending_orders = Order.objects.filter(preproccessed=True, ordered=True, delivered=True)
                except ObjectDoesNotExist:
                    messages.info(self.request, "No such orders")
            elif filter_option =="Not_Dispatched":
                try:
                    pending_orders = Order.objects.filter(preproccessed=True, ordered=True, dispatched=False)
                except ObjectDoesNotExist:
                    messages.info(self.request, "No such orders")
            elif filter_option =="Dispatched":
                try:
                    pending_orders = Order.objects.filter(preproccessed=True, ordered=True, dispatched=True)
                except ObjectDoesNotExist:
                    messages.info(self.request, "No such orders")
            else:
                try:
                    pending_orders = Order.objects.filter(preproccessed=True, ordered=True, delivered=False)
                except ObjectDoesNotExist:
                    messages.info(self.request, "No such orders")
            context= {
               "filter_form": filter_form,
               "pending_orders_list": pending_orders
            }
            return render(self.request, "staff/delivery/pending_orders.html", context)

class  delivery_staff_view_pending_refunds(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Delivery_staff_admin').exists() or self.request.user.is_superuser:
            pending_refunds = Refund.objects.filter(accepted=True)
            filter_form = PendingRefundsFilterForm()
            context= {
               "pending_refunds_list": pending_refunds,
               "filter_form": filter_form
            }
            return render(self.request, "staff/delivery/pending_refunds.html", context)
        else:
            messages.warning(self.request, "You do not have permission to access this resource!")
            return redirect("/")
    def post(self, *args, **kwargs):
       my_form = PendingRefundsFilterForm(self.request.POST)
       if my_form.is_valid():
           filter_form = PendingRefundsFilterForm()
           filter_option = my_form.cleaned_data.get("filter_by")
           if filter_option =="Not_Dispatched":
               try:
                   pending_refunds = Refund.objects.filter(accepted=True, order__RefundWorkerDispatched=False)
               except ObjectDoesNotExist:
                   messages.info(self.request, "No such orders")
           elif filter_option =="Dispatched":
               try:
                   pending_refunds = Refund.objects.filter(accepted=True, order__RefundWorkerDispatched=True)
               except ObjectDoesNotExist:
                   messages.info(self.request, "No such orders")
           else:
               try:
                   pending_refunds = Refund.objects.filter(accepted=True)
               except ObjectDoesNotExist:
                   messages.info(self.request, "No such orders")
           context= {
              "filter_form": filter_form,
              "pending_refunds_list": pending_refunds
           }
           return render(self.request, "staff/delivery/pending_refunds.html", context)

class delivery_staff_search_pending_orders(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Delivery_staff_admin').exists() or self.request.user.is_superuser:
            search_query = self.request.GET['query']
            filter_form = PendingOrdersFilterForm()
            orders = Order.objects.filter(preproccessed=True, ordered=True, delivered=False)
            searched_pending_orders = orders.filter(user__first_name__icontains=search_query)
            if len(searched_pending_orders) < 1:
                searched_pending_orders = orders.filter(user__last_name__icontains=search_query)
                if len(searched_pending_orders) < 1:
                    messages.warning(self.request, "[!] No order by this user found!")
                    searched_pending_orders = Order.objects.filter(preproccessed=True, ordered=True, delivered=False)
            context = {
                "filter_form": filter_form,
                "pending_orders_list": searched_pending_orders
            }
            return render(self.request, "staff/delivery/pending_orders.html", context)


class delivery_staff_search_pending_refunds(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Delivery_staff_admin').exists() or self.request.user.is_superuser:
            search_query = self.request.GET['query']
            filter_form = PendingRefundsFilterForm()
            refunds = Refund.objects.filter(accepted=True)
            searched_pending_refunds = refunds.filter(order__user__first_name__icontains=search_query)
            if len(searched_pending_refunds) < 1:
                searched_pending_orders = refunds.filter(order__user__last_name__icontains=search_query)
                if len(searched_pending_refunds) < 1:
                    messages.warning(self.request, "[!] No refund for this user found!")
                    searched_pending_refunds = Refund.objects.filter(accepted=True)
            context = {
                "filter_form": filter_form,
                "pending_refunds_list": searched_pending_refunds
            }
            return render(self.request, "staff/delivery/pending_refunds.html", context)




########################

class preprocessing_staff_view_pending_preprocessings(LoginRequiredMixin, generic.View):
     def get(self, *args, **kwargs):
         if self.request.user.groups.filter(name='Preprosessing_staff_admin').exists() or self.request.user.is_superuser:
             pending_orders = Order.objects.filter(preproccessed=False, ordered=True, delivered=False)
             #filter_form = PendingOrdersFilterForm()
             context= {
                "pending_orders_list": pending_orders,
                #"filter_form": filter_form
             }
             return render(self.request, "staff/preprocessing_unit/pending_preprocessings.html", context)
         else:
             messages.warning(self.request, "You do not have permission to access this resource!")
             return redirect("home")

class preprocessing_staff_search_pending_preprocessings(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Preprosessing_staff_admin').exists() or self.request.user.is_superuser:
            search_query = self.request.GET['query']
            #filter_form = PendingOrdersFilterForm()
            orders = Order.objects.filter(preproccessed=False, ordered=True, delivered=False)
            searched_pending_orders = orders.filter(user__first_name__icontains=search_query)
            if len(searched_pending_orders) < 1:
                searched_pending_orders = orders.filter(user__last_name__icontains=search_query)
                if len(searched_pending_orders) < 1:
                    messages.warning(self.request, "[!] No order by this user found!")
                    searched_pending_orders = Order.objects.filter(preproccessed=True, ordered=True, delivered=False)
            context = {
                #"filter_form": filter_form,
                "pending_orders_list": searched_pending_orders
            }
            return render(self.request, "staff/preprocessing_unit/pending_preprocessings.html", context)

@login_required
def ListPendingPreprocessingOrderDetails(request, pk):
    if request.method == "GET":
        try:
            order = Order.objects.get(pk=pk, ordered=True, preproccessed=False)
            context = {
                "order": order,
            }
            return render(request, "staff/preprocessing_unit/pending_preprocessing_order_details.html", context)
            if order.count()<1:
                messages.info(request, "No such order has is there for preprocessing!")
                return redirect("staff:pending_preprocessing")
        except ObjectDoesNotExist:
            messages.info(request, "No such order has is there for preprocessing!")
            return redirect("ecommerce:my_orders")
