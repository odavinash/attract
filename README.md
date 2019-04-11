#### Dependencies

* Create virtualenv:
 	virtualenv -p python3 envname 
 	pip install -r requirements.txt


#### Database Access
MySQL could be access 



#### Configure Email in settings.py
* EMAIL_USE_TLS = True
* EMAIL_HOST = 'smtp.gmail.com'
* EMAIL_HOST_USER = '*****@gmail.com'
* EMAIL_HOST_PASSWORD = '**********'
* EMAIL_PORT = 587
* EMAIL_FROM = 'Attract <no-reply@*****@gmail.com>'
 

#### Admin User
* Create Admin user
	python manage.py createsuperuser


#### Import User
* Go to admin and click on Import Users
* Click on "ADD IMPORT USER"
* Select file and click on save

#### Open API
http://localhost:8000/api

#### Open Frontend
http://localhost:8000
* Enter username and password
* If login success than it will redirect to product list page
* On click on order button user order will be add 
