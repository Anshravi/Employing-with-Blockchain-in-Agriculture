from django.urls import path

from . import views

urlpatterns = [
               path("", views.index, name="index"),
               path("index.html", views.index, name="index_html"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('RegisterAction', views.RegisterAction, name="RegisterAction"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('LoginAction', views.UserLogin, name="LoginAction"),
	       path('Logout', views.Logout, name="Logout"),
	       path('FarmerScreen.html', views.FarmerScreen, name="FarmerScreen"),
	       path('MillerScreen.html', views.MillerScreen, name="MillerScreen"),
	       path('DRSScreen.html', views.DRSScreen, name="DRSScreen"),
	       path('UploadCrop.html', views.UploadCrop, name="UploadCrop"),
	       path('UploadCropAction', views.UploadCropAction, name="UploadCropAction"),
	       path('FertilizerInfo.html', views.FertilizerInfo, name="FertilizerInfo"),
	       path('ViewOrdersForFarmer.html', views.ViewOrdersForFarmer, name="ViewOrdersForFarmer"),
	       path('BrowseProducts.html', views.BrowseProducts, name="BrowseProducts"),
	       path('SearchProductAction', views.SearchProductAction, name="SearchProductAction"),
	       path('PurchaseProducts.html', views.PurchaseProducts, name="PurchaseProducts"),
	       path('MillerSearchProductAction', views.MillerSearchProductAction, name="MillerSearchProductAction"),
	       path('SaleToConsumer.html', views.SaleToConsumer, name="SaleToConsumer"),
	       path('ConsumerSaleAction', views.ConsumerSaleAction, name="ConsumerSaleAction"),
	       path('BookOrder', views.BookOrder, name="BookOrder"),
	       path('MillerBookOrder', views.MillerBookOrder, name="MillerBookOrder"),
]