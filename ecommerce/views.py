from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, OrderItem, BillingAddress, Coupon, Refund
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckOutForm, PaymentForm, CouponForm, RefundForm
import random, string
# Create your views here.

class items_list(generic.ListView):
    model = Item
    ordering = ['-id']
    paginate_by = 4
    template_name = "items_list.html"

def generate_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class items_detail(generic.DetailView):
    model = Item
    template_name = "item_details.html"

class OrderSummary(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context= {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order!")
            return redirect("/")

@login_required
def add_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item was added to your cart!")
        else:
            order.items.add(order_item)
            order_item.quantity = 1
            messages.info(request, "This item was added to your cart!")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart!")

    return redirect("ecommerce:view_item", slug=slug)

@login_required
def remove_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.error(request, "This item was removed from your cart!")
            return redirect("ecommerce:view_item", slug=slug)
        else:
            messages.info(request, "You don't have this item in your cart!")
            return redirect("ecommerce:view_item", slug=slug)
    else:
        messages.info(request, "You don't have an active order!!")
        return redirect("ecommerce:view_item", slug=slug)

@login_required
def remove_one_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_item.quantity -= 1
            if order_item.quantity <= 0:
                order.items.remove(order_item)
                messages.info(request, "This item was removed from your cart!")
            else:
                order_item.save()
                messages.info(request, "This item's quantity was reduced from your cart!")
            return redirect("ecommerce:order_summary")
        else:
            messages.info(request, "You don't have this item in your cart!")
            return redirect("ecommerce:view_item", slug=slug)
    else:
        messages.info(request, "You don't have an active order!!")
        return redirect("ecommerce:view_item", slug=slug)

def delete_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.error(request, "This item was removed from your cart!")
            return redirect("ecommerce:order_summary")
        else:
            messages.info(request, "You don't have this item in your cart!")
            return redirect("ecommerce:order_summary")
    else:
        messages.info(request, "You don't have an active order!!")
        return redirect("ecommerce:order_summary")

class checkout_view(generic.View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            coupon_form = CouponForm()
            form = CheckOutForm()
            context = {
                'form': form,
                'object': order,
                'coupon_form': coupon_form
            }
            return render(self.request, "check_out.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order!")
            return redirect("ecommerce:order_summary")

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('shipping_street_address')
                apartment_address = form.cleaned_data.get('shipping_apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                if payment_option == 'Card':
                    return redirect('ecommerce:payment', payment_option="Card")
                elif payment_option == 'Paypal':
                    return redirect('ecommerce:payment', payment_option="Paypal")
            else:
                messages.info(self.request, "The form you submitted was incorrect!")
                return redirect("/")
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order!")
            return redirect("ecommerce:order_summary")

class PaymentView(generic.View):
    def get(self, *args, **kwargs):
        form = PaymentForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context ={
                "form": form,
                "object": order
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, "You have not added a shipping address!")
            return redirect("ecommerce:checkout")

    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            #order_item = OrderItem.objects.filter(user=self.request.user, ordered=False)
            if form.is_valid:
                #order_item.ordered = True
                #order_item.save()
                order.ordered = True
                order.ref_code = generate_ref_code()
                order.Paid_price = order.get_total()
                order.coupon = None
                order.save()
                return render(self.request, "payment_successful.html")
            else:
                messages.info("The form you submitted was incorrect")
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order!")
            return redirect("ecommerce:order_summary")

def add_coupon_code(request):
    if request.method == "POST":
        form = CouponForm(request.POST or None)
        if form.is_valid():
            coupon = form.cleaned_data.get("coupon_code")
            try:
                order = Order.objects.get(user=request.user, ordered=False)
                try:
                    coupon = Coupon.objects.get(coupon_code=coupon)
                    Order.coupon = coupon
                    messages.success(request, "Added coupon success fully!")
                    return redirect("ecommerce:checkout")
                except:
                    messages.info(request, "This is not a valid coupon!")
                    return redirect("ecommerce:checkout")
            except ObjectDoesNotExist:
                messages.info(request, "You do not have an active order!")
                return redirect("ecommerce:items_list")
        else:
            messages.info(request, "The form you submitted was not valid!")
            return redirect("ecommerce:items_list")

class request_refund(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context ={
            'form': form
        }
        return render(self.request, "request_refund.html", context)
    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code  = form.cleaned_data.get("Order_Reference_Code")
            reason = form.cleaned_data.get("Reason_For_Refund")
            email = form.cleaned_data.get("Email")
            try:
                order = Order.objects.get(ref_code=ref_code, ordered=True, user=self.request.user)
                order.Refund_requested = True
                order.save()
                refund = Refund(order=order, reason=reason, email=email, refund_ammount=order.Paid_price)
                refund.save()
                messages.info(self.request, "Your request has been recieved!")
                return redirect("ecommerce:request_refund")
            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist!")
                return redirect("ecommerce:request_refund")

class search_product(generic.View):
    def get(self, *args, **kwargs):
        search_query = self.request.GET['query']
        items = Item.objects.filter(itemName__icontains = search_query)
        items_count = items.count()
        message = ""
        if items_count < 1:
            items = Item.objects.filter(category__icontains=search_query)
            items_count = items.count()
            if items_count < 1:
                if items_count < 1:
                    items = Item.objects.filter(itemPrice__icontains=search_query)
                    items_count = items.count()
                    if items_count < 1:
                        items = Item.objects.filter(itemDescription__icontains=search_query)
                        items_count = items.count()
                        if items_count < 1:
                            messages.info(self.request, "No such items found! Please try a different keyword")
                            items = Item.objects.all()
        context = {
            "object_list": items,
        }
        return render(self.request, "items_list.html", context)

class ListOrdersByUser(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        try:
            orders = Order.objects.filter(user=self.request.user, ordered=True, delivered=True)
            print(orders.count())
            context = {
                "orders": orders,
            }
            if orders.count() < 1:
                messages.info(self.request, "You have not ordered anything yet. Visit the shop to order now!")
                return redirect("home")
            return render(self.request, "past_orders_page.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You have not ordered anything yet. Visit the shop to order now!")
            return redirect("home")

@login_required
def ListOrderDetailsByUser(request, pk):
    if request.method == "GET":
        try:
            order = Order.objects.get(pk=pk, ordered=True, user=request.user, delivered=True)
            context = {
                "order": order,
            }
            return render(request, "past_order_details.html", context)
        except ObjectDoesNotExist:
            messages.info(request, "No such order has been made by you!")
            return redirect("ecommerce:my_past_orders")

class ListCurrentOrdersByUser(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        try:
            orders = Order.objects.filter(user=self.request.user, ordered=True, delivered=False)
            print(orders.count())
            context = {
                "orders": orders,
            }
            if orders.count() < 1:
                messages.info(self.request, "You have no currently active orders. Visit the shop to order now!")
                return redirect("home")
            return render(self.request, "current_orders_page.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "You have no currently active orders. Visit the shop to order now!")
            return redirect("home")

@login_required
def ListCurrentOrderDetailsByUser(request, pk):
    if request.method == "GET":
        try:
            order = Order.objects.get(pk=pk, ordered=True, user=request.user, delivered=False)
            context = {
                "order": order,
            }
            return render(request, "current_order_details.html", context)
        except ObjectDoesNotExist:
            messages.info(request, "No such undelivered order has been made by you!")
            return redirect("ecommerce:my_current_orders")

@login_required
def cancel_Order(request, pk):
    if request.method == "GET":
        try:
            order = Order.objects.get(pk=pk, ordered=True, user=request.user, delivered=False)
            order.delete()
            orders = Order.objects.filter(ordered=True, user=request.user, delivered=False)
            messages.info(request, "The order has been cancelled!")
            if orders.count() > 0:
                return redirect("ecommerce:my_current_orders")
            else:
                return redirect("home")
        except ObjectDoesNotExist:
            orders = Order.objects.filter(ordered=True, user=request.user, delivered=False)
            messages.info(request, "No such undelivered order has been made by you!")
            if orders.count() > 0:
                return redirect("ecommerce:my_current_orders")
            else:
                return redirect("home")
