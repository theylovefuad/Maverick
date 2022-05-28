"""fuadfood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ast import Delete
from django.contrib import admin
from django.urls import path, include
from accounts.views import (login_view,
                            signup_view,
                            logout_view,
                            )
from main.views import (home_view,
                        menu_view,
                        food_detail_view,
                        cart_view,
                        add_reviews,
                        delete_order,
                        empty_cart,
                        search_view,
                        ItemCreateView,
                        ItemUpdateView,
                        order_summary,
                        order_item,
                        admin_view,
                        pending_orders,
                        update_status,
                        admin_dashboard
)
from accounts.views import (logout_view,
                            login_view,
                            signup_view)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/',login_view),
    path('logout/',logout_view, name='logout'),
    path('signup/',signup_view,),
    path('', home_view, name='home'),
    path('menu/',menu_view,),
    path('dishes/<int:id>/', food_detail_view),
    path('cart/',cart_view,name='cart'),
    path('dishes/<int:id>/review/',add_reviews,),
    path('delete_order/<int:id>',delete_order,),
    path('empty/',empty_cart,name='empty-cart'),
    path('search/',search_view,name='search'),
    path('create/', ItemCreateView.as_view(),name='item-create'),
    path('dishes/<int:id>/update',ItemUpdateView.as_view(),),
    path('checkout/',order_item),
    path('order_summary/',order_summary, name='order-summary'),
    path('admin_view/',admin_view, name='admin_view'),
    path('pending_orders/',pending_orders, name='pending_orders'),
    path('update_status/<int:id>',update_status,name='update_status'),
    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),

    path('admin/', admin.site.urls),

] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

