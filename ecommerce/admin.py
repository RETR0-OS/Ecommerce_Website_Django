from django.contrib import admin
from .models import Item, OrderItem, Order, BillingAddress, Coupon, Refund
# Register your models here.

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(Refund_requested=False, Refund_granted=True)
make_refund_accepted.short_description = 'Update refund status to granted'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'ordered_date', 'preproccessed', 'dispatched', 'Refund_requested', 'Refund_granted', 'delivered', 'user', 'billing_address']
    list_display_links = ['user', 'billing_address']
    list_filter = ['user', 'ordered', 'ordered_date', 'preproccessed', 'dispatched', 'Refund_requested', 'Refund_granted', 'delivered']
    search_fields = ['user__username', 'ref_code']
    actions = [make_refund_accepted]

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Coupon)
admin.site.register(Refund)
