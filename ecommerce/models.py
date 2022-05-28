from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# Create your models here.

CATEGORY_CHOICES = (
    ('Genocide', 'Genocide'),
    ('Assasination', 'Assasination'),
    ('Silent', 'Silent'),
    ('Standard', 'Standard Equipment'),
    ('Banana', 'Banana Goodies'),
)

LABEL_CHOICES = (
    ('D', 'danger'),
    ('S', 'secondary'),
    ('P', 'primary'),
    ('ss', 'success'),
    ('w', 'warning'),
)

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=500, blank=True, null=True)
    coupon_discount_percentage = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.coupon_code

class Item(models.Model):
    itemName = models.CharField(max_length=300)
    itemPic = models.ImageField(blank=True, null=True)
    itemDescription = models.TextField()
    itemPrice = models.FloatField(default=0)
    itemDiscountPrice = models.FloatField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=500, default='Standard')
    label = models.CharField(choices=LABEL_CHOICES, max_length=500, default='D')
    slug = models.SlugField(default="Item")

    def __str__(self):
        return self.itemName
    def get_absolute_url(self):
        return reverse("ecommerce:view_item", kwargs={
            "slug":self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("ecommerce:add_to_cart", kwargs={
            "slug":self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("ecommerce:remove_from_cart", kwargs={
            "slug":self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.itemName}"
    def get_total_price_item(self):
        return self.quantity * self.item.itemPrice
    def get_total_dicount_item_price(self):
        return self.quantity * self.item.itemDiscountPrice
    def get_savings_item(self):
        return self.get_total_price_item() - self.get_total_dicount_item_price()
    def get_final_price(self):
        if self.item.itemDiscountPrice:
            return self.get_total_dicount_item_price()
        return self.get_total_price_item()
    #def get_coupon_discount(self):


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ref_code = models.CharField(max_length=20, default=1234)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey("BillingAddress", on_delete=models.SET_NULL, blank=True, null=True)
    Paid_price = models.FloatField(default=0)
    coupon = models.ForeignKey("Coupon", on_delete=models.SET_NULL, blank=True, null=True)
    preproccessed = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    Refund_requested = models.BooleanField(default=False)
    Refund_granted = models.BooleanField(default=False)
    RefundWorkerDispatched = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon is not None:
            coupon_dicount_ammount = total - (total*(self.coupon.coupon_discount_percentage/100))
            total -= (total * (self.coupon.coupon_discount_percentage/100))
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=10000000000)
    apartment_address = models.CharField(max_length=10000000000)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=10000000000)
    #payment_option =
    def __str__(self):
        return self.user.username

class Refund(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    refund_ammount = models.FloatField(default=0)
    requested_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.pk)
