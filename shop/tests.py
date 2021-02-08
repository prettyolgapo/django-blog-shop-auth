from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Product, Cart, OrderItem, Point
from shop.forms import CartForm


class ProductTests(TestCase):
    def setUp(self):
        # run before each test
        Product.objects.create(name="lion", price=1, description="description1")
        Product.objects.create(name="cat", price=2, description="description2")
        Product.objects.create(name="fin", price=3, description="description3")
        Product.objects.create(name="pin", price=4, description="description4")

    def test_shop_list(self):
        """
            Shows shop list
        """
        response = self.client.get(reverse('shop:list'))
        # error: 'Trying to compare non-ordered queryset against more than one ordered values' is solved 'ordered=False'
        self.assertQuerysetEqual(list(response.context['products']), ['<Product: lion>',
                                                                      '<Product: cat>',
                                                                      '<Product: fin>',
                                                                      '<Product: pin>'])

    def test_product_detail(self):
        """
             Displayed product detail by id
        """
        lion = Product.objects.get(name="lion")
        response = self.client.get(reverse('shop:product-details', args=(lion.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], lion)

    def test_search(self):
        """
           Displayed search results from response
        """
        # response = self.client.get('/shop/search/?q=cat')
        response = self.client.get(reverse('shop:search-results'), {'q': 'cat'})
        self.assertQuerysetEqual(list(response.context['object_list']), ['<Product: cat>'])


class CartTests(TestCase):
    def setUp(self):
        Cart.objects.create(order_id="GDqeCrnD",
                            first_name="John",
                            active=False,
                            payment_type=0,
                            total=3.00)
        Cart.objects.create(order_id="RDasCRyu",
                            first_name="Peter",
                            active=False,
                            payment_type=1,
                            total=32.00)
        Cart.objects.create(active=True,
                            payment_type=1,
                            total=32.00)
        Point.objects.create(name='here',
                             address='address')
        # Cart.objects.create(name="pin", price=4, description="description4")

    def test_form_saves_values_to_instance_cart_on_save(self):
        """
            test form saves name, payment_type, values to corresponding Cart object
            when commiting form
            Also shows total value - todo
        """
        cart_setup = Cart.objects.get(active=True)
        point_setup = Point.objects.get(name='here')
       # valid_pk = Point.objects.all()[0].pk
        cart_form = CartForm(instance=cart_setup, data={'first_name': 'has_changed', 'last_name': 'has_changed_too',
                                                        'email': 'test@test.com', 'payment_type': 1, 'point': point_setup.pk,
                                                        })

        if cart_form.is_valid():
            cart_assert = cart_form.save()
            self.assertEquals(cart_assert.first_name, "has_changed")
            self.assertEquals(cart_assert.last_name, "has_changed_too")
            self.assertEquals(cart_assert.email, "test@test.com")
            self.assertEquals(cart_assert.point, point_setup)
            self.assertEquals(cart_assert.payment_type, 1)
        else:
            self.fail("cart_form not valid")

    def test_no_active(self):
        """
            Check if order closed (no more Active=True)
        """
        cart_setup = Cart.objects.get(active=True)
        response = self.client.get(reverse('shop:thanks'))
        cart_response = response.context['order']
        self.assertNotEquals(cart_response.active, cart_setup.active)
        self.assertEqual(response.status_code, 200)


class OrderItemTests(TestCase):
    def setUp(self):
        # run before each test
        Product.objects.create(name="lion", price=1, description="description1")
        product1 = Product.objects.create(name="cat", price=20, description="description2")
        product = Product.objects.create(name="fin", price=3, description="description3")
        Product.objects.create(name="pin", price=4, description="description4")

        current_cart = Cart.objects.create(order_id="GDqeCrnD",
                                           first_name="John",
                                           active=True,
                                           payment_type=0,
                                           total=13.00)
        Cart.objects.create(order_id="RDasCRyu",
                            first_name="Peter",
                            active=False,
                            payment_type=1,
                            total=32.00)

        OrderItem.objects.create(
            product=product,
            quantity=100,
            price=100*product.price,
            cart=current_cart
        )
        OrderItem.objects.create(
            product=product1,
            quantity=100,
            price=100*product1.price,
            cart=current_cart
        )

    def test_add_quantity(self):
        """
            Check adding item if same Product already exists in Cart, Cart exists too
        """
        adding_product = Product.objects.get(name="fin")
        adding_item = OrderItem.objects.get(product=adding_product)
        self.client.get(reverse('shop:add-to-cart', args=(adding_product.pk,)))
        added_item = OrderItem.objects.get(product=adding_product)
        self.assertEquals(added_item.quantity - adding_item.quantity, 1)

    def test_add_item(self):
        """
            Check adding item if Product doesn't exist in Cart, Cart exists
        """
        adding_product = Product.objects.get(name="pin")
        # No OrderItem containing "product=adding_product".  This should raise a Http404 error.
        with self.assertRaises(Http404):
            get_object_or_404(OrderItem, product=adding_product)
        # adding_item = get_object_or_404(OrderItem, product=adding_product)
        # self.assertEquals(adding_item.status_code, 404)
        self.client.get(reverse('shop:add-to-cart', args=(adding_product.pk,)))
        added_item = OrderItem.objects.get(product=adding_product)
        self.assertEquals(added_item.quantity, 1)

    def test_cart_total(self):
        """
             Checks the total counting the amount of the cost each Item in Cart
        """
        response = self.client.get(reverse('shop:cart'))
        self.assertEquals(response.context['total'], Decimal('2300.00'))


    def test_update_cart(self):
        """
             Check: Change Item quantity
        """
        product = Product.objects.get(name="fin")
        updating_item = OrderItem.objects.get(product=product)
        self.client.post(reverse('shop:cart-update', args=(updating_item.pk,)), {'quantity': '5'})
        updated_item = OrderItem.objects.get(product=product)
        self.assertEquals(updated_item.quantity, 5)

    def test_delete_item(self):
        """
             Check: Item has been deleted
        """
        product = Product.objects.get(name="cat")
        order_item = get_object_or_404(OrderItem, product=product)
        self.client.get(reverse('shop:item-remove', args=(order_item.pk,)))
        with self.assertRaises(Http404):
            get_object_or_404(OrderItem, product=product)