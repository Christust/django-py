# from apps.base.api import GeneralListAPIView
from apps.products.api.serializers.product_serializer import ProductSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

# ! Se sutituyen por ListCreateAPIView
# class ProductListAPIView(GeneralListAPIView):
#     serializer_class = ProductSerializer


# class ProductCreateAPIView(generics.CreateAPIView):
#     serializer_class = ProductSerializer

# ! Se sustituye por ModelViewSet
# class ProductListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = ProductSerializer
#     queryset = serializer_class.Meta.model.objects.filter(state=True)


# ! Se sustituyen por RetrieveUpdateDestroyAPIView
# class ProductRetrieveAPIView(generics.RetrieveAPIView):
#     serializer_class = ProductSerializer
#     queryset = serializer_class.Meta.model.objects.filter(state=True)


# class ProductDestroyAPIView(generics.DestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = serializer_class.Meta.model.objects.filter(state=True)

#     def delete(self, request, pk):
#         product = self.queryset.filter(id=pk).first()
#         print(product)
#         if product:
#             product.state = False
#             product.save()
#             product_serializer = self.serializer_class(product)
#             return Response(product_serializer.data, status=status.HTTP_200_OK)
#         return Response("No existe el producto", status=status.HTTP_404_NOT_FOUND)


# class ProductUpdateAPIView(generics.UpdateAPIView):
#     serializer_class = ProductSerializer
#     queryset = serializer_class.Meta.model.objects.filter(state=True)

# ! Se sustituye por ModelViewSet
# class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
#     queryset = serializer_class.Meta.model.objects.filter(state=True)

#     def delete(self, request, pk):
#         product = self.queryset.filter(id=pk).first()
#         print(product)
#         if product:
#             product.state = False
#             product.save()
#             product_serializer = self.serializer_class(product)
#             return Response(product_serializer.data, status=status.HTTP_200_OK)
#         return Response("No existe el producto", status=status.HTTP_404_NOT_FOUND)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = serializer_class.Meta.model.objects.filter(state=True)

    def destroy(self, request, pk):
        print("Delete")
        print(self.user)
        product = self.queryset.filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response("No existe el producto", status=status.HTTP_404_NOT_FOUND)
