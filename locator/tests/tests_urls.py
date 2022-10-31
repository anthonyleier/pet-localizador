import pytest
from django.urls import reverse
from django.test import TestCase


@pytest.mark.fast
class LocatorUrls(TestCase):
    def test_home(self):
        url = reverse('home')
        self.assertEqual(url, '/')

    def test_post(self):
        url = reverse('post', args=[2])
        self.assertEqual(url, '/posts/2')

    def test_search(self):
        url = reverse('search')
        self.assertEqual(url, '/posts/search')
