from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home-page"),
    path('about/', aboutUs, name="about-page"),
    path('contact/', contact, name="contact-page"),
    path('showcontact/', showContact, name='showcontact-page'),
    path('register/', userRegist, name="register-page"),
    path('profile/', userProfile, name="profile-page"),
    path('editprofile/', editProfile, name="editprofile-page"),
    path('action/<int:cid>/', actionPage, name="action-page"),
    path('addproduct/', addProduct, name="addproduct-page"),
    path('product/<int:product_id>/', productDetail, name='product-detail'),
    path('add-to-basket/<int:product_id>/', add_to_basket, name='add-to-basket'),  # Add product to basket
    path('view-basket/', view_basket, name='view-basket'),  # View all items in the basket
    path('basket/delete/<int:item_id>/', delete_basket_item, name='delete_basket_item'),  # Delete item from basket
    path('basket/update/<int:item_id>/', update_basket_item, name='update_basket_item'),
    path('add-credit-card/', add_credit_card, name='add_credit_card'),
    path('select-credit-card/', select_credit_card, name='select_credit_card'),
    path('update-credit-card/<int:card_id>/', update_credit_card, name='update_credit_card'),
    path('delete-credit-card/<int:card_id>/', delete_credit_card, name='delete_credit_card'),
    path('confirm_payment/', confirm_payment, name='confirm_payment'),
    path('all_bills/', all_bills, name='all_bills'),
    path('bill/<int:bill_id>/', bill_detail, name='bill_detail'),
    path('admin_all_bills/', admin_all_bills, name='admin_all_bills'),
    path('admin_bill/<int:bill_id>/', admin_bill_detail, name='admin_bill_detail'),
]
