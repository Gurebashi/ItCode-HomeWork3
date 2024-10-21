from shop import factories, models
from django.urls import reverse
from django.test import TestCase


class ShopTest(TestCase):
    def setUp(self):
        self.picture = factories.PictureFactory()

    def test_picture_list(self):
        url = reverse('pictures_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pictures'].count(), models.Picture.objects.count())
        print(response.context['pictures'].count(), models.Picture.objects.count())

    def test_picture_detail(self):
        url = reverse('pictures_detail', kwargs={'pk': self.picture.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_picture_update(self):
        url = reverse('pictures_update', kwargs={'pk': self.picture.pk})
        old_title = self.picture.title
        old_history = self.picture.history
        response = self.client.post(url, {'title': 'new title', 'history': 'new history'})
        print(self.picture.title)
        self.assertEqual(response.status_code, 302)
        self.picture.refresh_from_db()
        print(self.picture.title)
        self.assertNotEqual(self.picture.title, old_title)
        self.assertNotEqual(self.picture.history, old_history)


    def test_picture_delete(self):
        url = reverse('pictures_delete', kwargs={'pk': self.picture.pk})
        old_title_count = models.Picture.objects.count()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertGreater(old_title_count, models.Picture.objects.count())
        print(old_title_count, models.Picture.objects.count())

    def test_picture_create(self):
        url = reverse('pictures_create', kwargs={'pk': self.picture.pk})
        old_title_count = models.Picture.objects.count()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertGreater(models.Picture.objects.count(), old_title_count)
