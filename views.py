import json
import stripe

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from django.http.response import Http404

from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import UserProfile
from .models import *
from .forms import UserForm
from .serializers import OrderListSerializer

# Create your views here.
from django.views import View

TEMPLATE_CODE = 'temp1'

DOMAIN_URL = 'http://127.0.0.1:8000/'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        print("returning REAL_IP")
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        print("returning REMOTE_ADDR")
        ip = request.META.get('REMOTE_ADDR')
    return ip


def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    for x in unique_list:
        print(x)

    return unique_list


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(text_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    print(the_data)
    return HttpResponse(the_data, content_type='application/json')


class ShopHomeView(View):
    template_name = TEMPLATE_CODE + '/index.html'

    def get(self, request):
        categories = ProductCategory.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, self.template_name, context=context)


class ShopProductsView(View):
    template_name = 'common/shop_page/shop-horizontal-filter.html'
    model = Course
    ordering = ['-created_at']

    def get(self, request):
        context = {}
        product_list = Course.objects.filter(in_stock=True, is_active=True).exclude \
            (product_sub_category__sub_category_name__in=["Enrollment Package", "Additional Enrollment Package"])
        categories = ProductCategory.objects.all()
        variations = ProductVariationAttribute.objects.all()
        filter_data = querydict_to_dict(self.request.GET)
        variation = list(filter_data.values())
        if len(variation) == 0:
            print('executed')
            un_products = Course.objects.filter(in_stock=True, is_active=True).exclude(
                product_sub_category__sub_category_name__in=["Enrollment Package",
                                                             "Additional Enrollment Package"]).order_by('-created_at')
            print(un_products)
        else:
            un_products = Course.objects.filter(product_variation_attribute_values__variation_value1__in=variation,
                                                in_stock=True, is_active=True).exclude(
                product_sub_category__sub_category_name__in=["Enrollment Package",
                                                             "Additional Enrollment Package"]).order_by('-created_at')

        page = request.GET.get('page')
        page = page or 1
        paginate = request.GET.get('paginate')
        paginate = paginate or 12
        paginator = Paginator(un_products, paginate)

        products = paginator.get_page(page)

        context['filter'] = filter_data
        context['products'] = product_list
        context['categories'] = categories
        context['variations'] = variations
        context['variation_products'] = products
        context['filter_data'] = filter_data
        return render(request, self.template_name, context=context)


class ShopCategoriesView(View):
    template_name = 'common/shop_page/shop-list.html'

    def get(self, request):
        product_list = Course.objects.all()
        categories = ProductCategory.objects.all()
        context = {
            'products': product_list,
            'categories': categories,
        }
        return render(request, self.template_name, context=context)


class ShopSubCategoryView(View):
    template_name = 'common/shop_page/shop-list.html'

    def get(self, request, category_slug):
        product_list = Course.objects.filter(product_sub_category__sub_category_name=category_slug).order_by(
            '-created_at')
        paginate = request.GET.get('paginate')
        paginate = paginate or 12
        page = request.GET.get('page')
        page = page or 1
        paginator = Paginator(product_list, paginate)
        products = paginator.get_page(page)
        categories = ProductCategory.objects.all()
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, self.template_name, context=context)


class ShopCategoryView(View):
    template_name = 'common/shop_page/shop-list_category.html'

    def get(self, request, category_slug):
        context = {
            # 'products': product_list,
            # 'categories': categories,
        }
        return render(request, self.template_name, context=context)


class ShopProductDetailView(View):
    template_name = 'common/product_pages/product.html'

    def get(self, request, slug):
        product_detail = Course.objects.get(slug=slug)
        product_variations = ProductVariationAttribute.objects.all()
        for a in product_variations:
            print(a)
            for b in a.product_variation_value.filter(product__slug=slug):
                print(b.variation_value1)
        try:
            order_list_count = OrderList.objects.get(product_id__slug=slug, order_id__order_status=False)
        except ObjectDoesNotExist:
            order_list_count = 1
        except MultipleObjectsReturned:
            order_list_count = 1
        context = {
            'product_detail': product_detail,
            'order_list_count': order_list_count,
            'product_variations': product_variations
        }
        return render(request, self.template_name, context=context)


