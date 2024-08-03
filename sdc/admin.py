from django.contrib import admin
from .models import Documents,Users,EditUser,Order,Notifications,User
from random import randint
from django.db import models
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime

admin.site.site_header = 'Admin | Patner Portal'                    
admin.site.index_title = 'Database'                
admin.site.site_title = 'Admin | Company Name'

from .Forms import OrderForm

class YearFilter(admin.SimpleListFilter):
    title = _('Year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = Order.objects.dates('date', 'year')
        return [(year.year, year.year) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date__year=self.value())
        return queryset

class MonthFilter(admin.SimpleListFilter):
    title = _('Month')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        months = Order.objects.dates('date', 'month')
        return [(month.month, month.strftime('%B')) for month in months]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date__month=self.value())
        return queryset

class DayFilter(admin.SimpleListFilter):
    title = _('Day')
    parameter_name = 'day'

    def lookups(self, request, model_admin):
        days = Order.objects.dates('date', 'day')
        return [(day.day, day.day) for day in days]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(date__day=self.value())
        return queryset  

class OrderInfo(admin.ModelAdmin):
    form = OrderForm  # Use the custom form

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['Assigned_to'].queryset = EditUser.objects.filter(users__is_online=True)
        return form

    list_display = ("order_no","status","Assigned_to","distance","customer_name","hotel_name")
    search_fields = ("Assigned_to","order_no","customer_name",'hotel_name',)
    list_filter = ("status","Assigned_to",YearFilter, MonthFilter, DayFilter)
    readonly_fields = ("order_no","Current_Location",'distance',"route1","route2","distance2","duration2","distance1","duration1","date")

class DocumentProduct(admin.ModelAdmin):
    list_display = ('name','emp_id','email')
    search_fields = ['name','emp_id','email']
    list_filter = ['name']
    readonly_fields = ('name','emp_id','email','bus_file','bus','travelling_file','travelling','fees_file','fees','house_file','house_rent')

class UsersProduct(admin.ModelAdmin):
    list_display = ('name','user',"employee_type","plate")
    search_fields = ('designation',"employee_type","plate")
    list_filter = ['user']
    readonly_fields = ("is_online",)
    def name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

class NotificationsInfo(admin.ModelAdmin):
    list_display = ('User_id','title',"publish_type")
    search_fields = ("title","publish_type")
    list_filter = ["User_id"]

# Register your models here.
admin.site.register(Documents,DocumentProduct)
admin.site.register(Users,UsersProduct)
admin.site.register(Order,OrderInfo)
admin.site.register(Notifications,NotificationsInfo)
