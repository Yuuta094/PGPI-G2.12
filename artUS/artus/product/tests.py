from django.test import TestCase, Client
from django.urls import reverse
from .models import Obra
from django.shortcuts import render,get_object_or_404
class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Obra.objects.create(name='Test Product', price=10.99,quantity=5)

    def test_detail_view(self):
        response = self.client.get(reverse('product:detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertTemplateUsed(response, 'product/detail.html')