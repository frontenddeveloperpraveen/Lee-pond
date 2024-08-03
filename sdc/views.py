# Standard Library Imports
import os

# Django Imports
from django.shortcuts import render, redirect, HttpResponse
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.db.models import Q

# Models and Settings
from .models import Users, Documents,Notifications,Order
from django.conf import settings

# Image Processing
import cv2
import base64
import threading
# Utility Imports
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

#External Custom Imports
from . import Backend
#Codes

# Utility Based Functions



def generate_uidb64_token(user):
    '''
    Type   : Helper 
    Args   : Model of a User
    Job    : Encryt User Model into Base64, Create a Token
    Return : Base64 Encryption & Token
    '''
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk)) 
    token_generator = PasswordResetTokenGenerator() 
    token = token_generator.make_token(user)

    return uidb64, token

#Static Pages 

def Login(request):
    '''
    Type   : HTTP GET Request
    Pupose : Serves Login Page
    Return : Login Page HTML
    '''
    return render(request, "login.html")

class Logout(LogoutView):
    '''
    Type    : HTTP POST Request
    Purpose : Remove the Session and Token to Logout
    Return  : Return to Home Page
    '''
    next_page = reverse_lazy('login')

def ResetPassword(request):
    '''
    Type    : HTTP GET Request
    Purpose : Severs Password reset Page
    Return  : Password Reset 'Forget.html' Page
    '''
    return render(request,"forget.html")

# Request Handelers

def Login_Submit(request):
    '''
    Type    : HTTP POST Request
    ARGS    : Employee ID and Password
    Purpose : Validate the user.
    Return  : Validation True - return Home Page | Validation False - return Error.
    '''
    if request.method == 'POST':
        employeeID = request.POST.get('emp-id')
        Password = request.POST.get('pass')
        User_details = authenticate(request, username=employeeID, password=Password)
        if User_details is not None:
            # User is there in the db
            login(request, User_details)
            request.session['id'] = employeeID
            return redirect('status_screen')
        else:
            # Authentication failed, Returning the error.
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def Form_Submit(request):
    '''
    Type    : HTTP POST Request
    ARGS    : Money and File details
    Purpose : Store the Details to the User DB.
    Return  : Success - Return to Success Page | False - return Error in Server Log.
    '''
    if request.method == 'POST':
        #Form submission
        # Yet to work
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
            email=email,  
            emp_id=emp_id,  
            name=name 
        )

        # Return a response
        return render(request,'success.html')
    else:
        return HttpResponse("UnAuthorised Response")
    
#Main Routes
#  Home
@login_required
def pppp(request):
    '''
    Type    : HTTP GET Request
    ARGS    : Session Token (@login_required)
    Purpose : Fetch the details of the User and display.
    Return  : Success - Return to Home Page | False - return Error in Server Log.
    '''
    employee_id = request.session.get('id')
    User_details = User.objects.filter(username=employee_id).first()
    if User_details:
        first_name = User_details.first_name
        last_name = User_details.last_name
        date_of_joining = User_details.date_joined.strftime("%Y-%m-%d")
        email = User_details.email
        Info = Users.objects.filter(user__username=employee_id).first()
        if Info:
            designation = Info.designation
            pan_number = Info.pan
            emp_type = Info.employee_type
            school = Info.school
            name = f"{first_name} {last_name}"
            UAN_no = Info.uan_no
            img_b64_string = None
            if Info.image:
                try:
                    # Assuming img_path is the path to the image file
                    img = cv2.imread(Info.image.path)
                    if img is not None:
                        _, buffer = cv2.imencode('.jpg', img)
                        img_b64_string = base64.b64encode(buffer).decode('utf-8')
                except Exception as e:
                    # Handle the exception gracefully
                    print(f"Error processing image: {e}")
            response = {
                "name": name,
                "email": email,
                "empid": employee_id,
                "designation": designation,
                "panno": pan_number,
                "emptype": emp_type,
                "school": school,
                "image": img_b64_string,
                'uanno':UAN_no,
                'doj':date_of_joining,
            }
            return render(request, 'portal.html', response)
    # Handle the case when user or user Info not found
    return redirect("login")

@login_required
def Page1(request):
    return render(request, "pages/index.html")

@login_required
def Home(request):
    print("served - Inital Home")
    return render(request,"pages/initial.html")

#  Forget Password
def Reset_Password_Link(request, uidb64, token):
    '''
    Type    : HTTP GET & POST Request
    ARGS    : Base64 String, Token
    Purpose : Decrupt and Validate the token.
    Return  : Success - Return to Change Password Page | False - Return HTTPResponse stating Invalid Token.
    '''
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # Checking if the user exists and the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-password')
            if new_password == confirm_password:
                try:
                    validate_password(new_password)
                except ValidationError as error:
                    return render(request, 'PasswordReset.html', {'error': error})
                else:
                    # Setting the new password for the user
                    user.set_password(new_password)
                    user.save()
                    print("Password Changed Successfull")
                    logout(request)
                    return render(request,"login.html",{'success':'Password Changed Successfully'})
            else:
                # If passwords don't match
                return render(request, 'PasswordReset.html', {'error': 'Passwords do not match'})

        else:
            # If it's a GET request
            return render(request, 'PasswordReset.html')

    else:
        # If user or token is invalid
        return HttpResponse("Token Invalid")

