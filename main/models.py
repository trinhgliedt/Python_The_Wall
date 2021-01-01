from django.db import models
import re


# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')
        errors = {}

        if len(post_data["first_name"]) < 2:
            errors["first_name"] = "Please enter at least 2 characters for your first name."
        if len(post_data["last_name"]) < 2:
            errors["last_name"] = "Please enter at least 2 characters for your last name."
        if not EMAIL_REGEX.match(post_data['email']): 
            errors['email'] = 'Please enter a valid email address!'
        elif User.objects.filter(email = post_data["email"]).exists():
            errors['email'] = "You can't use that email address."
        if post_data["password"] != post_data["confirmPW"]:
            errors["confirmPW"] = "Please ensure that your password matches the confirmation."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class Message(models.Model):
    message = models.TextField()
    
    user = models.ForeignKey(
        User,
        related_name='message',
        on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Comment(models.Model):
    comment = models.TextField()
    
    user = models.ForeignKey(
        User,
        related_name='comment',
        on_delete=models.CASCADE)

    message = models.ForeignKey(
        Message,
        related_name='comment',
        on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