class ShopCartView(View):
    template_name = 'common/product_pages/cart.html'

    def get(self, request):
        try:
            orders = ShopOrder.objects.get(order_status=False, order_user=request.user)
        except ShopOrder.DoesNotExist:
            return redirect('shop-products')
        order_lists = OrderList.objects.filter(order_id__order_user=request.user, order_id__order_status=False)
        # print(f"order total: {orders.get_order_sub_total}")
        print(f" order sub total {orders.get_order_sub_total}orders.get_order_sub_total")
        context = {
            'order': orders,
            'order_lists': order_lists
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        order, status = ShopOrder.objects.get_or_create(order_status=False, order_user=request.user)
        order_list, status = OrderList.objects.get_or_create(order_id=order)
        context = {

            'order_lists': order_list
        }
        return render(request, self.template_name, context=context)


class ShopCheckoutView(View):
    template_name = 'common/product_pages/checkout.html'

    def get(self, request):
        payment_methods = PaymentType.objects.all()
        try:
            order = ShopOrder.objects.get(order_status=False, order_user=request.user)
        except ShopOrder.DoesNotExist:
            order = None
        for a in payment_methods:
            print(a.id)
            print(a.payment_gateway)
            print(a.payment_gateway_desc)
        order_lists = OrderList.objects.filter(order_id=order)
        for order_list in order_lists:
            print(order_list.get_item_total)

        context = {
            'order': order,
            'order_lists': order_lists,
            'payment_methods': payment_methods
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        order_id = request.POST.get('order-id')
        print(f"Prder id {order_id}")
        order = ShopOrder.objects.get(id=order_id)
        order_lists = OrderList.objects.filter(order_id=order)
        b_first_name = request.POST.get('first-name')
        b_last_name = request.POST.get('last-name')
        b_company_name = request.POST.get('company-name')
        b_country = request.POST.get('country')
        b_address_1 = request.POST.get('address1')
        b_address_2 = request.POST.get('address2')
        b_city = request.POST.get('city')
        b_state = request.POST.get('state')
        b_zip = request.POST.get('zip')
        b_phone = request.POST.get('phone')
        b_email = request.POST.get('email-address')
        payment_gateway = request.POST.get('payment-gateway')
        print(f"Payment Gateway: {payment_gateway}")
        print(b_email, b_first_name)
        request.session['order-id'] = order.id
        print(request.session['order-id'])
        order_address, status = Address.objects.get_or_create(order_id=order)
        order_address.billing_first_name = b_first_name
        order_address.billing_last_name = b_last_name
        order_address.billing_company_name = b_company_name
        order_address.billing_addr1 = b_address_1
        order_address.billing_addr2 = b_address_2
        order_address.billing_city = b_city
        order_address.billing_state = b_state
        order_address.billing_country = b_country
        order_address.billing_pincode = b_zip
        order_address.billing_phone = b_phone
        order_address.save()

        if int(payment_gateway) == 3:
            return redirect('shop:stripe-payment')

        else:
            order.order_status = False
            order.save()
            payment_id, status = Payments.objects.get_or_create(order_id=order)
            print(type(payment_id))
            print(f"paymen tt ype {payment_id.id}")
            payment_id.payment_type_id = int(payment_gateway)
            payment_id.payment_status = False
            payment_id.save()
            context = {
                'order': order,
                'order_address': order_address,
                'order_lists': order_lists

            }
            return render(request, 'common/product_pages/order.html', context=context)


class ShopMyAccountView(View):
    template_name = 'common/account.html'

    def get(self, request):
        return render(request, self.template_name)


class ShopAddCourseView(View):
    template_name = 'common/add course.html'

    def get(self, request):
        return render(request, self.template_name)


class ShopView(View):
    template_name = 'common/course.html'

    def get(self, request):
        return render(request, self.template_name)


class ShopShowalleLearningView(View):
    template_name = 'common/course.html'

    def get(self, request):
        return render(request, self.template_name)


class ShopStatusView(View):
    template_name = 'common/course.html'

    def get(self, request):
        return render(request, self.template_name)


class ShopWishListView(View):
    template_name = 'common/wishlist.html'

    def get(self, request):
        wishlist = WishlistModel.objects.filter(wishlist_user=request.user)
        context = {
            'product_lists': wishlist
        }
        return render(request, self.template_name, context=context)


class ShopSuccessView(View):
    template_name = 'common/product_pages/order.html'

    def get(self, request):
        return render(request, self.template_name)


class CustomerRegister(View):
    template_name = 'common/login.html'

    def get(self, request):
        form = UserForm()
        user_sponsor = request.session.get('sponsor')
        print(f"user sponsor id {user_sponsor}")
        context = {
            'form': form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('f-name')
        last_name = request.POST.get('l-name')
        user_sponsor = request.session.get('sponsor')
        print(f'user sponsor in post {user_sponsor}')
        if user_sponsor:
            print('if executed')
            try:
                print('try if executed')
                sponsor_fetched = User.objects.get(id=user_sponsor)
                print(f'try sponsor fetch {sponsor_fetched}')
            except User.DoesNotExist:
                print('exempt')
                sponsor_fetched = User.objects.get(id=1)
        else:
            sponsor_fetched = User.objects.get(id=1)
        user_id = f"CUSTID{abs(random.random() * 100000)}"
        user = User.objects.create_customer(email=email, user_id=user_id, password=password, sponsor=sponsor_fetched,
                                            sponsor_id=sponsor_fetched.id, first_name=first_name, last_name=last_name)
        logged_user = authenticate(email=email, password=password)
        if logged_user is not None:
            login(request, logged_user)
            return redirect('account:my_account')
        else:
            return redirect('shop:home')


class CustomerLogin(View):
    template_name = 'common/login.html'

    def get(self, request):
        form = UserForm()
        user_sponsor = request.session.get('sponsor')
        print(f"user sponsor id {user_sponsor}")
        context = {
            'form': form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        next_page = request.POST.get('next', '/')
        email = request.POST.get('sign-in-email')
        password = request.POST.get('sign-in-password')
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None and next_page is None:
            msg = login(request, user)
            print(msg)
            messages.success(request, "You have successfully logged in")
            return render(request, self.template_name)
        elif user is not None and next_page is not None:
            msg = login(request, user)
            print(msg)
            return redirect(next_page)
        else:
            error = user
            print('executed outside')
            context = {
                'form_errors': error
            }
            return render(request, self.template_name, context=context)


class AddToCart(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data.get('productId')
        qty = data.get('qty')
        variations = data.get('variations')
        print(product_id, qty, variations)
        print(request.user)
        product = Course.objects.get(id=product_id)
        order, status = ShopOrder.objects.get_or_create(order_user_id=request.user.id, order_status=False)
        order_item, status = OrderList.objects.get_or_create(order_id=order, product_id=product)
        order_item.product_count = qty
        order_item.save()

        return JsonResponse('success', safe=False)


class UpdateCart(View):
    def post(self, request):
        data = json.loads(request.body)
        order_list_id = data.get('orderListId')
        order_list_qty = data.get('orderListQty')
        print(order_list_qty, order_list_id)
        order_list_update = OrderList.objects.get(id=order_list_id)
        order_list_update.product_count = order_list_qty
        order_list_update.save()
        if int(order_list_qty) < 1:
            order_list_update.delete()

        return JsonResponse('success', safe=False)


class ShopMiniCart(APIView):

    def get(self, request):
        order_fo_list = OrderList.objects.select_related().filter(order_id__order_user=request.user,
                                                                  order_id__order_status=False)
        order_obj = OrderListSerializer(order_fo_list, many=True, context={"request": request})
        return Response(order_obj.data)


class UpdateWishListView(View):
    def post(self, request):
        global wish_list, _
        data = json.loads(request.body)
        print(data)
        product_id = data['productId']
        action = data['action']
        print(data)
        print(product_id)
        if action == "add":
            wish_list, status = WishlistModel.objects.get_or_create(wishlist_user=request.user,
                                                                    wishlist_product_id=product_id)
        elif action == "remove":
            wish_list = WishlistModel.objects.get(wishlist_product_id=product_id)
            wish_list.delete()

        print(wish_list, _)
        return JsonResponse('success', safe=False)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    print(request.method)
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        print(domain_url)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            # form = request.session['form']
            # print(form)
            # package_purchase_transaction_id = request.session['package_purchase_id']
            order_id = request.session.get('order-id')
            print(order_id)
            order_obj = ShopOrder.objects.get(id=order_id)
            print(order_obj)
            print(request.user.email)
            user_fetched = User.objects.get(email=request.user.email)
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                client_reference_id=user_fetched.id,
                customer_email=user_fetched.email,
                metadata={
                    'first_name': str(user_fetched.first_name),
                    'last_name': str(user_fetched.last_name),
                    'package': str(order_obj.id),
                    'order_id': str(order_obj.id),
                },
                line_items=[
                    {
                        'name': str(f"User {order_obj.order_user.first_name}:  {order_obj.id}"),
                        "quantity": 1,
                        'currency': 'usd',
                        'amount': int(order_obj.get_total_sum * 100),
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(View):
    template_name = 'common/product_pages/order.html'

    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session_id = request.GET.get('session_id')
        stripe_response = stripe.checkout.Session.retrieve(
            session_id,
        )
        print(stripe_response)
        response_dict = {
            'customer': stripe_response['customer'],
            'subscription_id': stripe_response['subscription'],
            'id': stripe_response['id']
        }
        order_id = stripe_response['metadata']['order_id']
        order_fetched = ShopOrder.objects.get(id=order_id)
        order_fetched.order_status = True
        order_fetched.save()
        payment_id, status = Payments.objects.get_or_create(order_id=order_fetched)
        user_obj, status = UserProfile.objects.get_or_create(profile_user=order_fetched.order_user)
        user_obj.payment_id = stripe_response['customer']
        payment_type = PaymentType.objects.get(id=3)
        payment_id.payment_customer = order_fetched.order_user
        payment_id.payment_type = payment_type
        payment_id.gateway_response = response_dict
        payment_id.payment_status = True
        payment_id.save()
        user_obj.save()
        context = {
            'data': request.META,
            'stripe_response': stripe_response,
            'order': order_fetched,
        }
        return render(request, self.template_name, context=context)


class CancelledView(TemplateView):
    template_name = 'common/product_pages/order.html'


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


class StripePaymentPage(View):
    template_name = 'common/stripe-payment.html'

    def get(self, request):
        print(request)
        print(request.META)
        return render(request, self.template_name)


class CouponCodeView(View):

    def post(self, request):
        global coupon_code_value, coupon_code_type, order_fetch
        coupon_code_value = 0
        coupon_code_type = ''
        data = json.loads(request.body)
        coupon_code = data['coupon-code']
        order_id = data['order-id']
        print(coupon_code)
        print(order_id)
        try:
            coupon_check = CouponCodeModel.objects.get(coupon_code=coupon_code)
            order_fetch = ShopOrder.objects.get(id=order_id)
            order_credits, status = ShopOrderCredits.objects.get_or_create(credit_order=order_fetch)
            order_credits.credit_note = f"Discount Coupon applied for User {request.user} with Coupon Code {coupon_check.coupon_code} applied for the Order id: {order_fetch.id} "
            order_credits.credit_type = "Discount Coupon"
            coupon_check.applied_order.add(order_fetch)
            coupon_check.save()
            coupon_code_status = "Valid"
            if coupon_check.coupon_amount:
                coupon_code_type = 'flat'
                coupon_code_value = coupon_check.coupon_amount
                order_fetch.order_credits = coupon_check.coupon_amount
                order_credits.credit_value = coupon_check.coupon_amount
                order_credits.save()
                order_fetch.save()
            else:
                coupon_code_type = 'perc'
                coupon_code_value = coupon_check.coupon_percent
                order_fetch.order_credits = order_fetch.get_order_sub_total * coupon_check.coupon_percent / 100
                order_credits.credit_value = order_fetch.get_order_sub_total * coupon_check.coupon_percent / 100
                order_fetch.save()
                order_credits.save()

        except CouponCodeModel.DoesNotExist:
            coupon_code_status = "Invalid"

        context = {
            'coupon_code_status': coupon_code_status,
            'coupon_value': coupon_code_value,
            'coupon_code_type': coupon_code_type

        }
        return JsonResponse(context, safe=False)


class ReplicatedUrlView(View):
    template_name = 'temp1/index.html'

    def get(self, request, username):
        user = get_object_or_404(User, user_id=username)
        print(user)
        request.session['sponsor'] = user.id
        url_tracking(request, username)
        return render(request, self.template_name)


def url_tracking(request, username):
    try:
        redirect_url = PromotionalPagesModel.objects.get(page_url=username)
        browser_value = request.META
        referrer = request.META.get('HTTP_REFERER')
        user_host = request.META.get('REMOTE_HOST')
        remote_user = request.META.get('REMOTE_USER')
        request_method = request.META.get('REQUEST_METHOD')
        user_ip = request.META.get('REMOTE_ADDR')
        print(user_ip)
        print(request)

        # Device Check

        is_mobile = request.user_agent.is_mobile
        is_tablet = request.user_agent.is_tablet
        is_touch_capable = request.user_agent.is_touch_capable
        is_pc = request.user_agent.is_pc
        is_bot = request.user_agent.is_bot

        # Accessing user agent's browser attributes
        browser = request.user_agent.browser
        browser_family = request.user_agent.browser.family
        browser_version = request.user_agent.browser.version
        browser_version_string = request.user_agent.browser.version_string

        # Operating System properties
        system = request.user_agent.os
        system_family = request.user_agent.os.family
        system_version = request.user_agent.os.version
        system_version_string = request.user_agent.os.version_string

        # Device properties
        device_type = request.user_agent.device
        device_family = request.user_agent.device.family

        # Country Check

        try:
            remote_ip = get_client_ip(request)
            g = GeoIP2()
            if remote_ip:
                city = g.city(remote_ip)
                country = g.country_code(remote_ip)
                region = g.coords(remote_ip)
        except GeoIP2Exception:
            city = ""
            country = ""
            region = ""

        short_url = PromotionalPagesModel.objects.get(page_url=username)

        redirect_request = UrlRequests.objects.create(request_short_url=short_url, request_meta=browser_value,
                                                      remote_ip=remote_ip, is_mobile=is_mobile, is_tablet=is_tablet,
                                                      is_touch_capable=is_touch_capable, is_pc=is_pc, is_bot=is_bot,
                                                      browser=browser, browser_family=browser_family,
                                                      browser_version=browser_version,
                                                      browser_version_string=browser_version_string,
                                                      system_os=system, system_os_family=system_family,
                                                      system_os_version=system_version,
                                                      system_os_version_string=system_version_string,
                                                      device_type=device_type, device_family=device_family,
                                                      ip_country=country, ip_city=city, ip_region=region,
                                                      referrer=referrer, remote_user=remote_user,
                                                      user_host=user_host,
                                                      request_method=request_method)

        if "http://" in redirect_url.page_redirect_url or "https://" in redirect_url.page_redirect_url:
            url_redirect = redirect_url.page_redirect_url
        else:
            url_redirect = 'https://{0}'.format(redirect_url.page_redirect_url)
            # Tracker.objects.create_from_request(request, redirect_request)
    except PromotionalPagesModel.DoesNotExist:
        try:
            user = User.objects.get(user_id=username)
            redirect_url = PromotionalPagesModel.objects.create(page_created_user=user, page_url=user.user_id,
                                                                page_title="Main Replicated Url",
                                                                page_redirect_url=user.user_id,
                                                                page_status=True)

            if "http://" in redirect_url.page_redirect_url or "https://" in redirect_url.page_redirect_url:
                url_redirect = redirect_url.page_redirect_url
            else:
                url_redirect = 'https://{0}'.format(redirect_url.page_redirect_url)
                # Tracker.objects.create_from_request(request, redirect_request)
        except User.DoesNotExist:
            raise Http404("User Page Requested Does Not Exist")
    return redirect(url_redirect)


