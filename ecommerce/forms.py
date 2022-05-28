from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
class CheckOutForm(forms.Form):
    PAYMENT_CHOICES = (
        ('Card', 'Card'),
        ('Paypal', 'Paypal')
    )
    shipping_street_address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 mb-2"}))
    shipping_apartment_address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 mb-2"}), required=False)
    country = CountryField(blank_label="(Select Your Country)").formfield(widget=CountrySelectWidget(attrs={"class": "form-select mt-2 mb-2"}))
    zip = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 mb-2"}))
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect(attrs={"class":"form-check-input mt-2 mb-2 ms-3 me-3"}))
    #coupon_code = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 mb-2"}), required=False)

class CouponForm(forms.Form):
    coupon_code = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 mb-2", "placeholder":"promocode"}), required=False)

class PaymentForm(forms.Form):
    credit_card_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control", "minlength":"16","maxlength":"16"}))
    cvv = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mt-2 mb-2", "minlength":"3","maxlength":"3"}))
    expiry = forms.DateField(widget=forms.DateInput(attrs={"class":"form-control mt-2 mb-2"}))
    Name_on_card = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 mb-2"}))

class RefundForm(forms.Form):
    Order_Reference_Code = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 mb-2"}))
    Reason_For_Refund = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control mt-2 mb-2"}))
    Email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control mt-2 mb-2"}))
