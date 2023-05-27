
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken,BlacklistedToken,OutstandingToken
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer,UserSerializer,UpdateUserSerializer,UserLoginSerializer,PropertySerializer,Favorite_Serializer
from django.contrib.auth import authenticate
from rest_framework import mixins

# from django.contrib.auth.models import User

from .models import User,Favorite
from rest_framework.generics import ListCreateAPIView
from rest_framework import status


class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "msg": "User Created Successfully.  Now perform Login to get your token",
        })

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Username or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


class LogoutUser(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self,request):
        try:
            refresh_token=request.data["refresh_token"]
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'msg':'Logout successfuly'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)







class UpdateProfileView(mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    lookup_field='pk'


    def get(self, request,pk):
        return self.retrieve(request)
    def put(self, request,*args, **kwargs):
        return self.update(request) 
    def patch(self, request,*args, **kwargs):
        return self.partial_update(request)
    def delete(self, request,*args, **kwargs):
        return self.destroy(request)


from .models import Image,Property
from .serializers import ImageSerializer
from django.http import JsonResponse





class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    name = 'Image-list'

class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    name = 'Image-detail'



from rest_framework.parsers import MultiPartParser ,FormParser
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

# from drf_yasg.utils import swagger_auto_schema



class PropertiesList(generics.ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    # filter_backends=(SearchFilter,)
    # search_fields=[
    #     'price',
    #     'city',
    #     'region',
         
    # ]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    # filterset_fields=['city']
    # filter_backends = []
    search_fields=['city','sell','region','price']
    # ordering_fields=['city']
# 
    # parser_classes=(MultiPartParser,FormParser)

    # def perform_create(self,serializer):
    #     images=self.request.FILES.getlist('image')
    #     print(images)
    #     property=serializer.save()
    #     for image in images:
    #         Image.objects.create(property=property,image=image)

    name = 'Properties-list'
class PropertiesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    name = 'Properties-detail'






class AddFavoriteView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=Favorite_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


class FavoriteList(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = Favorite_Serializer
    name = 'Favorite-list'