from django.core.exceptions import ValidationError
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.models import Item, List
from lists.views import home_page

# Create your tests here.
class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_item(self):
        email = "test@test.com"
        list_ = List.objects.create(email=email)
        list_.save()

        first_item = Item()
        first_item.text = 'First Item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Second Item'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'First Item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Second Item')
        self.assertEqual(second_saved_item.list, list_)
    
    def test_cannot_save_empty_list_item(self):
        email = "test@test.com"
        list_ = List.objects.create(email=email)
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
    def test_get_absolute_url(self):
        email = "test@test.com"
        list_ = List.objects.create(email=email)
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.email}/')