from django.contrib import admin
from django.contrib.auth import get_user_model
from lunchorderingapp import models


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active', 'is_staff',)
    search_fields = ('first_name',)


@admin.register(models.ImportUser)
class ImportUserAdmin(admin.ModelAdmin):
    list_display = ('import_path',)
 

@admin.register(models.Product)
class ImportUserAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'company_name', 'price',)
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id',)
    