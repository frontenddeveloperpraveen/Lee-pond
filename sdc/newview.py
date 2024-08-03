# views.py
import os
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, FileResponse,HttpResponseForbidden,JsonResponse
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Users, Documents
from django.conf import settings
import cv2
import base64
import json
from django.http import HttpResponse, FileResponse
from urllib.parse import unquote
from django.contrib.auth import logout
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def generate_uidb64_token(user):
    # Encode the user's primary key to base64
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    # Generate the token
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)

    return uidb64, token

#token gen
#done



def Login(request):
    return render(request, "login.html")

class Logout(LogoutView):
    next_page = reverse_lazy('Home')

# Done
# Login Done
def login_view(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp-id')
        password = request.POST.get('pass')
        user = authenticate(request, username=emp_id, password=password)
        if user is not None:
            login(request, user)
            request.session['id'] = emp_id
            return redirect('Home')
        else:
            # Authentication failed, handle error or redirect to login again
            print("Wromg cred")
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
# Home Done
@login_required
def Home(request):
    emp_id = request.session.get('id')
    user_det = User.objects.filter(username=emp_id).first()
    if user_det:
        first_name = user_det.first_name
        last_name = user_det.last_name
        email = user_det.email
        details = Users.objects.filter(user__username=emp_id).first()
        if details:
            designation = details.designation
            pan_number = details.pan
            emp_type = details.employee_type
            school = details.school
            name = f"{first_name} {last_name}"
            img_b64_string = None
            if details.image:
                try:
                    # Assuming img_path is the path to the image file
                    img = cv2.imread(details.image.path)
                    if img is not None:
                        _, buffer = cv2.imencode('.jpg', img)
                        img_b64_string = base64.b64encode(buffer).decode('utf-8')
                except Exception as e:
                    # Handle the exception gracefully
                    print(f"Error processing image: {e}")
            response = {
                "name": name,
                "email": email,
                "empid": emp_id,
                "designation": designation,
                "panno": pan_number,
                "emptype": emp_type,
                "school": school,
                "image": img_b64_string
            }
            return render(request, 'portal.html', response)
    # Handle the case when user or user details not found
    return redirect("login")


# Subkit done
def Submit(request):
    if request.method == 'POST':
        # Handle form submission
        house_price = request.POST.get('house-price')
        house_file = request.FILES.get('house-file')

        fees_price = request.POST.get("fees-price")
        fees_file = request.FILES.get('fees-file')

        travelling_price = request.POST.get("travel-price")
        travelling_file = request.FILES.get("travel-file")

        bus_fees = request.POST.get('bus-price')
        bus_file = request.FILES.get('bus-file')
        
        # Save form data to the database
        emp_id = request.session['id'] 
        info = User.objects.filter(username=emp_id).first()
        email = info.email
        name = info.first_name + " " + info.last_name
        document = Documents.objects.create(
            house_rent=house_price,
            house_file=house_file,
            fees=fees_price,
            fees_file=fees_file,
            travelling=travelling_price,
            travelling_file=travelling_file,
            bus=bus_fees,
            bus_file=bus_file,
            email=email,  # Assuming user is logged in
            emp_id=emp_id,  # Assuming user has emp_id attribute
            name=name  # Assuming user has name attribute
        )

        # Process or save the files

        # Return a response
        return render(request,'success.html')
    else:
        # Handle GET request (if needed)
        return HttpResponse("This view only accepts POST requests")
    


@login_required
def serve_file(request, file_path):
    # Construct the full file path
    full_path = os.path.join(settings.BASE_DIR, '/SDC/', file_path)

    # Check if the user is authenticated and is a superuser
    if request.user.is_authenticated and request.user.is_superuser:
        # Check if the file exists
        if os.path.exists(full_path):
            # Serve the file as an attachment
            return FileResponse(open(full_path, 'rb'), as_attachment=True)
        else:
            return HttpResponse("File not found", status=404)
    else:
        # Return forbidden error if the user is not authenticated or not a superuser
        return HttpResponseForbidden("You do not have permission to access this file.")
    
# Done
def ResetPassword(request):
    return render(request,"forget.html")
# Done
# Reset password

# reset pass - done
# Done
def reset_password(request, uidb64, token):
    try:
        # Decode the uidb64 to get the user's id
        uid = urlsafe_base64_decode(uidb64).decode()
        # Get the user model
        User = get_user_model()
        # Get the user by id
        print(User)
        user = User.objects.get(pk=uid)
        print(user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the user exists and the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # If it's a POST request, process the form
            new_password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-password')
            
            if new_password == confirm_password:
                try:
                    validate_password(new_password)
                except ValidationError as error:
                    return render(request, 'PasswordReset.html', {'error': error})
                else:
                    # Set the new password for the user
                    user.set_password(new_password)
                    user.save()
                    print("Password Changed Successfull")
                    # Redirect to password reset complete page
                    logout(request)
                    return render(request,"login.html",{'success':'Password Changed Successfully'})
            else:
                # If passwords don't match, render the form with an error message
                return render(request, 'PasswordReset.html', {'error': 'Passwords do not match'})

        else:
            # If it's a GET request, render the password reset form
            return render(request, 'PasswordReset.html')

    else:
        # If user or token is invalid, render an error page or redirect as needed
        return HttpResponse("Token Invalid")
    


# Done
def custom_password_reset(request, template_name='Forget.html'):
    if request.method == 'POST':
        userid = request.POST.get("emp-id")
        print(userid)
        if User.objects.filter(username=userid).exists():
            # User exists, proceed with password reset
            user = User.objects.get(username=userid)
            email = user.email
            print(email)
            # Generate password reset token and send email
            # You may need to customize the domain and URL to match your project's settings
            uidb64,token = generate_uidb64_token(user)
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_url}',
                'course.bytecamp@gmail.com',
                [email],
                fail_silently=False,
            )
            return render(request,"Forget.html",{'success':"Email Sent Successfully. Follow the instruction to reset Password."}) # Redirect to password reset done page
        else:
            # User doesn't exist, redirect to a different page or show an error message
            # For example, you could redirect to a page indicating that the email is not registered
            return render(request,"Forget.html",{'error':"No User Found"})  # Redirect to email not registered page
    return render(request, template_name)
