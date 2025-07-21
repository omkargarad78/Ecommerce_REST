from django.urls import path
from .views import PlaceOrderView, UpdateOrderStatusView,MyOrderHistoryView,MyOrderDetailView

urlpatterns = [
    path('place/', PlaceOrderView.as_view(), name='place_order'),
    path('<int:pk>/update-status/', UpdateOrderStatusView.as_view(), name='update_order_status'),

    path('my-orders/', MyOrderHistoryView.as_view(), name='my_orders'),
    path('my-orders/<int:pk>/', MyOrderDetailView.as_view(), name='my_order_detail'),
]
