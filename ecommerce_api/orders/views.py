from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order, OrderItem
from products.models import Product
from .serializers import OrderSerializer
from django.db import transaction
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Websockets
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        items = request.data.get('items', [])

        if not items:
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        order = Order.objects.create(user=user, total_price=0)

        for item in items:
            product_id = item.get('product')
            quantity = item.get('quantity', 1)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({"error": f"Product ID {product_id} not found."}, status=404)

            if product.stock < quantity:
                return Response({"error": f"Insufficient stock for {product.name}"}, status=400)

            price = product.price * quantity
            total_price += price

            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            # Reduce stock
            product.stock -= quantity
            product.save()

        order.total_price = total_price
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


# User can view their own orders
class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

# Admin can view all orders
class AllOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Order.objects.all().order_by('-created_at')
    
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class UpdateOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Order._meta.get_field('status').choices):
            return Response({'error': 'Invalid status'}, status=400)

        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data)
    

# List all orders for current user
class MyOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


# Retrieve a single order for current user
class MyOrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

def patch(self, request, *args, **kwargs):
    order = self.get_object()
    new_status = request.data.get('status')

    if new_status not in dict(Order._meta.get_field('status').choices):
        return Response({'error': 'Invalid status'}, status=400)

    order.status = new_status
    order.save()

    # Send WebSocket notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{order.user.id}",
        {
            'type': 'order_status_update',
            'order_id': order.id,
            'status': order.status,
        }
    )

    return Response(OrderSerializer(order).data)