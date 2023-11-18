from django.test import TestCase, Client
from django.urls import reverse
from .models import Artwork
from django.shortcuts import render,get_object_or_404


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Artwork.objects.create(name='Test Product', price=10.99,quantity=5)
        self.client.save()
        self.product.save()
    
    def tearDown(self):
        self.client = None
        self.product = None

    def test_detail_view(self):
        response = self.client.get(reverse('product:detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'product/detail.html')
    
    def test_detail_view_with_invalid_product(self):
        response = self.client.get(reverse('product:detail', args=[1000]))
        self.assertEqual(response.status_code, 404)
    
class ProductSearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Artwork.objects.create(name='Fusión Abstracta', price=110.99,quantity=5, category='Abstracto', 
                                           author='Alex Martínez', description='Fusión de colores abstractos',
                                           manufacturer='Alex Martínez', image='product/abstracto.jpg')
        
    def test_search_page_view(self):
        response = self.client.get(reverse('product:search_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/search.html')
        
    def test_search_specific_product(self):
        response = self.client.get(reverse('product:search'),{'q':'Fusión','category':'Abstracto','author':'Alex','min_price':'10','max_price':'120'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/search.html')
        obras = Artwork.objects.filter(name__icontains='Fusión', category__icontains='Abstracto', author__icontains='Alex', price__gte='10', price__lte='120')
        for obra in obras:
            self.assertContains(response, obra.name)
        

class ProductCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_view(self):
        response = self.client.post(reverse('product:new'), {'author': 'Test_author', 'name': 'New Product', 'description':'Test_description', 'price': 19.99, 'quantity': 3,  'manufacturer':'Test_manufacturer'})
        self.assertEqual(response.status_code, 302)  # 302 significa redirección después de una creación exitosa
        self.assertTrue(Artwork.objects.filter(name='New Product').exists())

class ProductUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Artwork.objects.create(name='Test Product', price=10.99, quantity=5)

    def test_update_view(self):
        response = self.client.post(reverse('product:edit', args=[self.product.id]), {'author': 'Update_author', 'name': 'Update Product', 'description':'Update_description', 'price': 15.99, 'quantity': 8,  'manufacturer':'Upadte_manufacturer'})
        self.assertEqual(response.status_code, 302)  # 302 significa redirección después de una actualización exitosa
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, 15.99)
        self.assertEqual(self.product.quantity, 8)

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Artwork.objects.create(name='Test Product', price=10.99, quantity=5)

    def test_delete_view(self):
        response = self.client.post(reverse('product:delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # 302 significa redirección después de un borrado exitoso
        self.assertFalse(Artwork.objects.filter(name='Test Product').exists())
