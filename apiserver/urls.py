from . import views
from django.urls import path


urlpatterns = [
    path('',views.index,name='index'),
    path('explore_menu/', views.Explore_menu_serve, name='Explore_menu_serve'),
    path('test/',views.jsonresponse_test,name='jsonresponse_test'),
    path('itemList/', views.itemList, name='itemList'),
    path('cartData/', views.cartData, name='cartData'),
    path('login/', views.loginUser, name="login"),
    path('register/', views.RegisterUser, name='RegisterUser'),
    path('logout/', views.LogoutUser, name='LogoutUser'),
    path('addressget/',views.AddressAPI,name="AddressAPI"),
    path('checkAuth/', views.check_auth_view, name='checkAuth'),
    path('profileupdate/',views.getProfile,name="getProfile"),
    path('payment/', views.payment_view, name='payment_view'),
    path('success/', views.success, name='success'),
#     path('testuser/', views.create_user_profile,name="create_user_profile"),
 ]
