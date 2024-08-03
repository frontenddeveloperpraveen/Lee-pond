from django import forms
from .models import Order, EditUser, Users

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Fetch all EditUser instances
        users = EditUser.objects.filter(is_superuser=False)
        # Update queryset with status
        self.fields['Assigned_to'].queryset = users
        self.fields['Assigned_to'].label_from_instance = lambda obj: f"{obj.username} - {obj.first_name} ({'Online' if Users.objects.filter(user=obj, is_online=True).exists() else 'Offline'})"
