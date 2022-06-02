from django.urls import path
from .views import items_detail, items_list, add_item_to_cart, remove_item_from_cart, OrderSummary, remove_one_item_from_cart, delete_item_from_cart, checkout_view,PaymentView, add_coupon_code, request_refund, search_product, ListOrdersByUser, ListOrderDetailsByUser, ListCurrentOrderDetailsByUser, ListCurrentOrdersByUser, cancel_Order
from django.conf import settings
from django.conf.urls.static import static


app_name = 'ecommerce'

urlpatterns = [
    path('', items_list.as_view(), name="items_list"),
    path('item/<slug>/view', items_detail.as_view(), name="view_item"),
    path('item/<slug>/add_to_cart', add_item_to_cart, name="add_to_cart"),
    path('item/<slug>/remove_to_cart', remove_item_from_cart, name="remove_from_cart"),
    path('order_summary', OrderSummary.as_view(), name='order_summary'),
    path('reduce_item/<slug>', remove_one_item_from_cart, name='reduce_item'),
    path('delete_an_item_from_cart/<slug>', delete_item_from_cart, name='delete_an_item_from_cart'),
    path('checkout', checkout_view.as_view(), name="checkout"),
    path('payment/<payment_option>', PaymentView.as_view(), name="payment"),
    path('add_coupon', add_coupon_code, name="add_coupon"),
    path('request_refund', request_refund.as_view(), name="request_refund"),
    path('search_for_product', search_product.as_view(), name="search_for_product"),
    path('my_past_orders', ListOrdersByUser.as_view(), name="my_past_orders"),
    path('my_past_orders/view_order_details/<int:pk>', ListOrderDetailsByUser, name="my_past_order_details"),
    path('my_current_orders', ListCurrentOrdersByUser.as_view(), name="my_current_orders"),
    path('my_current_orders/view_order_details/<int:pk>', ListCurrentOrderDetailsByUser, name="my_current_order_details"),
    path('my_current_orders/view_order_details/<int:pk>/cancel', cancel_Order, name="my_current_order_cancel"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
