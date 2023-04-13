from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate,User
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from math import ceil
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
                    response =  json.dumps([updates,orders[0].items_json], default=str)  

                return HttpResponse(response) 
            
            else:
              return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}') 
    return render(request,'Shop/tracker.html')

def search(request):
    return render(request,'Shop/search.html')

def productview(request,myid):
    # We will fetch the product from model using id of product
    product = Product.objects.filter(id =myid)
    return render(request,'Shop/prodView.html',{'product':product[0]})

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
        return render(request,'Shop/checkout.html',{'thank':thank,'id':id})
        #  Request paytm to transfer the amount to your acoount after payment by user
    return render(request,'Shop/checkout.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['psw']

        if User.objects.filter(email = email).exists():
            usr = authenticate(email = email, psw=password)
    
            if usr:
                login(request,usr)
                return redirect('table')
            
            return redirect('table')
        
        messages.info(request,'Please insert the correct password and email!')

        return redirect('login')
    
    return render(request,'Shop/login.html')



def admin1(request):
    if request.method == 'POST':
        product_name = request.POST.get('product name')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.POST.get('image')
        date = request.POST.get('date')
        product = Product(product_name=product_name, category = category , subcategory = subcategory , price=price, desc=desc, image = image ,pub_date=date )
        product.save()

    return render(request,'Shop/admin.html')

def table(request):
   product = Product.objects.all()
   return render(request,'Shop/table.html',{'product':product})

# def edit(request,product_id):
#     product = Product.objects.get(id=product_id)
#     if request.method == 'POST':
#        product.product_name=  request.POST['product name']
#        product.category = request.POST['category'] 
#        product.subcategory =  request.POST['subcategory']
#        product.price = request.POST['price']
#        product.desc = request.POST['desc']
#        product.image = request.POST['image']
#        product.date = request.POST['date']
#        product.save()
#        return redirect('table')
#     else:
#        return render(request,'Shop/table.html',{'product':product})
       
def deleteProd(request,product_id):
    product = Product.objects.get(id=product_id)  
    product.delete()
    return redirect('table')

@csrf_exempt
def handlerequest(request):
    # Paytm will send you post request here
    pass
