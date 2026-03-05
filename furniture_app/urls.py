from django.urls import path
from.import views
from.views import *
urlpatterns=[
    path('',views.index,name='index'),
    path("login/",views.login,name='login'),
    path('registration/', views.registration, name='registration'),
    path('renter/',views.renter,name='renter'),
    path('seller/',views.seller,name='seller'),

    # Admin #
    path('admin_index/',views.admin_index,name='admin_index'),
    path('view-users/', views.view_users, name='view_users'),
    path('block_user/', views.block_user, name='block_user'),
    path('unblock_user/', views.unblock_user, name='unblock_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('manage_renter/',views.manage_renter,name='manage_renter'),
    path('approve_renter/',views.approve_renter,name='approve_renter'),
    path('reject_renter/',views.reject_renter,name='reject_renter'),
    path('manage_seller/',views.manage_seller,name='manage_seller'),
    path('approve_seller/',views.approve_seller,name='approve_seller'),
    path('reject_seller/',views.reject_seller,name='reject_seller'),
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/edit/<int:category_id>/", views.edit_category, name="edit_category"),
    path("categories/delete/<int:category_id>/", views.delete_category, name="delete_category"),




    # User #
    path("user_index/",views.user_index,name='user_index'),
    path('profile_settings/',views.profile_settings,name='profile_settings'),
    path('profile_edit/',views.profile_edit,name='profile_edit'),
    path('product_details/<int:id>/', views.product_details, name='product_details'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/', views.view_furniture, name='furniture'),
    path('rental_products/', views.rental_products, name='rental_products'),
    path('buy_now/<str:product_type>/<int:product_id>/', buy_now, name='buy_now'),
    path('order/confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('notifications/', views.user_notifications_view, name='user_notifications'),




    # seller #
    path("seller_index/",views.seller_index,name="seller_index"),
    path("add_furniture/",views.add_furniture,name='add_furniture'),
    path('manage_products/', views.manage_products, name='manage_products'),
    path('delete-furniture/<int:product_id>/', views.delete_furniture, name='delete_furniture'),
    path('edit-products/<int:product_id>/', views.edit_products, name='edit_products'),
    path('seller_profile/',views.seller_profile,name='seller_profile'),
    path('seller_edit/',views.seller_edit,name='seller_edit'),
    path('seller/bookings/', views.seller_bookings_view, name='seller_bookings'),





    # Renter #

    path('renter_index/',views.renter_index,name='renter_index'),
    path('add_renter_furniture/',views.add_renter_furniture,name='add_renter_furniture'),
    path('manage_products_renter/',views.manage_products_renter,name='manage_products_renter'),
    path('delete_furniture_renter/',views.delete_furniture_renter,name='delete_furniture_renter'),
    path('edits_products_renter/',views.edit_products_renter,name='edits_products_renter'),
    path('renter_profile/',views.renter_profile,name='renter_profile'),
    path('renter_edit/',views.renter_edit,name='renter_edit'),
    path('renter/bookings/', views.renter_bookings_view, name='renter_bookings_view'),
    
    

    
    # path('manage_shops',views.manage_shops , name='manage_shops'),
    
    # path('delete/<int:shop_id>/',views.delete_shop, name='delete_shop'),
    

]   
