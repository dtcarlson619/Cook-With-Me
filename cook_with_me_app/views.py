from django.shortcuts import render, redirect
from .models import UserManager, User, Chef,RestaurantManager, Restaurant, Course 
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def loginPage(request):
    return render(request, "login_reg.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="register")
            return redirect("/login")
        else:
            restaurant_manager = request.POST["restaurant_manager"]
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(restaurant_manager=restaurant_manager, first_name=first_name, last_name=last_name, email=email, password=pw_hash)
            request.session["userid"] = user.id
            login = User.objects.get(email=request.POST["email"])
            if login.restaurant_manager == False:
                return redirect("/bookings")
            else:
                return redirect("/restaurant/new")

def login(request):
    if request.method == "POST":
        errors = User.objects.loginCheck(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="login")
            return redirect("/login")
        else:
            login = User.objects.get(email=request.POST["email"])
            context = {
                "user": login,
            }
            request.session["userid"] = login.id
            if login.restaurant_manager == False:
                return redirect("/bookings")
            else:
                return redirect("/restaurant/new")
            

def logout(request):
    try:
        del request.session["userid"]
        return redirect("/")
    except:
        return redirect("/")

def bookings(request):
    context = {
        "all_courses": Course.objects.all(),
        "user": User.objects.get(id=request.session['userid'])
    }
    return render(request, "bookings.html", context)    

# def restaurantEdit(request, user_id):
#     context = {
#         "user": User.objects.get(id=request.session['userid']),
#         "restaurant": Restaurant.objects.get(id=user_id),
#     }
#     return render(request, "restaurant_edit.html", context)

def newRestaurant(request):
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "course": Course.objects.all(),
    }
    return render(request, "restaurant_new.html", context)

def restaurantCreate(request):
    errors = Restaurant.objects.basic_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/restaurant/new")
        else:
            name = request.POST["name"]
            city = request.POST["city"]
            state = request.POST["state"]
            street = request.POST["street"]
            description = request.POST["description"]
            newRestaurant = Restaurant.objects.create(name=name, city=city, state=state, street=street, description=description)
            return redirect("/bookings")

def restaurant(request, course_id):
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "restaurant": Restaurant.objects.get(id=course_id),
    }
    return render(request, "restaurant.html", context)