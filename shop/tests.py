from decimal import Decimal

from unicodedata import decimal

from shop import factories, models
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone


class ShopTest(TestCase):
    def setUp(self):
        self.picture = factories.PictureFactory()
        self.painter = factories.PainterFactory()
        self.style = factories.StyleFactory()
        self.category = factories.CategoryFactory()



    def test_picture_list(self):
        url = reverse('pictures_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pictures'].count(), models.Picture.objects.count())

    def test_picture_detail(self):
        url = reverse('pictures_detail', kwargs={'pk': self.picture.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_picture_update(self):
        url = reverse('pictures_update', kwargs={'pk': self.picture.pk})
        old_title = self.picture.title
        old_public_date = self.picture.public_date
        old_availability = self.picture.availability
        old_is_original = self.picture.is_original
        old_history = self.picture.history
        old_price = self.picture.price
        old_cover_picture = self.picture.cover_picture
        old_category = self.picture.category
        old_style = self.picture.style.all()
        old_author = self.picture.author

        new_title = 'New Title'
        new_public_date = timezone.now().date()
        new_availability = not old_availability
        new_is_original = not old_is_original
        new_history = 'New history'
        new_price = Decimal('123.45')
        new_cover_picture = 'C:/Users/ghost/PycharmProjects/ItCode-HomeWork3/templates/static/55259a660d54af15267578aeaa25db4c.jpg'
        new_category = self.category
        new_author = self.painter
        new_style = [self.style]

        response = self.client.post(url, {
            'title': new_title,
            'public_date': new_public_date.strftime('%Y-%m-%d'),
            'availability': new_availability,
            'is_original': new_is_original,
            'history': new_history,
            'price': new_price,
            'cover_picture': open(new_cover_picture, 'rb'),
            'category': new_category.pk,
            'author': new_author.pk,
            'style': [style.pk for style in new_style],
        })
        self.assertEqual(response.status_code, 302)
        self.picture.refresh_from_db()
        self.assertNotEqual(self.picture.title, old_title)
        self.assertNotEqual(self.picture.public_date, old_public_date)
        self.assertNotEqual(self.picture.availability, old_availability)
        self.assertNotEqual(self.picture.is_original, old_is_original)
        self.assertNotEqual(self.picture.history, old_history)
        self.assertNotEqual(self.picture.price, old_price)
        self.assertNotEqual(self.picture.cover_picture.name, old_cover_picture.name)
        self.assertNotEqual(self.picture.category, old_category)
        self.assertNotEqual(self.picture.author, old_author)
        self.assertNotEqual((self.picture.style.all()),old_style)


    def test_picture_delete(self):
        url = reverse('pictures_delete', kwargs={'pk': self.picture.pk})
        old_title_count = models.Picture.objects.count()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertGreater(old_title_count, models.Picture.objects.count())

    def test_picture_create(self):
        url = reverse('pictures_create')
        old_picture_count = models.Picture.objects.count()

        new_title = 'New Title'
        new_public_date = timezone.now().date()
        new_availability = True
        new_is_original = True
        new_history = 'New history'
        new_price = Decimal('123.45')
        new_cover_picture = 'C:/Users/ghost/PycharmProjects/ItCode-HomeWork3/templates/static/55259a660d54af15267578aeaa25db4c.jpg'
        new_category = self.category
        new_author = self.painter
        new_style = [self.style]

        response = {
            'title': new_title,
            'public_date': new_public_date.strftime('%Y-%m-%d'),
            'availability': new_availability,
            'is_original': new_is_original,
            'history': new_history,
            'price': new_price,
            'cover_picture': open(new_cover_picture, 'rb'),
            'category': new_category.pk,
            'author': new_author.pk,
            'style': [style.pk for style in new_style],
        }

        response = self.client.post(url, response)
        self.assertEqual(response.status_code, 302)

        self.assertGreater(models.Picture.objects.count(), old_picture_count)
        created_picture = models.Picture.objects.latest('created_at')

        self.assertEqual(created_picture.title, new_title)
        self.assertEqual(created_picture.public_date, new_public_date)
        self.assertEqual(created_picture.availability, new_availability)
        self.assertEqual(created_picture.is_original, new_is_original)
        self.assertEqual(created_picture.history, new_history)
        self.assertEqual(created_picture.price, new_price)
        self.assertEqual(created_picture.cover_picture.size, 41020)
        self.assertEqual(created_picture.category, new_category)
        self.assertEqual(created_picture.author, new_author)
        self.assertEqual(list(created_picture.style.all()), list(new_style))
