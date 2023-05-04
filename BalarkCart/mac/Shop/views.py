from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate,User
from math import ceil
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import Group 
from django.contrib.auth.decorators import login_required
from .decoraters import unauthenticated_user,allowed_users

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category =cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    # params = {'no_of_slides': nSlides,'range': range(1,nSlides),'product':products}
    # allProds = [[products, range(1,nSlides),nSlides],[products, range(1,nSlides),nSlides]]
    params = {'allProds': allProds}
    return render(request,'Shop/index.html',params)

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email =request.POST.get('email')
        phone =request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name = name, email=email, phone = phone ,desc = desc)
        contact.save()
    return render(request,'Shop/contact.html')

def about(request):
    return render(request,'Shop/about.html')

@login_required(login_url='/shop/login/')
def tracker(request):
    if request.method == "POST":
        email =request.POST.get('email')
        orderId = request.POST.get('orderId')
        try:
            orders = Order.objects.filter(order_id = orderId , email = email)
            if len(orders) > 0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                updates = []

                for i in update:
                    updates.append({'text': i.update_desc , 'time': i.timestamp})
                    response =  json.dumps({"status":"success","updates":updates,"items_json":orders[0].items_json },default=str)  

                return HttpResponse(response) 
            
            else:
              return HttpResponse('{"status":"No item found"}')
        except Exception as e:
            return HttpResponse('{"status":"Error"}') 
    return render(request,'Shop/tracker.html')

# Serach page view function
def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'Shop/search.html', params)

# Search query match function
def searchMatch(query, item):
    if query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True
    else:
        return False
   
      


# Product View page function
@login_required(login_url='/shop/login/')
def productview(request,myid):
    # We will fetch the product from model using id of product
    product = Product.objects.filter(id =myid)
    return render(request,'Shop/prodView.html',{'i':product[0]})

# Cart View page function
@login_required(login_url='/shop/login/')
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson')
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        phone = request.POST.get('phone')

        order = Order(name=name, email=email, address1=address1,address2 = address2,city=city, state= state, zip_code=zip_code, phone=phone,items_json = items_json , amount= amount)
        order.save()
        update = OrderUpdate(order_id = order.order_id, update_desc = "The Order has been placed") 
        update.save()
        thank = True 
        id= order.order_id
        param_dict = {

                'MID': 'Your-Merchant-Id-Here',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        return render(request,'Shop/checkout.html',{'thank':thank,'id':id})
        #  Request paytm to transfer the amount to your acoount after payment by user
    return render(request,'Shop/checkout.html')



@login_required(login_url='/shop/login/')
@allowed_users(allowed_roles=['Admin'])
def registerProduct(request):
    return render(request,'Shop/')



@login_required(login_url='/shop/login/')
@allowed_users(allowed_roles=['Admin'])
def table(request):
   product = Product.objects.all()
   return render(request,'Shop/table.html',{'product':product})

@login_required(login_url='/shop/login/')
@allowed_users(allowed_roles=['Admin'])
def deleteProd(request,product_id):
    product = Product.objects.get(id=product_id)  
    product.delete()
    return redirect('table')



# -------------------------Login Authentication system starts from her-------------#
@unauthenticated_user
def loginPage(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('ShopeHome')
        else:
          messages.info(request,"Password or Username is Invalid!")

    return render(request,'Shop/login.html')

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            messages.success(request,username + ',You have successfully created account in BalarkCart!')
            return redirect('loginPage')

    context = {'form': form}
    return render(request,'Shop/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')