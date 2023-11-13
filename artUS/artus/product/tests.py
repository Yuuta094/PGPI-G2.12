from django.test import TestCase, Client
from django.urls import reverse
from .models import Obra
from django.shortcuts import render,get_object_or_404
class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Obra.objects.create(name='Test Product', price=10.99, quantity=5, category='Abstracto', 
                                           author='Alex Martínez', description='Fusión de colores abstractos',
                                           manufacturer='Alex Martínez', image='product/abstracto.jpg')

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
        self.product = Obra.objects.create(name='Fusión Abstracta', price=110.99,quantity=5, category='Abstracto', 
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
        obras = Obra.objects.filter(name__icontains='Fusión', category__icontains='Abstracto', author__icontains='Alex', price__gte='10', price__lte='120')
        for obra in obras:
            self.assertContains(response, obra.name)