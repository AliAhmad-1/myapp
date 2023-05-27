
from rest_framework import  serializers

# from django.contrib.auth.models import User
from .models import User,Property,Image,Favorite
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model=User
        fields = ['username', 'password']



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(style={'input_type':'password'},write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True, required=True,validators=[validate_password])


    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email','phone_number')
        extra_kwargs = {
            'phone_number': {'required': True},

        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['phone_number'],

        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user



class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username','email','phone_number','profile_image','password')
        extra_kwargs = {
            # 'first_name': {'required': True},
            # 'last_name': {'required': True},
            # 'password':{'read_only':True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = (
         
        'property_id',
        'image',

    )

class PropertySerializer(serializers.ModelSerializer):
    # image=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='image-detail')
    image=ImageSerializer(many=True,read_only=True)
    uploaded_images=serializers.ListField(child=serializers.ImageField(max_length=1000000,allow_empty_file=False,use_url=False),write_only=True)
    class Meta:
        model = Property
        fields = (
        'user',
        'name',
        'price',
        'sell',
        'description',
        'city',
        'region',
        'image',
        'uploaded_images',
        
    )
        
    def create(self,validated_data):
        uploaded_images=validated_data.pop("uploaded_images")
        property_id=Property.objects.create(**validated_data)
        for image in uploaded_images:
            new=Image.objects.create(property_id=property_id,image=image)

        return property_id



class Favorite_Serializer(serializers.ModelSerializer):
    item=PropertySerializer()
    class Meta:
        model=Favorite
        fields=('id','user','item')

