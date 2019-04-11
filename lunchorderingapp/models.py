from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
import xlrd
from collections import OrderedDict
import simplejson as json
import uuid
import os
from django.contrib.auth import get_user_model
from lunchordering.utils import randomString, send_email
from django.utils import timezone


# Create your models here.

def get_upload_import_path(instance, filename):
    return os.path.join('excel', '', '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1]))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	class Meta:
		db_table = "user"

	email = models.EmailField(unique=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
	last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)
	is_staff = models.BooleanField(
	    _('staff status'),
	    default=False,
	    help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
	    _('active'),
	    default=False,
	    help_text=_('Designates whether this user should be treated as active. '),
	)

	USERNAME_FIELD = 'email'
	objects = UserManager()

	def __str__(self):
	    return f'{self.first_name}'


class ImportUser(models.Model):
	class Meta:
		db_table = "import_user"

	import_path = models.FileField(upload_to=get_upload_import_path, help_text='excel file', blank=True, default='')

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		
		import_path = self.import_path.url[1:]
		wb = xlrd.open_workbook(import_path)
		sh = wb.sheet_by_index(0)
		user_list = []
		
		for rownum in range(1, sh.nrows):
		    depreciation = OrderedDict()
		    row_values = sh.row_values(rownum)
		    pwd = randomString(8)
		    
		    get_user_model().objects.create_user(first_name=row_values[0],
                                                    last_name=row_values[1],
                                                    email=row_values[2],
                                                    password=pwd)
		    send_email(row_values[2], pwd)


class Product(models.Model):

    class Meta:
        db_table = "product"

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, null=False)
    company_name = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False, default=0)
    
    def __str__(self):
        return self.product_name


class Order(models.Model):
    class Meta:
        db_table = "order"

    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    date = models.DateTimeField('date', null=False, default=timezone.now)