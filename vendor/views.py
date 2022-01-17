from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth  import authenticate,  login, logout
from .models import Contact, UserAI, token
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject= request.POST.get('subject', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, subject=subject, desc=desc)
        contact.save()
        thank = True
    return render(request,'vendor/contact.html',{'thank': thank})

def loginpage(request):
    return render(request,'vendor/login.html')

def signuppage(request):
    return render(request,'vendor/signup.html')

def roc(request, tokhen, choice):
    done = False
    if request.method == "POST":
        randomToken = request.POST['randomToken']
        phoneNum = request.POST['mobile']
        addNote = request.POST['note']
        vendor = request.user.username 
        vendor = User.objects.get(username = vendor)
        newToken = token(randomToken = randomToken, phoneNum = phoneNum, addNote = addNote, vendor = vendor, completed = False, rejected = False)
        newToken.save()
        done = True
    vendor = request.user.username 
    vendor = User.objects.get(username = vendor)    
    listTokens = token.objects.filter(vendor = vendor)
    UAI = UserAI.objects.get(user = vendor)  
    tokens = generateToken()
    oldTokens = token.objects.filter(vendor = vendor)  
    if choice == 1: 
        try: 
            ctoken = token.objects.get(randomToken = tokhen)
            ctoken.completed = True
            ctoken.save()
        except:
            print("completion aborded")
    if choice == 2:
        try: 
            ctoken = token.objects.get(randomToken = tokhen)
            ctoken.rejected = True
            ctoken.save()
        except:
            print("completion aborded")
    param = {'UAI': UAI, 'token': tokens, 'listToken': listTokens, 'done':done, 'oldTokens': oldTokens}
    return render(request,'vendor/vendor.html', param)    

@login_required
def dashBoard(request):
    done = False
    if request.method == "POST":
        randomToken = request.POST['randomToken']
        phoneNum = request.POST['mobile']
        addNote = request.POST['note']
        vendor = request.user.username 
        vendor = User.objects.get(username = vendor)
        newToken = token(randomToken = randomToken, phoneNum = phoneNum, addNote = addNote, vendor = vendor, completed = False, rejected = False)
        newToken.save()
        done = True
    vendor = request.user.username 
    vendor = User.objects.get(username = vendor)    
    UAI = UserAI.objects.get(user = vendor.id)
    listTokens = token.objects.filter(vendor = vendor)  
    tokens = generateToken()
    oldTokens = token.objects.filter(vendor = vendor)  
    param = {'UAI': UAI, 'token': tokens, 'done':done, 'listToken': listTokens}#, 'oldTokens': oldTokens}
    return render(request,'vendor/vendor.html', param)

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username'].lower()
        email=request.POST['email']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        password=request.POST['password'] 
        confirmpassword=request.POST['confirmpassword']
        businessname=request.POST['businessname']
        objective=request.POST['objective']
        sticknote=request.POST['sticknote']
        # check for errorneous input
        sgnpg = '/vendor/signup/'
        try:
            UserCheck = User.objects.get(username = username)          
            if UserCheck:
                messages.error(request, " User Already exist")
                return redirect(sgnpg)
  
        except:
            pass
        
        if len(username)>30:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect(sgnpg)

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect(sgnpg)

        if (password!= confirmpassword):
             messages.error(request, " Passwords do not match")
             return redirect(sgnpg)

        # Create the user
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name= firstname
        myuser.last_name= lastname
        myuser.save()
        up = UserAI(user=myuser, businessname = businessname, objective = objective, sticknote = sticknote)
        up.save()
		
        messages.success(request, " Your account has been successfully created")
        return redirect('/vendor/login/')

    else:
        return HttpResponse("404 - Not found")

def handelLogin(request):
    if request.method=="POST":
        try:
            randomToken = request.POST['randomToken']
            phoneNum = request.POST['mobile']
            addNote = request.POST['note']
            vendor = username
            print(randomToken, phoneNum, addNote, vendor)
            newToken = token.objects.Create(randomToken = randomToken, phoneNum = phoneNum, addNote = addNote, vendor = vendor)
            newToken.save()
        except Exception as e:
            print(e,1)
    
        # Get the post parameters
        loginusername=request.POST['loginusername'].lower()
        loginpassword=request.POST['loginpassword']
        user=authenticate(username= loginusername, password= loginpassword)
        
        
        if user is not None:
            UAI = UserAI.objects.get(user = user.id)
            login(request, user)
            messages.success(request, "Successfully Logged In")
            tokens = generateToken()
            try:
                oldTokens = token.objects.filter(vendor = username)
            except:
                oldTokens = ''
            param = {'UAI': UAI, 'token': tokens, "oldTokens":oldTokens}
            print('handel login',param)
            return render(request,'vendor/vendor.html', param)

        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect('/vendor/login/')

    return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return render(request,'index.html')

def trackToken(request):
    if request.method=="POST":
        trackToken = request.POST['trackToken']
        try:
            tracked = token.objects.get(randomToken = trackToken)
            if tracked.completed == True:
                status = "completed"
            elif tracked.rejected == True:
                status = "Rejected"
            else: 
                status = "awaiting"
            param = {'tracked':tracked, 'status':status}
            return render(request, 'vendor/user.html', param)
        except:
            messages.error(request, "Invalid token ID! Please try again")
            return redirect("/")
    

def generateToken():
    check = True
    while check:
        number = random.randint(3141592653, 9999999999)
        try:
            tokens1 = token.objects.get(randomToken = number)
        except:
            tokens1 = None
        if tokens1:
            pass
        else:
            check = False
    return number



