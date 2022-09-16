from rest_framework import serializers
from signup.models import User_details
from django.contrib.auth.models import User
from .constants import GENDER_CHOICES
from rest_framework_simplejwt.tokens import RefreshToken
    
class SignInSerializer(serializers.ModelSerializer):
    username =serializers.CharField(required=True)
    password =serializers.CharField(required=True,write_only=True)
    access =serializers.CharField(read_only=True)
    refresh =serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['username','password','access','refresh']

    def validate(self, attrs):
        attrs=super().validate(attrs)
        try:
            user_Obj=User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"user":"Provided cred are not valid"})
        except User.MultipleObjectsReturned:
            raise serializers.ValidationError({"user":"Provided cred are not valid"})
        if user_Obj and user_Obj.check_password(attrs.get('password')):
            token=RefreshToken.for_user(user_Obj)
            attrs['access']=str(token.access_token)
            attrs['refresh']=str(token)
            return attrs
        else:
            raise serializers.ValidationError("Provided cred are not valid")

class SignupSerializer(serializers.ModelSerializer):
    contact_num=serializers.IntegerField(write_only=True)
    gender=serializers.ChoiceField(choices=GENDER_CHOICES,write_only=True)
    address=serializers.CharField(write_only=True)
    # password = serializers.CharField(write_only=True)
    user_detail=serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        super(SignupSerializer, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'pk'):
            self.fields['username'].required = False
    
    class Meta:
        model =User 
        fields = ["id","email",'first_name','last_name','password','username','contact_num','gender','address',"user_detail"]
    
    def validate(self, attrs):
        if attrs["first_name"] == attrs["last_name"]:
            raise serializers.ValidationError("first and last name cannot be same")
        return attrs
    
    def create(self, validated_data):
        gender=validated_data.pop("gender",'')
        address=validated_data.pop("address",'')
        contact_num=validated_data.pop("contact_num",'')

        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("email already exists")    

        user_obj=super(SignupSerializer,self).create({**validated_data})
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()

        data={"gender":gender,"address":address,"contact_num":int(contact_num)}

        user_=User_details(**data)
        user_.user_detail=user_obj
        
        user_.save()
        
        return user_obj
    
    def to_representation(self, instance):
        return super().to_representation(instance)
    
    def get_user_detail(self,obj):
        try:
            userObj=User_details.objects.get(user_detail__id=obj.id)
            return {"contact":userObj.contact_num,
                    "address":userObj.address,
                    "Gender":userObj.gender}
        except User_details.DoesNotExist:
            return {}
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)