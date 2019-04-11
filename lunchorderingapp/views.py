from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import generics
from lunchorderingapp import serializers
from lunchorderingapp import models
from rest_framework import status
from django.template import loader 
from django.http import HttpResponse 


# Create your views here.

def index(request):  
	template = loader.get_template('lunchorderingapp/index.html') # getting our template  
	return HttpResponse(template.render())       # rendering the template in HttpResponse  

def product(request):  
	template = loader.get_template('lunchorderingapp/product.html') # getting our template  
	return HttpResponse(template.render())       # rendering the template in HttpResponse  

class Login(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.get_data()
            return Response({"status": 200, 'message': 'success', 'success': True, 'data': data})
        except Exception as e:
            return Response ({"status": 400, "message" : "Authentication fail"}, status=status.HTTP_400_BAD_REQUEST)


class Product(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = (IsAuthenticated,)
    model = models.Product

    def get_queryset(self):
        try:
            page = self.kwargs['page']
            start = ((page - 1)*10)
            end = start + 10
            
            return self.model.objects.all().order_by('-product_id')[start:end]
        except self.model.DoesNotExist:
        	return None

    def list(self, request, *args, **kwargs):
        try:
            total = self.model.objects.count()
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response({"data": serializer.data, "recordsTotal": total,
  "recordsFiltered": total})
        except Exception as e:
        	print(e)
        	return Response ({"status": 400, "message" : "Failure to fetch products"}, status=status.HTTP_400_BAD_REQUEST)


class Order(generics.CreateAPIView):
    serializer_class = serializers.OrderSerializer
    permission_classes = (IsAuthenticated,)
    model = models.Order

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            return Response ({"status": 200, "message" : 'Order add successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
        	print(e)
        	return Response ({"status": 400, "message" : "Failure- add order."}, status=status.HTTP_400_BAD_REQUEST)
