from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.db.models.query_utils import Q

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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def mydate_filter(request):
   
    orders=Detects.objects.filter(classobj=0).values()
    ser = DetectSeializer1(orders, many=True)
  
    return Response(ser.data, status=status.HTTP_200_OK) 

@api_view(['GET'])
@permission_classes([AllowAny])
def area(request):
    if request.method == 'GET':
        all_data = AreaModel.objects.all()
        if all_data:
            data = AreaSerializer(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("منطقه ای ثبت نشده است", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def camera(request):
    if request.method == 'GET':
        all_data = CameraInfo.objects.all()
        if all_data:
            data = CameraSerializer(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("نوعی برای ابجکت ثبت نشده است ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def category(request):
    if request.method == 'GET':
        all_data = CategoryModel.objects.all()
        if all_data:
            data = CategorySerializer(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("نوعی برای ابجکت ثبت نشده است ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def factory(request):
    if request.method == 'GET':
        all_data = FactoryModel.objects.all()
        if all_data:
            data = FactorySerializer(all_data, many=True).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("کارخانه ای ثبت نشده است ", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
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
