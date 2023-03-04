
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.permissions import IsAuthenticated






@api_view(['GET', 'POST'])

def dectect_list(request):

    if request.method == 'GET':
        snippets = Detects.objects.all()
        serializer = DetectSeializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DetectSeializer(data=request.data)
        dt = request.data['date_created']
        

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#222222222222222222222222222222222

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def date_filter(request):
    mylist=[]
    samecodelist=[]
    p=[]
    finalsend=[]
    myorde=[]
    resultfilter=[]
    
    
    if(request.data["startdate"]!= None and request.data["startdate"] != "" and request.data["enddate"]!= "" and request.data["enddate"]!=None):
        search=(Q(date2__gte=request.data["startdate"] , date2__lte=request.data["enddate"]))
    orders=Detects.objects.filter(search).all() 
    ser = DetectSeializer1(orders, many=True)
  
    return Response(ser.data, status=status.HTTP_200_OK) 


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mydate_filter(request):
   
    orders=Detects.objects.filter(classobj=0).values()
    ser = DetectSeializer1(orders, many=True)
  
    return Response(ser.data, status=status.HTTP_200_OK) 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def area(request):
    if request.method == 'GET':
        all_data = AreaModel.objects.all()
        if all_data:
            data = AreaSerializer(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("منطقه ای ثبت نشده است", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def camera(request):
    if request.method == 'GET':
        all_data = CameraInfo.objects.all()
        if all_data:
            data = CameraSerializer(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("نوعی برای ابجکت ثبت نشده است ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category(request):
    if request.method == 'GET':
        all_data = CategoryModel.objects.all()
        if all_data:
            data = CategorySerializer(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("نوعی برای ابجکت ثبت نشده است ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def factory(request):
    if request.method == 'GET':
        all_data = FactoryModel.objects.all()
        if all_data:
            data = FactorySerializer(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("کارخانه ای ثبت نشده است ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def factory_image(request):
    if request.method == 'POST':
        data = request.data
        serialized = FactoryImageSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        all_data = FactoryImageModel.objects.all()
        if all_data:
            data = FactoryImageSerializer2(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("دیتا موجود نیست", status=status.HTTP_400_BAD_REQUEST)




from django.contrib.auth import authenticate
@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    d={}
    # muser=User.objects.filter(username=request.data['username']).first()
    
    uuser=authenticate(username=request.data['username'],password=request.data['password'])
    
    if uuser is not None:
        d["token"]=Token.objects.get(user=uuser).key
        return Response(d, status = status.HTTP_200_OK)
    else:
        return Response("notexist", status = status.HTTP_404_NOT_FOUND)
    
    
# def signin(request):
#     if request.user.is_authenticated:
#         return render(request, 'homepage.html')
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#             form = AuthenticationForm(request.POST)
#             return render(request, 'signin.html', {'form': form})
#     else:
#         form = AuthenticationForm()
#         return render(request, 'signin.html', {'form': form})

# obtain_auth_token