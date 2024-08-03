# Create your models here.
import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import  UserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
import datetime
from random import randint


class UserQuerySet(models.QuerySet):
    def delete(self):
        for instance in self:
            instance.delete()
        super().delete()

class EditUser(User):
    class Meta:
        proxy = True
    def __str__(self):
        return f"{self.first_name} - {self.username}"

class Users(models.Model):
    user = models.ForeignKey(EditUser, on_delete=models.CASCADE,limit_choices_to={'is_superuser': False})
    choice = (('Permanent',"Permanent"),("Temporary","Temporary"))
    age = models.CharField(max_length=2,null=False,blank=False,default="")
    image = models.ImageField(upload_to='user_images/',default="user_images/User/blank.png") 
    city = models.CharField(max_length=100, blank=False, null=False)
    aadhar = models.CharField(max_length=100, blank=False, null=False)
    plate = models.CharField(max_length=100,blank=False,null=False)
    employee_type = models.CharField(max_length=100, choices=choice, blank=False, null=False)
    language = models.CharField(max_length=200,blank=False,null=False,help_text="Language the user knows, Seperate by commas",default="Tamil")
    mobile_number = models.CharField(max_length=10,blank=False,null=False)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserQuerySet.as_manager()

    def delete(self, *args, **kwargs):
    # Delete associated files before deleting the instance
        for field in ['image']:
            file_field = getattr(self, field)
            if file_field:
                print(file_field)
                if os.path.isfile(file_field.path):
                    os.remove(file_field.path)
        super().delete(*args, **kwargs)


def document_upload_path(instance, filename):
    # Define the upload path for each file
    return os.path.join("media/"+instance.name + '_' + instance.emp_id, filename)

class DocumentQuerySet(models.QuerySet):
    def delete(self):
        for instance in self:
            instance.delete()
        super().delete()

class Documents(models.Model):
    email = models.EmailField(blank=False, null=False)
    emp_id = models.CharField(blank=False, null=False, max_length=100)
    name = models.CharField(max_length=100, blank=False, null=False)
    house_rent = models.IntegerField(blank=False, null=False)
    house_file = models.FileField(upload_to=document_upload_path, blank=False, null=False)
    fees = models.IntegerField(blank=False, null=False)
    fees_file = models.FileField(upload_to=document_upload_path, blank=False, null=False)
    travelling = models.IntegerField(blank=False, null=False)
    travelling_file = models.FileField(upload_to=document_upload_path, blank=False, null=False)
    bus = models.IntegerField(blank=False, null=False)
    bus_file = models.FileField(upload_to=document_upload_path, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = DocumentQuerySet.as_manager()

    def delete(self, *args, **kwargs):
        # Delete associated files before deleting the instance
        for field in ['house_file', 'fees_file', 'travelling_file', 'bus_file']:
            file_field = getattr(self, field)
            if file_field:
                print(file_field)
                if os.path.isfile(file_field.path):
                    os.remove(file_field.path)
        super().delete(*args, **kwargs)
        # Delete folder
        folder_path = os.path.join('media', f"{self.name}_{self.emp_id}")
        if os.path.exists(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)

class Order((models.Model)):
    choice= (("assigned","Assigned"),("accepted","Accepted"),("picked","Picked"),("delievered","Delievered"),("cancelled_by_admin","Cancelled by Admin"),("cancelled_by_boy","Cancelled by Delievery Boy"),)
    Assigned_to = models.ForeignKey(
        EditUser,
        on_delete=models.CASCADE, 
    )
    order_no = models.CharField(max_length=30,null=False,blank=False,default="Automatically Update")
    customer_name = models.CharField(max_length=30, null=False,blank=False)
    delievery_addr = models.TextField(max_length=200,null=False,blank=False)
    hotel_name = models.CharField(max_length=30,null=False,blank=False)
    hostel_addr = models.TextField(max_length=200,null=False,blank=False)
    note = models.TextField(max_length=100)
    customer_number = models.CharField(help_text="Customer Mobile Number",blank=False,null=False,max_length=10)
    hotel_number = models.CharField(help_text="Hotel Mobile Number",blank=False,null=False,max_length=10)
    Shop_Location = models.URLField(null=False,blank=False,max_length=100)
    Delievery_Location = models.URLField(null=False,blank=False,max_length=100)
    status = models.TextField(choices=choice,max_length=100,blank=False,null=False,default='assigned')
    Current_Location = models.URLField(null=False,blank=False,max_length=100, default="Fetch Automatically")
    distance = models.TextField(null=False,blank=False, default="will be calculated shortly",max_length=10)
    route1 = models.URLField(null=False,blank=False,default="Will be updated",max_length=100)
    duration1 = models.CharField(max_length=10,blank=False,null=False,default="Update Automatically")
    distance1 = models.CharField(max_length=10,blank=False,null=False,default="Update Automatically")
    route2 = models.URLField(null=False,blank=False,default="Will be updated",max_length=100)
    duration2 = models.CharField(max_length=10,blank=False,null=False,default="Update Automatically")
    distance2 = models.CharField(max_length=10,blank=False,null=False,default="Update Automatically")
    date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.order_no == "Automatically Update":
            while True:
                order_id = str(randint(1000000000, 9999999999))
                if not Order.objects.filter(order_no=order_id).exists():
                    self.order_no = order_id
                    break
    def clean(self):
        if self.pk is not None:  # Check if the instance is being updated
            old_instance = Order.objects.get(pk=self.pk)
            print('Old --> ',old_instance.status)
            if old_instance.status in ["delievered", "cancelled_by_admin", "cancelled_by_boy"]:
                print("yes shoudl not be changeed")
                if self.Assigned_to != old_instance.Assigned_to:
                    raise ValidationError("You cannot change the Assigned_to field when the order is delivered or cancelled.")
    def save(self, *args, **kwargs):
        if self.order_no == "Automatically Update":
            while True:
                order_id = str(randint(1000000000, 9999999999))
                if not Order.objects.filter(order_no=order_id).exists():
                    self.order_no = order_id
                    break
        self.clean()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_no}"
    
class Notifications(models.Model):
    User_id = models.ForeignKey(
        EditUser,
        on_delete=models.CASCADE,
    )
    choice = (("unicast","Send to Perticular One"),("broadcast","Broadcast to all Members"),)
    publish_type = models.TextField(choices=choice,max_length=60,default="unicast")
    title = models.CharField(max_length=60,default="Message from Admin",blank=False,null=False)
    message = models.TextField(max_length=200,blank=False,null=False)
    created_at = models.DateTimeField(auto_now=True)



    