#Forget Password 
def Forget_Password(request, template_name='Forget.html'):
    '''
    Type    : HTTP GET Request
    ARGS    : None
    Purpose : 1. Serves the Forget.html Page.
              2. Validate the Employee ID.
              3. Sending Email
    Return  : Validation Success - Send Email to respective User's email ID | Failed - return Error.
    '''
    if request.method == 'POST':
        userid = request.POST.get("emp-id")
        print(userid)
        if User.objects.filter(username=userid).exists():
            # User exists, proceed with password reset
            user = User.objects.get(username=userid)
            email = user.email
            print(email)
            # Generate password reset token and send email
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
            return render(request,"Forget.html",{'error':"No User Found"})
    return render(request, template_name)


# Admin Side Rotes Media Download

@login_required
def Media_Download(request, file_path):
    '''
    Type    : HTTP POST Request
    ARGS    : Session Token (@login_required) Only Superuser
    Purpose : Download the File.
    Return  : Success - Send the File | False - return Error in Server Log.
    '''
    full_path = os.path.join(settings.BASE_DIR, '/My Projects - GIGS/Delievery Patner', file_path)
    if request.user.is_authenticated and request.user.is_superuser:
        print(full_path,"---> ful")
        if os.path.exists(full_path):
            # Serve the file as an attachment
            return FileResponse(open(full_path, 'rb'), as_attachment=True)
        else:
            return HttpResponse("File not found", status=404)
    else:
        # Return forbidden error if the user is not authenticated or not a superuser
        return HttpResponseForbidden("You do not have permission to access this file.")


# APIS CALL
@login_required
def Base_Page(request):
    try:
        employee_id = request.session.get('id')
        name = User.objects.filter(username=employee_id).first()
        username = name.first_name + " " + name.last_name
        name = name.first_name + "-"+ str(employee_id)
        notifications = Notifications.objects.filter(
            Q(User_id__username=employee_id) | Q(publish_type="broadcast")
        )
        last_id = notifications.last()
        orders = Order.objects.filter(Assigned_to__username=employee_id)
        ongoing_orders = orders.filter(Q(status="picked") | Q(status="accepted"))
        pending_orders = orders.filter(status="assigned")
        print("pending --> home",pending_orders,ongoing_orders)
        print(last_id)
        try:
            notifi = request.session.get('notifications')
            if(notifi <= last_id.id):
                ans = (last_id.id - notifi)
                print('sxhjgshb',ans)
                return render(request,"pages/base.html",{"username":username,"notification":ans,"ongoing_orders":ongoing_orders,"pending_orders":pending_orders})
            else:
                raise Exception
        except Exception as e:
            return render(request,"pages/base.html",{"username":username,"notification":len(notifications),"ongoing_orders":ongoing_orders,"pending_orders":pending_orders})
        
    except:
        return redirect("login")
@login_required
def Notification_api(request):
    print("hi")
    employee_id = request.session.get('id')
    notifications = Notifications.objects.filter(
        Q(User_id__username=employee_id) | Q(publish_type="broadcast")
    )
    try:
        request.session['notifications'] = notifications.last().id
    except: pass
    return render (request,"routes/Notification.html",{'notify':notifications.order_by('-id')})
    
@login_required
def Profile_api(request):
    employee_id = request.session.get('id')
    user = User.objects.filter(username=employee_id).first() 
    email, doj = user.email , user.date_joined
    firstname , lastname = user.first_name,user.last_name
    user = Users.objects.filter(user__username = employee_id).first()
    print("final usrr -> ",user)
    aadhar , plate , emp_type ,city , dob, img,language ,age,mob=  user.aadhar, user.plate, user.employee_type,user.city,user.created_at, user.image,user.language,user.age,user.mobile_number
    print('img ---> ',img)
    img_b64_string = None
    if img:
        try:
            # Assuming img_path is the path to the image file
            img = cv2.imread(img.path)
            if img is not None:
                _, buffer = cv2.imencode('.jpg', img)
                img_b64_string = base64.b64encode(buffer).decode('utf-8')
        except Exception as e:
            # Handle the exception gracefully
            print(f"Error processing image: {e}")

    return render (request,"routes/Profile.html",{'firstname':firstname,"lastname":lastname,"email":email,"doj":doj,"emp_id":employee_id,"aadhar":aadhar,"plate":plate,"emp":emp_type,"dob":dob,"dp":img_b64_string,"city":city,'language':language,"age":age,"mob":mob})
    
@login_required
def Orders_api(request):
    employee_id = request.session.get('id')
    orders = Order.objects.filter(Assigned_to__username=employee_id)
    ongoing_orders = orders.filter(Q(status="picked") | Q(status="accepted"))
    pending_orders = orders.filter(status="assigned")
    context = {
        "ongoing_orders": ongoing_orders,
        "pending_orders": pending_orders,
    }
    return render(request, "routes/Order.html", context)
