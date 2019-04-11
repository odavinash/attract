import random
import string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from threading import Thread


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def send_email(email, password):
    t = Thread(target=email_thread, args=(email, password))
    t.start()


def email_thread(email, password):
	#html = get_template('user/verification_email.html')
	subject = 'Your password'

	print(settings.EMAIL_FROM)    
	print(email)
	msg = EmailMultiAlternatives(subject, 'Your password is : ' + password, settings.EMAIL_FROM, [email])
	#msg.attach_alternative(html_content, "text/html")
	result = msg.send()
	print(result)
