from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderCreateSerializer, OrderDetailSerializer, CustomerReportSerializer
from .services import order_create
from .selectors import order_detail_selector, customer_report_selector

class OrderCreateAPI(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            order = order_create(
                customer_id=serializer.validated_data['customer_id'],
                items=serializer.validated_data['items']
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response_serializer = OrderDetailSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class OrderDetailAPI(APIView):
    def get(self, request, pk):
        try:
            order = order_detail_selector(order_id=pk)
        except Exception:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)

class CustomerReportAPI(APIView):
    def get(self, request, pk):
        try:
            customer = customer_report_selector(customer_id=pk)
        except Exception:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerReportSerializer(customer)
        return Response(serializer.data)
