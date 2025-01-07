from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
    def update_quantity(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            new_quantity = request.data.get('quantity')
            if new_quantity is None:
                return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
            product.quantity = int(new_quantity)
            product.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
