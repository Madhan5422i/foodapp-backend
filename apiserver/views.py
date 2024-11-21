from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest,JsonResponse
from .models import *
from .serializers import *
from rest_framework.decorators import api_view,parser_classes
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
import json
# from django.contrib.auth.models import User
from decimal import Decimal
from django.contrib.auth import login,logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import razorpay
import django.conf as settings
from rest_framework.parsers import MultiPartParser,FormParser

# Create your views here.
def index(request):
    return HttpResponse("hii")

def jsonresponse_test(request):
    return JsonResponse({'name':'Madhan','age':19},status=201)


@api_view(['GET'])
def Explore_menu_serve(request):
    data = Explore_menu.objects.all()
    serializer = Explore_menu_serializer(data, many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['GET'])
def itemList(request):
    data = item_List.objects.all()
    serializer = item_List_serializer(data, many=True,context={'request':request})
    return Response(serializer.data)

@api_view(['POST'])
def cartData(request):
    serializer = cartDataSerializer(data=request.data, many=True)
    if serializer.is_valid():
        user = CusUser.objects.get(username='madhan')
        cart, created = Cart.objects.get_or_create(user=user)
        total = cart.total
        is_cart_edited = False

        for data in serializer.validated_data:
            itemname = data['item']
            item = item_List.objects.get(name=itemname)
            quantity = data['quantity']
            item_price = data['item_price']
            price = data['price']

            # Calculate the total based on price and quantity
            total += Decimal(price)
        
            # Check if the item already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(item=item, cart=cart)

            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity

            cart_item.save()

        # Update the cart total
        cart.total = Decimal(total) + Decimal('2.5')
       
        print(cart.total)
        print(total)
        cart.save()

        return Response({'status': 'success'})
    else:
        return Response(serializer.errors, status=400)

    
@api_view(['POST','GET'])
def loginUser(request):
    serializer = loginSerializer(data=request.data,context={'request':request})
    # print(dir(request))
    if serializer.is_valid():
        user = serializer.validated_data['user']
        check = serializer.validated_data.get('check')
        if check == True:
            request.session.set_expiry(1209600)
        else:
            request.session.set_expiry(0)
        login(request._request,user)
        serializer = DataSerializer(user)
        print(check)
        return JsonResponse({'isAuthenticated': True,"data":serializer.data})
    else:
        return Response(serializer.errors,status=400)
    


@api_view(['POST'])
def RegisterUser(request):
    serializer = RegisterSerializer(data=request.data,context={'request':request})
    if serializer.is_valid():
        result = serializer.save()
        user = result['user']
        if user is not None:
            login(request._request, user)
            return JsonResponse({'isAuthenticated': True})
        else:
            return JsonResponse({'error': 'Authentication failed'}, status=400)
    return Response(serializer.errors,status=400)



@api_view(['POST'])
def LogoutUser(request):
    if request.user and request.user.is_authenticated:
        logout(request)
        return JsonResponse({"isAuthenticated":False})
    else:
        return JsonResponse({"not a user":True})


@login_required(login_url='/api/login/')
@api_view(['POST','GET', 'PUT'])
def AddressAPI(request):
    if request.method in ['POST', 'PUT']:
        # Check if the address for this user already exists
        addresses = Address.objects.filter(user=request.user)
        if addresses.exists():
            address = addresses.first()  # Get the existing address
            serializer = AddressSerializer(address, data=request.data, context={'request': request})
        else:
            serializer = AddressSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            adr, created = Address.objects.update_or_create(user=request.user, defaults=serializer.validated_data)
            return JsonResponse(serializer.data, status=201 if created else 200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'GET':
        addresses = Address.objects.filter(user=request.user)
        serializer = AdrObjSerializer(addresses, many=True)
        return Response(serializer.data)


@login_required(login_url='/api/login/')
@api_view(['POST','GET'])
@parser_classes([MultiPartParser, FormParser])
def getProfile(request):
    if request.method == 'GET':
        user = request.user
        data = CusUser.objects.filter(email=user)
        serializer = profileSerializer(data, many=True,context={'request':request})
        return Response(serializer.data)
    if request.method == 'POST':
        user = request.user
        profile = request.FILES.get('profile')
        if profile:
            user.profile_image = profile
            user.save()
            return JsonResponse({'message':'uploaded'},safe=False)
        else:
            return JsonResponse({'message':'not uploaded'},safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=402)

    
@login_required(login_url='/api/login/')
def check_auth_view(request):
    if request.user:
        user = request.user
        serializer = DataSerializer(user)
        return JsonResponse({'isAuthenticated': request.user.is_authenticated,"data":serializer.data})
    else:
        return JsonResponse({'isAuthenticated': False})






razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET_KEY))

@csrf_exempt
def payment_view(request):
    if request.method == 'GET':
        name = "Swapnil Pawar"
        amount = 400

        razorpay_order = razorpay_client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

        data = {
            "name" : name,
            "merchantId": RAZORPAY_KEY_ID,
            "amount": amount,
            "currency" : 'INR' ,
            "orderId" : razorpay_order["id"],
        }

        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'fucked Request'}, status=420)

@csrf_exempt
def callback_view(request):
    if request.method == 'POST':
        response = request.POST.dict()

        if "razorpay_signature" in response:
            data = razorpay_client.utility.verify_payment_signature(response)


        else:
            error_code = response['error[code]']
            error_description = response['error[description]']
            error_source = response['error[source]']
            error_reason = response['error[reason]']
            error_metadata = json.loads(response['error[metadata]'])

            error_status = {
                'error_code': error_code,
                'error_description': error_description,
                'error_source': error_source,
                'error_reason': error_reason,
            }

            return JsonResponse({'error_data': error_status}, status=401)


def success(request):
    return render(request, 'success.html')










