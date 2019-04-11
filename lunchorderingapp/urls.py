from django.urls import path
from lunchorderingapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'lunchorderingapp'

urlpatterns = [
	path('', views.index),
	path('product', views.product),
	path("login", views.Login.as_view(), name="login"),
	path("get-products/<int:page>", views.Product.as_view(), name="get-products"),
	path("add-order", views.Order.as_view(), name="add-order"),
]

