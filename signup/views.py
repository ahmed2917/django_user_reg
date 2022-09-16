
from email import message
from lib2to3.pytree import Base
from rest_framework.generics import GenericAPIView
from .models import User_details
from .serializers import SignupSerializer, SignInSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions, BasePermission
from signup import serializers

# Create your views here  .
class UserWritePermissions(BasePermission):
    message = "Editing user is restricted to admin only"
    def has_object_permission(self, request, view, obj):
        #safe methods are get options or heads / only for readonly
        if request.method in SAFE_METHODS:
            return True

class UserList(GenericAPIView, ListModelMixin):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = SignupSerializer 

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)  

class UserCreate(CreateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer 
      
    # def create(self, *args, **kwargs):
    #     return super().create(*args,**kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class UserUpdate(UpdateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer 
    
    def put(self, request, *args, **kwargs):
        kwargs.update({"partial":True})
        return super().update(request, *args, **kwargs)
    
# class UserLogin(CreateModelMixin, GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = LoginSerializer 
    
#     def post(self, request, *args, **kwargs):
#         print("asd",request.data, args, kwargs)
        
#         a = TokenObtainPairSerializer.validate(self, request.data)
#         return {}

# class UserLogin(CreateModelMixin, GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = SignInSerializer
#     def post(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)
        # print("asd",request.data, args, kwargs)
        # a = serializer_class.validate(self, request.data)
        # data = super().validate(attrs)
    # Replace the serializer with your custom

class SigninView(APIView):
    def post(self,*args,**kwargs):
        print("request.data",self.request.data)
        serializer=SignInSerializer(data=self.request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors)


