from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import *




class ProductViewTest(TestCase):
    def test_get_product(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')

        category = Category.objects.create(name='django')
        product_1 = Product.objects.create(
            title='Test Product1',
            category=category,
            image=uploaded,
            slug='product-2'
        )
        product_2 = Product.objects.create(
            title='Test Product2',
            category=category,
            image=uploaded,
            slug='product-2',
        )

        response = self.client.get(reverse('shop:products'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(list(response.context['products']), [product_1, product_2])
        self.assertEqual(response.context['products'].count(), 2)
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)

class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django1')
        product_1 = Product.objects.create(
            title='Test Product1',
            category=category,
            image=uploaded,
            slug='product-1'
        )
        response = self.client.get(reverse('shop:product_details', kwargs={'slug': 'product-1'}))

        self.assertEqual(200, response.status_code)

        self.assertEqual(response.context['product'], product_1)
        self.assertEqual(response.context['product'].slug, product_1.slug)

class CategoryDetailViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(name='test django', slug='test-category')

        self.product = Product.objects.create(
            title='Test Product',
            slug='test-product',
            category=self.category,
            image=uploaded,

        )
    def test_status_code(self):
        response = self.client.get(reverse('shop:category_list', kwargs={'slug': 'test-category'}))
        self.assertEqual(200, response.status_code)
    def test_template_used(self):
        response = self.client.get(reverse('shop:category_list', kwargs={'slug': 'test-category'}))

        self.assertTemplateUsed(response, 'shop/category_list.html')
    def test_context_data(self):
        response = self.client.get(reverse('shop:category_list', kwargs={'slug': 'test-category'}))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)




class TestLoginUser:

    # User is redirected to the shop page if already authenticated
    def test_redirect_if_authenticated(self, mocker):
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        from django.shortcuts import redirect
        from account.views import login_user

        request = RequestFactory().get('/login')
        request.user = mocker.Mock(is_authenticated=True)

        response = login_user(request)
        assert response.status_code == 302
        assert response.url == 'shop:shop'

    # User tries to login with an empty username or password
    def test_login_with_empty_credentials(self, mocker):
        from django.test import RequestFactory
        from django.contrib.messages.storage.fallback import FallbackStorage
        from account.views import login_user

        request = RequestFactory().post('/login', data={'username': '', 'password': ''})
        request.user = mocker.Mock(is_authenticated=False)
        messages = FallbackStorage(request)
        mocker.patch('django.contrib.messages.get_messages', return_value=messages)

        response = login_user(request)
        assert response.status_code == 302
        assert response.url == 'account:login'

    # User is authenticated and redirected to the dashboard upon successful login
    def test_successful_login_redirect(self, mocker):
        # Mocking necessary objects and methods
        mock_request = mocker.MagicMock()
        mock_user = mocker.MagicMock()
        mock_authenticate = mocker.patch('django.contrib.auth.authenticate', return_value=mock_user)
        mock_login = mocker.patch('django.contrib.auth.login')

        # Simulating POST request with valid credentials
        mock_request.method = 'POST'
        mock_request.POST.get.side_effect = lambda x: 'username' if x == 'username' else 'password'

        # Calling the function under test
        login_user(mock_request)

        # Assertions
        mock_authenticate.assert_called_once_with(mock_request, username='username', password='password')
        mock_login.assert_called_once_with(mock_request, mock_user)
        mock_request.method = 'GET'
        assert login_user(mock_request) == redirect('account:dashboard')

    # Login form is rendered correctly when the request method is GET
    def test_render_login_form_get(self, mocker):
        # Mocking necessary objects and methods
        mock_request = mocker.MagicMock()
        mock_request.method = 'GET'

        # Calling the function under test
        response = login_user(mock_request)

        # Assertions
        assert response.status_code == 200
        assert response.template_name == 'account/login/login.html'


