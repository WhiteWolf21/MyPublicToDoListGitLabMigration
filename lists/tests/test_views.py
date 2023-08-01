from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from lists.models import Item, List
from lists.views import home_page
from django.contrib.auth import get_user_model
from django.test import Client

# Create your tests here.
class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'index.html')

class NewListTest(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(email='temporary@gmail.com')

        self.user = User.objects.get(email='temporary@gmail.com')
        self.client.force_login(self.user)

    def tearDown(self):
        self.user.delete()

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'todo-item': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'todo-item': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.email}/')
    
    def test_validation_errors_are_sent_back_to_homepage_template(self):
        response = self.client.post('/lists/new', data={'todo-item': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    
    def test_invalid_items_arent_saved(self):
        self.client.post('/lists/new', data={'todo-item':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
    
    def test_redirect_to_home_when_not_auth(self):
        self.client.logout()
        response = self.client.post('/lists/new', data={'todo-item':''})
        self.assertRedirects(response, '/')

class ListViewTest(TestCase):

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(email='temporary@gmail.com')

        self.user = User.objects.get(email='temporary@gmail.com')
        self.client.force_login(self.user)
    
    def tearDown(self):
        self.user.delete()
    
    def test_uses_list_template(self):
        list_ = List.objects.create(email=self.user.email)
        response = self.client.get(f'/lists/{list_.email}/')
        self.assertTemplateUsed(response, 'lists.html')
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create(email=self.user.email)
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)

        other_list = List.objects.create(email="random@r.com")
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.email}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create(email="random@r.com")
        correct_list = List.objects.create(email=self.user.email)
        response = self.client.get(f'/lists/{correct_list.email}/')
        self.assertEqual(response.context['list'], correct_list) 

    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create(email=self.user.email)

        self.client.post(
            f'/lists/{correct_list.email}/',
            data={'todo-item': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create(email=self.user.email)

        response = self.client.post(
            f'/lists/{correct_list.email}/',
            data={'todo-item': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.email}/')
    
    def test_validation_errors_end_up_on_list_page(self):
        list_ = List.objects.create(email=self.user.email)
        response = self.client.post(
            f'/lists/{list_.email}/',
            data={'todo-item': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
    
    def test_redirect_to_his_list_when_access_other_list(self):
        correct_list = List.objects.create(email=self.user.email)
        another_list = List.objects.create(email="dummy@email.com")

        response = self.client.get(f'/lists/{another_list.email}/', follow=True)
        self.assertRedirects(response, f'/lists/{correct_list.email}/')
    
    def test_redirect_to_home_when_access_other_list(self):
        another_list_url = "other@email.com"
        self.client.logout()

        response = self.client.get(f'/lists/{another_list_url}/', follow=True)
        self.assertRedirects(response, "/")