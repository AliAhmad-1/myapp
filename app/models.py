from django.db import models
import uuid
# Create your models here.

from django.contrib.auth.models import PermissionsMixin,BaseUserManager,AbstractBaseUser

from django.utils import timezone
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
class UserManger(BaseUserManager):
	def _create_user(self,username,email,password,**extra_fields):
		if not username:
			raise ValueError('username is not valid..!')
		email=self.normalize_email(email)
		now=timezone.now()
		user=self.model(username=username,email=email,date_joined=now,**extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_user(self,username,email,password,**extra_fields):
		extra_fields.setdefault('is_active',True)
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username,email,password,**extra_fields)

	def create_superuser(self,username,email,password,**extra_fields):
		extra_fields.setdefault('is_active',True)
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError("superuser  must have is_staff=True")

		if extra_fields.get('is_superuser') is not True:
			raise ValueError("superuser  must have is_superuser=True")
		return self._create_user(username,email,password,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin):

	username=models.CharField(max_length=100,unique=True)
	email=models.EmailField(max_length=100,unique=True)
	first_name=models.CharField(max_length=100,blank=True,null=True)
	last_name=models.CharField(max_length=100,blank=True,null=True)
	phone_number=models.BigIntegerField(blank=True,null=True)
	
	is_active =models.BooleanField(default=True)
	is_superuser=models.BooleanField(default=False)
	is_staff=models.BooleanField(default=False)

	date_joined=models.DateTimeField(default=timezone.now)
	birth_date=models.DateTimeField(blank=True,null=True)

	receive_newsletter=models.BooleanField(default=False)
	city=models.CharField(max_length=100,blank=True,null=True)
	address=models.CharField(max_length=100,blank=True,null=True)
	about_me=models.TextField(max_length=100,blank=True,null=True)
	profile_image=models.ImageField(upload_to='files/',blank=True,null=True)

	objects=UserManger()
	USERNAME_FIELD='username'
	REQUIRED_FIELDS = ['email']


	def __str__(self):
		return self.username







@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )



class Property(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=100,blank=True,null=True)
	sell=models.BooleanField(default=True)
	city=models.CharField(max_length=100,blank=True,null=True)
	region=models.CharField(max_length=100,blank=True,null=True)
	description=models.TextField(blank=True,null=True)
	price=models.BigIntegerField()
	def __str__(self):
		return self.name





class Image(models.Model):
	property_id = models.ForeignKey(
                Property,
				related_name='image',
                null=False,
                default=1,
		
                on_delete=models.CASCADE
            )
	image = models.FileField(upload_to='files/')
	def __str__(self):
		return f"{self.property_id.name}'s media images"





# class Like(models.Model):
#     post = models.ForeignKey(Property, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     like = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Post={self.post.id}||User={self.user.username}||Like={self.like}"



class Favorite(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	item=models.ForeignKey(Property,on_delete=models.CASCADE)

	def __str__(self):
		return self.item.name





