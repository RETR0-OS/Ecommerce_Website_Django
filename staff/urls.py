from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import staff_home, staff_login, delivery_staff_view_pending_orders, delivery_staff_search_pending_orders, delivery_staff_view_pending_refunds, delivery_staff_search_pending_refunds, preprocessing_staff_view_pending_preprocessings, preprocessing_staff_search_pending_preprocessings, ListPendingPreprocessingOrderDetails

app_name = 'staff'

urlpatterns = [
    path('', staff_home, name="staff_home"),
    path('staff_login/', staff_login.as_view(), name="staff_login"),
    path('delivery_staff/pending_orders', delivery_staff_view_pending_orders.as_view(), name="pending_orders"),
    path('delivery_staff/pending_refunds', delivery_staff_view_pending_refunds.as_view(), name="pending_refunds"),
    path('delivery_staff/pending_orders/search', delivery_staff_search_pending_orders.as_view(), name="search_pending_orders"),
    path('delivery_staff/pending_refunds/search', delivery_staff_search_pending_refunds.as_view(), name="search_pending_refunds"),
    path('preprocessing_staff/pending_preprocessing', preprocessing_staff_view_pending_preprocessings.as_view(), name="pending_preprocessing"),
    path('delivery_staff/pending_preprocessing/search', preprocessing_staff_search_pending_preprocessings.as_view(), name="search_pending_preprocessings"),
    path('delivery_staff/pending_preprocessing/view_details/<int:pk>', ListPendingPreprocessingOrderDetails, name="pending_preprocessing_order_details"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
