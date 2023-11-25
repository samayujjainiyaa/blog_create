from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login 
from django.shortcuts import get_object_or_404

def blog(request):
    flag = True
    auther = Account.Objects.get(username = request.user.username)
    if auther.is_auther == True:
        flag = True
        if request.method == "POST":
            title = request.POST.get('title')
            blog = request.POST.get('blog')
            user = request.user

            if Blog.objects.filter(title = title).exists():
                messages.info(request, "blog title already exists")
                return redirect('/blog/')
            blog = Blog(
                writer = user,
                title = title,
                blog = blog,
            )
            blog.save()
            print("blog added successfully")
            return redirect('/')

    else:
        flag = False

    context = {
        'Account':auther,
        'Flag':flag,
    }    
    return render(request,'blog.html', context)



def index(request): 
    if request.user.is_authenticated:
        flag = True
        auther = Account.Objects.get(username = request.user.username)
        if auther.is_auther == True:
            flag = True
        else:
            flag = False

        print("auther is : ", auther)
        if Blog.objects.filter(writer = auther):
            blog = Blog.objects.filter(writer = auther)
            print("blog is ",blog)
            context = {
                'blog' : blog,
                'Flag':flag
            }
        else:
            print("else part")
            blog = Blog.objects.all()
            context = {
                'blog' : blog,
                'Flag':flag
            }
        return render(request,'index.html', context)
    else:
        return render(request,'index.html')


def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pwd']
        is_auther = request.POST.get('is_auther','True')

        if is_auther=='on':
            print("hello world")
            
            # if Account.objects.filter(email=email).exists():
            if Account.Objects.filter(email=email).exists():
                print("email already exists")
                return redirect('/signup/')

            user = Account(username=username, email=email, is_auther=True)
            user.set_password(password)
            user.is_admin = True
            user.is_staff = True
            user.is_active = True
            user.save()
            messages.info(request,'sucessfully signed up')
            print("success")
            return redirect("/ulogin/")
            
        else: 
            print("off")
            if Account.Objects.filter(email=email).exists():
                print("email already exists")
                return redirect('/signup/')

            user = Account(username=username, email=email, is_auther=False)
            user.set_password(password)
            user.is_admin = True
            user.is_staff = True
            user.is_active = True
            user.save()
            messages.info(request,'sucessfully signed up')
            print("success")
            return redirect("/ulogin/")
    else:
        return render(request,'signup.html')


def mainlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['pwd']

        # Try to authenticate as a normal user
        user = authenticate(username=username, password=pwd)
        print(user)
        
        if user is not None:
            # User is a normal user
            login(request, user)
            return redirect('/')
        else:
            # If no normal user found, check for superuser
            superuser = Account.Objects.filter(username=username, is_superadmin=True).first()
            if superuser is not None and superuser.check_password(pwd):
                login(request, superuser)
                return redirect('/')
            else:
                messages.info(request, 'Invalid username and password')
                return redirect('/ulogin/')    
    else:
        return render(request, 'ulogin.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
def personal(request):
    return render(request,'personal.html')


