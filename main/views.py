from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

# Create your views here.
def display_login(request):

    return render(request, 'login_reg.html')


def create_user(request):
# if request method is GET then redirect to log in page

# if request method is POST then check errors. If no errors, move on to create user
    if request.method == "POST":
        print("request.POST:",request.POST)
        # to check errors before creating users. Display message amd redirect to log in page if there's errors:
        errors = User.objects.basic_validator(request.POST)

        if len(errors) > 0:
            print("errors: ",errors)
            for key, val in errors.items():
                messages.error(request, val)
            return redirect("/")

        # user will be created if there's no validation errors:
        print("----------Start creating user")

        hashed_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
        created_user = User.objects.create(first_name = request.POST["first_name"], last_name = request.POST["last_name"], email = request.POST["email"], password = hashed_pw)
        
        request.session["user_id"] = created_user.id

        return redirect("/user/message")
    
    # if request method is GET then redirect to log in page
    return redirect("/")


def login(request):
    if request.method == "POST":
        #try to find the user in the DB
        potential_users = User.objects.filter(email = request.POST["email"])

        if len(potential_users) ==0:
            messages.error(request, "Please check your email and password.")
            return redirect('/')
        
        #if we're here, meaning the email was found.
        #compate the provided pw with the hashed on in the DB
        if bcrypt.checkpw(
            request.POST["password"].encode(),
            potential_users[0].password.encode()):
            request.session["user_id"] = potential_users[0].id
            return redirect("/user/message")
        
        #if we're here, the password was incorrect
        messages.error(request, "Please check your email and password.")
    return redirect("/")


def logout(request):
    request.session.clear()
    return redirect("/")

def display_message(request):
    # to redirect to log in page when user didn't log an and user typed the direct path: user/message
    if "user_id" not in request.session:
        messages.error(request, "You need to log in to see that page.")
        return redirect("/")
    # if user already logged in: render page and pass on context
    context = {
        "this_user": User.objects.get(id=request.session["user_id"]),
        "cmt_on": False,
        "all_users_msgs": Message.objects.all(),
    }
    return render(request, 'message.html', context)


def display_comment(request):
    # to redirect to log in page when user didn't log an and user typed the direct path: user/message/comment
    if "user_id" not in request.session:
        messages.error(request, "You need to log in to see that page.")
        return redirect("/")
    # if user already logged in: render page and pass on context
    context = {
        "this_user": User.objects.get(id=request.session["user_id"]),
        "cmt_on": True,
        "all_users_msgs": Message.objects.all(),
    }
    return render(request, 'message.html', context)


def update_message(request):
    if request.method == "POST":
        Message.objects.create(message = request.POST["msg_input"], user_id=request.session["user_id"])
    return redirect("/user/message")

def update_comment(request, msg_id):
    if request.method == "POST":
        Comment.objects.create(comment = request.POST["cmt_input"], user_id=request.session["user_id"], message_id=msg_id)
    return redirect("/user/message/comment")

def delete_message(request, msg_id):
    if request.method == "POST":
        Message.objects.get(id=msg_id).delete()
    return redirect("/user/message")

def delete_comment(request, cmt_id):
    # print("cmt_id: ",cmt_id, "request.method: ",request.method)
    if request.method == "POST":
        Comment.objects.get(id=cmt_id).delete()
    return redirect("/user/message/comment")


# Make link to view comments when in the messages X
# format timestamp https://stackoverflow.com/questions/14657173/get-local-timezone-in-django
# css for message X
# note which one is a msg and which is a comment? no needed, indentation is clear X 
# let user delete their own msg X
#                               within 30 mins
# ask TA about local time X Morley helped