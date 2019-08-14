from __future__ import unicode_literals
from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        errors = {}

        if len(postData['fn']) <2 or not postData['fn'].isalpha():
            errors["fn"] = "Your first name should have more than 2 letters only!"
        
        if len(postData['ln']) <2 or not postData['ln'].isalpha():
            errors["ln"] = "Your last name should have more than 2 letters only!"

        if not EMAIL_REGEX.match(postData['em']): 
            errors["em"] = "You must enter a valid email!"

        if User.objects.filter(email = postData['em']):
            errors["em"] = "Your email is already registered!"

        if len(postData['pword']) < 8:
            errors["pword"] = "Your password needs to be at least 8 characters!"

        if postData['pword'] != postData['confirmpw']:
            errors["cpword"] = "Your passwords do not match!"
        
        print(f"***************************** {errors} from model.py")
        return errors

    def validate_login(self, postData):

        errors = {}

        user = User.objects.filter(email = postData['logem'])
        
        if not (user and bcrypt.checkpw(postData['logpw'].encode(), user[0].password.encode())):
            errors["login"] = "You didn't provide a valid email or password!"
            print("You didn't provide a valid email or password!")
        
        return errors
        

class User(models.Model):
    #id
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    