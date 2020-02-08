from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email address!"
        users = self.filter(email=postData["email"])
        if users:
            errors["email"] = "Email already exists"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData["password"]) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData["password"] != postData["password_confirm"]:
            errors["password"] = "Passwords do not match"
        return errors

    def loginCheck(self, postData):
        errors = {}
        if not self.filter(email=postData["email"]).exists():
            errors["email"] = "User account does not exist"
        else:
            userpw = User.objects.get(email=postData["email"]).password
            if not bcrypt.checkpw(postData["password"].encode(), userpw.encode()):
                errors["password"] = "Password does not match"
        return errors

class User(models.Model):
    restaurant_manager = models.BooleanField(default=False)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.CharField(max_length=155)
    password = models.CharField(max_length=155)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class RestaurantManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if len(postData['city']) < 3:
            errors["city"] = "City should be at least 3 characters"
        if len(postData['state']) < 2:
            errors["state"] = "State should be at least 2 characters"
        if len(postData['street']) < 3:
            errors["street"] = "Street should be at least 3 characters"
        if len(postData['description']) < 3:
            errors["description"] = "Description should be at least 3 characters"
        return errors

class Restaurant(models.Model):
    name = models.CharField(max_length=155)
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=55)
    street = models.CharField(max_length=155)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RestaurantManager()

class Chef(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="chefs", on_delete= models.CASCADE)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=55)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Course(models.Model):
    users = models.ManyToManyField(User, related_name="courses", default=None)
    restaurant = models.ForeignKey(Restaurant, related_name="courses", on_delete= models.CASCADE)
    dish = models.CharField(max_length=55)
    category = models.CharField(max_length=155)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time_slot = models.DateTimeField()
    available_slots = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)