@login_required
def Home_api(request):
    employee_id = request.session.get('id')
    name = User.objects.filter(username=employee_id).first()
    username = name.first_name + " " + name.last_name
    notifications = Notifications.objects.filter(
        Q(User_id__username=employee_id) | Q(publish_type="broadcast")
    )
    last_id = notifications.last()
    orders = Order.objects.filter(Assigned_to__username=employee_id)
    ongoing_orders = orders.filter(Q(status="picked") | Q(status="accepted"))
    pending_orders = orders.filter(status="assigned")
    print("served")
    try:
        notifi = request.session.get('notifications')
        print("Notify -> last id stored ",notifi)
        print("Real last id -> ",last_id.id)
        if(notifi <= last_id.id):
            ans = (last_id.id - notifi)
            return render(request,"routes/Home.html",{"username":username,"notification":ans,"ongoing_orders":ongoing_orders,"pending_orders":pending_orders})
        else:
            raise Exception
    except Exception as e:
        print(e)
        return render(request,"routes/Home.html",{"username":username,"notification":len(notifications),"ongoing_orders":ongoing_orders,"pending_orders":pending_orders})


# Sub Api Order Route
@login_required
def Order_switch(request, route):
    employee_id = request.session.get('id')
    orders = Order.objects.filter(Assigned_to__username=employee_id)

    if route == "past":
        orders_list = orders.exclude(status__in=["picked", "accepted","assigned"])
        context = {
            "past_orders": orders_list,
            "state_for": "past"
        }
    elif route == "pending":
        ongoing_orders = orders.filter(Q(status="picked") | Q(status="accepted"))
        pending_orders = orders.filter(status="assigned")
        context = {
            "ongoing_orders": ongoing_orders,
            "pending_orders": pending_orders,
            "state_for": "pending"
        }
    return render(request, "routes/Order_State.html", context)


@login_required
def Perticular_Order(request,param):
    set_list = param.split(",")
    if(len(set_list) == 4):
        state , orderno , latitude,longitude = set_list
    elif(len(set_list) == 2):
        state , orderno = set_list
    
    title = 'Accept the Order'
    now = "inital"
    print("State ---> ",state ,"Orderno ----> ",orderno)
    employee_id = request.session.get('id')
    orders = Order.objects.filter(order_no = orderno).first()
    if(orders.Assigned_to.username == employee_id):
        pickup,drop,cust_addr , hotel_addr, cust_name, hotel_name, note,cust_number,hotel_number  =  orders.Shop_Location,orders.Delievery_Location,orders.delievery_addr,orders.hostel_addr,orders.customer_name,orders.hotel_name,orders.note,orders.customer_number,orders.hotel_number
        Dest_lat , Dest_long = Backend.extract_coordinates(pickup)
        if(orders.distance == "will be calculated shortly"):
            orders.route1 = Backend.getDirection_(latitude,longitude,Dest_lat,Dest_long)
            orders.Current_Location = Backend.generate_map_link(latitude,longitude)
            d1,d2 = Backend.extract_coordinates(drop)
            orders.route2 = Backend.getDirection_(Dest_lat,Dest_long,d1,d2 )
            threading.Thread(target=Backend.Distance, args=(orderno,employee_id)).start()
        if(state == "accepted"):
            title = "Picked the Food"
            orders.status = 'accepted'
            orders.route1 = Backend.getDirection_(latitude,longitude,Dest_lat,Dest_long)
            now = "picked"
            orders.Current_Location = Backend.generate_map_link(latitude,longitude)
            d1,d2 = Backend.extract_coordinates(drop)
            orders.route2 = Backend.getDirection_(Dest_lat,Dest_long,d1,d2 )
            threading.Thread(target=Backend.Distance, args=(orderno,employee_id)).start()
        elif(state == "picked"):
            title = "Delivered the Food"
            orders.status = "picked"
            now = "delievered"
            latitude , longitude = Dest_lat,Dest_long
            Dest_lat,Dest_long = Backend.extract_coordinates(drop) 
            orders.route2 = Backend.getDirection_(latitude,longitude,Dest_lat,Dest_long)
        elif(state == "delievered"):
            orders.status = "delievered"
            title = "Ordered Completed"
            now = "closed"
            current_location = orders.Current_Location
            latitude,longitude = Backend.extract_lat_long(current_location) 
            Dest_lat,Dest_long = Backend.extract_coordinates(drop)
        orders.save()
        return render(request,"routes/Order_details.html",{"orderno":orderno,"status":orders.status.title(),"c_lat":latitude,"c_long":longitude,"d_lat":Dest_lat,"d_long":Dest_long,"title":title,"cname":cust_name,"hotel_name":hotel_name,"c_addr":cust_addr,"h_addr":hotel_addr,"c_no":cust_number,"h_no":hotel_number,"note":note,"now":now})
    else:
        return HttpResponse(500,"Wrong Order Number")
    

@login_required
def UserActivity(request,state):
    employee_id = request.session.get('id')
    users = Users.objects.filter(user__username = employee_id).first()
    print(state)
    if(state == "active"):
        users.is_online = True
    else:
        users.is_online = False
    users.save()
    return HttpResponse("Response Noted")