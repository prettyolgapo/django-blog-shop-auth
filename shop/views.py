from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, OrderItem, Cart
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import FormView, View
from shop.forms import CartForm
from django.utils.crypto import get_random_string
from .models import PAYMENT_CHOICES
from django.contrib.auth.decorators import login_required


def shop_list(request):
    # try:
    products = Product.objects.all()
    return render(request, "shop/list.html", {'products': products})
    # except Product.DoesNotExist:
    #     return render(request, "shop/empty-list.html")


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product-details.html', {'product': product})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        current_cart = Cart.objects.get(active=True)
    except Cart.DoesNotExist:
        current_cart = Cart.objects.create(
            active=True,
            order_id=get_random_string(8)
        )
    current_cart.save()
    try:
        preexisting_order = OrderItem.objects.get(product=product, cart=current_cart)
        preexisting_order.quantity += 1
        preexisting_order.price = int(preexisting_order.quantity)*int(product.price)
        preexisting_order.Cart = current_cart
        preexisting_order.save()
    except OrderItem.DoesNotExist:
        new_order = OrderItem.objects.create(
            product=product,
            quantity=1,
            price=product.price,
            cart=current_cart
        )
        new_order.save()
    #messages.success(request, "Cart updated!")
    return redirect('shop:list')


def cart(request):
    try:
        cart_detail = Cart.objects.get(active=True)
        order_items = OrderItem.objects.filter(cart=cart_detail)
        tmp_total = OrderItem.objects.filter(cart=cart_detail).aggregate(Sum('price'))
        cart_detail.total = tmp_total['price__sum']
        cart_detail.save()
        return render(request, 'shop/cart.html', {'order_items': order_items, 'total': cart_detail.total})
    except Cart.DoesNotExist:
        return render(request, 'shop/empty-cart.html')


def cart_update(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    quantity = request.POST.get('quantity', None)
    order_item.quantity = quantity
    order_item.price = int(order_item.quantity)*int(order_item.product.price)
    order_item.save()
    return redirect('shop:cart')


def item_remove(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order_item.delete()
    return redirect('shop:cart')


class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/search-results.html'

    # queryset = Post.objects.filter(name__icontains='Boston')

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        return object_list


# class CheckoutView(FormView):
#     template_name = 'shop/checkout.html'
#     form_class = CartForm
#     success_url = '/shop:thanks/'
#
#     def form_valid(self, form):
#         cart_detail = Cart.objects.get(active=True)
#         f = CartForm(self.request.POST, instance=cart_detail)
#         f.save()
#         return super().form_valid(form)


class CheckoutView(View):

    def get(self, request, *args, **kwargs):
        try:
            cart_detail = Cart.objects.get(active=True)
            order_items = OrderItem.objects.filter(cart=cart_detail)
            total = cart_detail.total
            if not request.user.is_authenticated:
                cart_detail.customer = None
                cart_detail.first_name = None
                cart_detail.last_name = None
                cart_detail.email = None
            else:
                cart_detail.customer = request.user
                cart_detail.first_name = request.user.first_name
                cart_detail.last_name = request.user.last_name
                cart_detail.email = request.user.email
            cart_detail.save()
            cart_detail = Cart.objects.get(active=True)
            form = CartForm(instance=cart_detail)
            context = {'form': form, 'total': total, 'order_items': order_items}

            return render(request, 'shop/checkout.html', context)
        except Cart.DoesNotExist:
            return redirect('shop:list')

    def post(self, request, *args, **kwargs):
        try:
            cart_detail = Cart.objects.get(active=True)
            total = cart_detail.total
            order_items = OrderItem.objects.filter(cart=cart_detail)
            form = CartForm(self.request.POST, instance=cart_detail)
            context = {'form': form, 'total': total, 'order_items': order_items}
            if form.is_valid():
                form.save()
                return redirect('shop:thanks')
            return render(request, 'shop/checkout.html', context)
        except Cart.DoesNotExist:
            return redirect('shop:list')


def thanks(request):
    try:
        #cart_detail = get_object_or_404(Cart, active=True)
        cart_detail = Cart.objects.get(active=True)
        cart_detail.active = False
        choices = PAYMENT_CHOICES
        choice_pay = cart_detail.payment_type
        choice_pay = dict(choices)[choice_pay]
        cart_detail.save()
        return render(request, 'shop/thanks.html', {'order': cart_detail, 'choice_pay': choice_pay})
    except Cart.DoesNotExist:
        return redirect('shop:list')


def order_complete(request):
    return redirect('shop:list')
