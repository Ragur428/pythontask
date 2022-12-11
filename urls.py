from django.conf.urls.static import static
from django.urls import path, re_path
from .views import *
from . import views
from django.conf import settings

app_name = 'shop'

urlpatterns = [

    path('', ShopHomeView.as_view(), name='home'),


    path('products/', ShopProductsView.as_view(), name='products'),
    path('product/<slug:slug>', ShopProductDetailView.as_view(), name='product-detail'),
    path('cart/', ShopCartView.as_view(), name='product-cart'),
    path('checkout/', ShopCheckoutView.as_view(), name='product-checkout'),
    path('my-account/', ShopMyAccountView.as_view(), name='product-my-account'),
    path('wishlist/', ShopWishListView.as_view(), name='wishlist'),
    path('login/', CustomerLogin.as_view(), name='login'),
    path('register/', CustomerRegister.as_view(), name='register'),
    path('addtocart/', AddToCart.as_view(), name='add-to-cart'),
    path('updatecart/', UpdateCart.as_view(), name='update-cart'),
    path('categories/', ShopCategoriesView.as_view(), name='categories'),
    path('categories/<str:category_slug>/', ShopCategoryView.as_view(), name='category'),
    path('category/<str:category_slug>/', ShopSubCategoryView.as_view(), name='sub-category'),
    path('cartlist/', ShopMiniCart.as_view(), name='shop-mini-cart'),
    # path('search/', include('haystack.urls')),
    path('search/autocomplete/', views.autocomplete, name='autocomplete'),
    path('updatewishlist/', UpdateWishListView.as_view(), name='update-wishlist'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session, name='stripe-checkout'),
    path('success/', SuccessView.as_view(), name='shop-stripe-success'),
    path('cancelled/', CancelledView.as_view()),
    path('webhook/', views.stripe_webhook),
    path('payment-stripe/', StripePaymentPage.as_view(), name='stripe-payment'),
    path('coupon/', CouponCodeView.as_view(), name='coupon'),
    re_path(r'^(?P<username>\w{0,50})/$', ReplicatedUrlView.as_view(), name='replicated-url'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


