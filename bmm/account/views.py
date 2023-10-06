from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserChangePasswordSerializer, UserLoginSerializer,UserProfileSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.http import JsonResponse 
from account.models import Events   
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EventSerializer
from .models import Event
from datetime import datetime, timedelta
from rest_framework.authentication import TokenAuthentication

@api_view(['GET'])
def get_event_details(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST','GET'])
def save_event_api(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success'})
    else:
        return Response({'status': 'error', 'message': serializer.errors})

#Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'Msg': 'Registration Success'},
            status = status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
            serializer = UserLoginSerializer(data= request.data)
            if serializer.is_valid(raise_exception=True):
                email = serializer.data.get('email')
                password  = serializer.data.get('password')
                user = authenticate(email=email,password=password)
                if user is not None:
                    token = get_tokens_for_user(user)
                    return Response({'token':token,'Message': 'Login Success'},status = status.HTTP_200_OK)
                else:
                    return Response({'error': {'non_field_errors':['email or password is not valid']}},
                                    status = status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors,status=status.HTTP_307_TEMPORARY_REDIRECT_404_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            user = request.user
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):  
    all_events = Events.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'index.html',context)
 

def all_events(request):
    all_events = Events.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y"),
            'end': event.end.strftime("%m/%d/%Y"),
        })

    return JsonResponse(out, safe=False)


def add_event(request):
    start = (datetime.now() + 1).strftime("%m/%d/%Y")
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {
        'start_date': start
    }
    return JsonResponse(data)


def update(request):
    start = (datetime.now() + 1).strftime("%m/%d/%Y")
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {
        'start_date': start
    }
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)