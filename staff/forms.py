from django import forms

class Staff_Login_Form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mt-2 mb-2"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mt-2 mb-2"}))

FILTER_CHOICES = (
    ('all', 'all'),
    ('Not_Dispatched', 'Not Dispatched'),
    ('Dispatched', 'Dispatched'),
)

FILTER_REFUND_CHOICES = (
    ('all', 'all'),
    ('Not_Dispatched', 'Worker Not Dispatched'),
    ('Dispatched', 'Worker Dispatched'),
)

class PendingOrdersFilterForm(forms.Form):
    filter_by = forms.ChoiceField(choices=FILTER_CHOICES)

class PendingRefundsFilterForm(forms.Form):
    filter_by = forms.ChoiceField(choices=FILTER_REFUND_CHOICES)
