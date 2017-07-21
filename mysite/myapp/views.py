from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from models import User, SessionToken, PostModel, LikeModel, CommentModel

#importing to convert paasword into hashcode
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta,datetime
from django.utils import timezone
from mysite.settings import BASE_DIR

#pre-installed library ctypes for showing pop up messageboxes
import ctypes

#sendgrid API used for sending mails to the new users
from sendgrid.helpers.mail import *
import sendgrid

#used for rematching the input
import re

#imgur API provides server to store images users uploads
from imgurpython import ImgurClient




# Create your views here.


#declarating function for signing up a new user
def signup_view(request):
    today = datetime.now()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if not re.match("[a-zA-Z]*$",username):
                ctypes.windll.user32.MessageBoxW(0, u"kindly enter valid details!!!", u"Error", 0)

            name = form.cleaned_data['name']
            if not re.match("[a-zA-Z]*$",name):
                ctypes.windll.user32.MessageBoxW(0, u"kindly enter valid details!!!", u"Error", 0)

            email = form.cleaned_data['email']
            if not re.match("[a-z0-9@.]*$",email):
                ctypes.windll.user32.MessageBoxW(0, u"kindly enter valid details!!!", u"Error", 0)
            password = form.cleaned_data['password']
            #saving data to DB
            user = User(name=name, password=make_password(password), email=email, username=username)
            user.save()

            #code to send mail to the user
            send = sendgrid.SendGridAPIClient(apikey=my_grid_api)
            from_email = Email("kajalangural1@gmail.com")
            to_email = Email(email)
            subject = "Confirmation Mail"
            content = Content("text/plain", "to verify provided email adress")
            mail = Mail(from_email, subject, to_email, content)
            response = send.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)


            ctypes.windll.user32.MessageBoxW(0, u"Successfully signed in..!!!!!\n\nEmail has been sent\n\nClick Ok", u"Success", 0)

            return render(request, 'feed.html')


    else:


        form = SignUpForm()

    return render(request, 'signup.html', {'date_show':today,'form' : form})


#declaring function to login a already user
def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    #generating session token
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login1.html', response_data)


#declaring function for posting
def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + post.image.url)

                client = ImgurClient("5295eea21198160", "87b2a4acd0794d75ed8a5caee3affdeac82aa8fc")
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()

                ctypes.windll.user32.MessageBoxW(0, u"Post Created!!!!", u"Success", 0)

                return redirect('/feed/')

        else:
            ctypes.windll.user32.MessageBoxW(0, u"Invalid Post!!!!",u"Error", 0)
            form = PostForm()
        return render(request, 'postview.html', {'form': form})
    else:
        return redirect('/login1/')


#declaring function to show feeds to the user
def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('-created_on')

        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True

        return render(request, 'feed.html', {'posts': posts})
    else:

        return redirect('/login1/')


#declaring function to like the post
def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
                ctypes.windll.user32.MessageBoxW(0, u"Successfully liked the post..!!!!!\nClick Ok", u"Success", 0)


            else:
                existing_like.delete()          #deleting the like of liked post
            return redirect('/feed/')
    else:
        return redirect('/login1/')



#declaring function to comment on post
def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            ctypes.windll.user32.MessageBoxW(0, u"Successfully commented the post..!!!!!\nClick Ok", u"Success", 0)

            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login1')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            #time to expire session token
            time_to_live = session.created_on + timedelta(minutes=5)
            if time_to_live > timezone.now():
                return session.user
    else:
       return None