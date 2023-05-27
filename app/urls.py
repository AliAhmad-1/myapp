from django.urls import path,include,re_path
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="#"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )

from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from . import views
urlpatterns = [
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),


    path('login/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('login_user/', views.UserLoginView.as_view(), name='login'),
    path('register/',views.RegisterUser.as_view(),name='registeruser'),
    path('logout/',views.LogoutUser.as_view(),name='logout'),
    path('update_profile/<int:pk>/', views.UpdateProfileView.as_view(), name='auth_update_profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),






    path('properties/',views.PropertiesList.as_view(),name = 'property-list'),
    path('properties-detail/<int:pk>/',views.PropertiesDetail.as_view(),name='property-detail'),

    path('property_image/',views.ImageList.as_view(),name = 'property-image'),
    path('image-detail/<int:pk>/',views.ImageDetail.as_view(),name='image-detail'),



    path('favorites/add/',views.AddFavoriteView.as_view(),name='add_favorite'),
    path('favorites/',views.FavoriteList.as_view(),name = 'favorite-list'),



    
   #  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   #  re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   #  re_path(r'^redoc/$',schema_view.with_ui('redoc',cache_timeout=0),name=""),






    
]
