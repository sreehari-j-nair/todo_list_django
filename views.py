from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth.models import User
from .models import TODOO
from django.contrib.auth import login as auth_login,logout,authenticate

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        conf_password = request.POST.get("confirm-password")

        if(password != conf_password):
            messages.error(request,"Password mismatch!!")
            return redirect("signup")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect("signup")
        
        user = User.objects.create_user(username,email,password)
        user.save()

        messages.success(request,"User registered successfully")
        return redirect("login")

    return render(request,"signup.html")

def login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            auth_login(request,user)
            result = TODOO.objects.filter(user=request.user).order_by("date")
            return render(request,"todo_mainpage.html", {"name":username,"result":result})
        else:
            messages.error(request,"Credentials are wrong")
            return redirect("login")

    return render(request,"login.html")

def index(request):

    if request.method == "POST":
        task = request.POST.get("task")
        obj = TODOO(title=task, user=request.user)
        obj.save()

        result = TODOO.objects.filter(user=request.user).order_by("date")
        return render(request,"todo_mainpage.html",{"result":result})
    
    result = TODOO.objects.filter(user=request.user).order_by("date")
    return render(request,"todo_mainpage.html",{"result":result})

def edit_todo(request,srno):

    if request.method == "POST":
        task = request.POST.get("task")
        obj = TODOO.objects.get(srno=srno)
        obj.title = task
        obj.save()

        result = TODOO.objects.filter(user=request.user).order_by("date")
        return render(request,"todo_mainpage.html",{"result":result})
    
    obj = TODOO.objects.get(srno=srno)
    return render(request,"edit_todo.html",{"obj":obj})

def delete_todo(request,srno):
    obj = TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect("todo_mainpage")

def signout(request):
    logout(request)
    return redirect("login")