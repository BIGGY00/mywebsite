from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from .models import *
# from songline import Sendline
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator

from django.utils import timezone
from decimal import Decimal
from django.db import transaction


# Create your views here.
def home(request):
    allproduct = Product.objects.all()
    product_per_page = 3
    paginator = Paginator(allproduct, product_per_page)
    page = request.GET.get('page')
    allproduct = paginator.get_page(page)

    context = {'allproduct' : allproduct}

    allrow = []
    row = []
    for i,p in enumerate(allproduct):
        if i%3 == 0:
            if i != 0:
                allrow.append(row)
            row = []
            row.append(p)
        else:
            row.append(p)
    allrow.append(row)
    context['allrow'] = allrow

    return render(request,'myapp/home.html', context)

def aboutUs(request):
    return render(request, 'myapp/aboutus.html')

def contact(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        topic = data.get('topic')
        email = data.get('email')
        detail = data.get('detail')

        if (topic =='' or email == '' or detail == ''):
            context['message']= 'Please, fill in all contact information'
            return render(request,'myapp/contact.html', context)

        newRecord = contactList()
        newRecord.topic = topic
        newRecord.email = email
        newRecord.detail = detail
        newRecord.save()

        context['message'] = 'The message has been received'
    return render(request, 'myapp/contact.html', context)
    # token = 'rH7moNvRhof84P5rfQNLDR9RpvTD6L91afitghPY59r'
    # context = {} #message to notify
    # return render(request, 'myapp/contact.html', context)
    # if request.method == 'POST':
    #     data = request.POST.copy()
    #     topic = data.get('topic')
    #     email = data.get('email')
    #     detail = data.get('detail')

    #     if(topic =='' or email =='' or detail ==''):
    #         context['message']= 'Please, fill in all contact information'
    #         return render(request, 'myapp/contact.html', context)

    #     newRecord = contactList() #create object
    #     newRecord.topic = topic
    #     newRecord.email = email
    #     newRecord.detail = detail
    #     newRecord.save()

    #     context['message'] = 'The message has been received'

    #     m = Sendline(token)
    #     m.sendtext('\ntopic:{0}\n email:{1}\n detail:{2}'.format(topic, email, detail))

def userLogin(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')
        password = data.get('password')

        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home-page')
        except:
            context['message']="username or password is incorrect."   
             
    return render(request, 'myapp/login.html', context)

def userLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login')
def showContact(request):
    allcontact = contactList.objects.all()
    context = {'contact': allcontact}
    return render(request, 'myapp/showcontact.html', context)

def userRegist(request):
    context={}

    if request.method =='POST':
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repassword = data.get('repassword')

        try:
            User.objects.get(username=username)
            context['message'] = "Username duplicate"

        except:
            newuser = User()
            newuser.username = username
            newuser.first_name = firstname
            newuser.last_name = lastname
            newuser.email = email

            if(password == repassword):
                newuser.set_password(password)
                newuser.save()
                newprofile = Profile()
                newprofile.user = User.objects.get(username=username)
                newprofile.save()
                context['message'] = "register complete."
            else:
                context['message'] = "password or re-password is incorrect."
    return render(request, 'myapp/register.html', context)

def userProfile(request):
    context={}
    userprofile = Profile.objects.get(user=request.user)
    context['profile']=userprofile
    return render(request,'myapp/profile.html',context)

def editProfile(request):
    context={}
    if request.method == 'POST':
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        current_user = User.objects.get(id=request.user.id)
        current_user.first_name = firstname
        current_user.last_name = lastname
        current_user.username = username
        current_user.email = email
        current_user.set_password(password)
        current_user.save()

        try:
            user = authenticate(username=current_user.username,password=current_user.password)
            login(request,user)
            return redirect('home-page')
        
        except:
            context['message'] = "edit profile fail"
    return render(request, 'myapp/editprofile.html')

def actionPage(request, cid):
    #cid = contactList id
    context ={}
    contact = contactList.objects.get(id=cid)
    context['contact'] = contact

    try:
        action = Action.objects.get(contactList=contact)
        context['action'] = action
    except:
        pass

    if request.method == 'POST':
        data = request.POST.copy()
        actiondetail = data.get('actiondetail')

        if 'save' in data:
            try:
                check = Action.objects.get(contactList=contact)
                check.actionDetail = actiondetail
                check.save()
                context['action'] = check
            except:
                new= Action()
                new.contactList = contact
                new.actionDetail = actiondetail
                new.save()
        elif 'delete' in data:
            try:
                contact.delete()
                return redirect('showcontact-page')
            except:
                pass
        elif 'complete' in data:
            contact.complete = True
            contact.save()
            return redirect('showcontact-page')
    return render(request,'myapp/action.html',context)


def addProduct(request):
    if request.method == 'POST':
        data= request.POST.copy()
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        quantity = data.get('quantity')
        instock = data.get('instock')

        new = Product()
        new.title = title
        new.description = description
        new.price = price
        new.quantity = quantity

        if instock == "instock":
            new.instock = True
        else:
            new.instock = False
        
        if 'picture' in request.FILES:
            file_image = request.FILES['picture']
            file_image_name = file_image.name.replace(' ','')

            fs = FileSystemStorage(location='media/product')
            filename = fs.save(file_image_name, file_image)
            upload_file_url = fs.url(filename)
            print('Picture url:', upload_file_url)
            new.picture = 'product' + upload_file_url[6:]

        if 'specfile' in request.FILES:
            file_specfile = request.FILES['specfile']
            file_specfile_name = file_specfile.name.replace(' ','')

            fs = FileSystemStorage(location='media/specfile')
            upload_file_url = fs.url(filename)
            print('Specfile url: ', upload_file_url)
            new.specfile = 'specfile' + upload_file_url[6:]

        new.save()
    
    return render(request, 'myapp/addproduct.html')


def handler404(request, exception):
    return render(request, 'myapp/404errorPage.html')

def productDetail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'myapp/product_detail.html', context)