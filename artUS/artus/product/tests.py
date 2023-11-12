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