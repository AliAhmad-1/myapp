from django.contrib import admin
from app.models import User,Property,Image,Favorite

# Register your models here.



class UserAdmin(admin.ModelAdmin):
	list_display=['id','username','email']
admin.site.register(User,UserAdmin)
admin.site.register([Image,Property,Favorite])


