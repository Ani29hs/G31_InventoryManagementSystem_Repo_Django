from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),  # Homepage (Dashboard)
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("explain/", views.explain_view, name='explain'),
    path("main/", views.main_view, name='main'),
    path("products/", views.add_product_view, name='product'),
    path('product/<int:product_id>/delete/', views.delete_product_view, name='deleteproduct'),
    path('update/<int:product_id>', views.update_product_view, name='updateproduct'),
    path('profile/', views.profile_view, name='profile'),  
    path('transfer/', views.transfer_product_view, name='transferproduct'),
    path('warehouse/', views.warehouse_view, name='warehouse'),
    path('approve-transfers/', views.approve_transfers_view, name='approvetransfers'),
    path('warehouse-products/', views.warehouse_product_view, name='warehouse_products'),
    path('users/', views.user_list_view, name='user_list'),
    path('make-staff/<int:user_id>/', views.make_staff_view, name='make_staff'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('my_products_by_warehouse/', views.user_warehouse_product_view, name='user_warehouse'),
    path('aboutus/', views.about_us_view, name='aboutus')

    
]
