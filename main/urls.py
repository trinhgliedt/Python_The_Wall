from django.urls import path

from . import views

urlpatterns = [
    path('', views.display_login), #GET, render log in-registration page
    path('user', views.display_login), #GET, redirect to root
    path('user/create-user', views.create_user), # 1.POST: create new user --> output: user/messages. 2. GET: redirect to root
    path('user/login', views.login), # 1. POST, log user in --> output: user/messages. 2. GET: redirect to root
    path('user/logout', views.logout), # 1. POST, log user out (clear user_id from session) --> output: redirect to root. 2. GET: redirect to root
    path('user/message', views.display_message), #GET: if user is not logged in: redirect to root. If user is logged in, render message.html (which includes input form to post messages)
    path('user/message/comment', views.display_comment), #GET: if user is not logged in: redirect to root. If user is logged in, render messageWithComment.html (which includes input form to post comments)
    path('user/message/update', views.update_message), #POST: Save message to the db --> output: redirect to user/message. #GET: if user is not logged in: redirect to root. If user is logged in, redirect to user/message.
    path('user/message/<msg_id>/comment/update', views.update_comment), #POST: Save comment to the db --> output: redirect to user/message.comment. #GET: if user is not logged in: redirect to root. If user is logged in, redirect to user/message/comment.
    path('user/message/<msg_id>/delete', views.delete_message), #POST: delete message --> output: redirect to user/message. #GET: if user is not logged in: redirect to root. If user is logged in, redirect to user/message.
    path('user/message/comment/<cmt_id>/delete', views.delete_comment), #POST: delete comment --> output: redirect to user/message/comment. #GET: if user is not logged in: redirect to root. If user is logged in, redirect to user/message/comment.

]