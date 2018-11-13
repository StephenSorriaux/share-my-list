from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import List

CREDENTIALS = {
            'username': 'testuser',
            'password': 'secret',
            'email': 'test@whatever.com'}

class TestCaseWithLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(**CREDENTIALS)
        login = self.client.login(**CREDENTIALS)
        self.assertTrue(login, True)

    def tearDown(self):
        self.user.delete()

class TestCaseWithList(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(**CREDENTIALS)
        login = self.client.login(**CREDENTIALS)
        self.assertTrue(login, True)
        self.list = List.objects.create(owner=self.user)

    def tearDown(self):
        self.user.delete()

class LogInTest(TestCase):

    def test_no_login(self):
        response = self.client.get(reverse('lists:index'), follow=True)
        self.assertRedirects(response, '{}?next={}'.format(reverse('login'),reverse('lists:index')))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login(self):
        self.user = User.objects.create_user(**CREDENTIALS)
        login = self.client.login(**CREDENTIALS)
        self.assertTrue(login, True)
        self.user.delete()

class LogOutTest(TestCaseWithLogin):

    def test_logout(self):
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, '{}?next={}'.format(reverse('login'),reverse('lists:index')))
        self.assertNotIn('_auth_user_id', self.client.session)


class ListsIndexViewTests(TestCaseWithLogin):

    def test_no_lists(self):
        """
        If no lists exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('lists:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucune liste pour le moment")
        self.assertQuerysetEqual(response.context['all_lists'], [])

    def test_create_list(self):
        """
        Can create one list.
        """
        response = self.client.get(reverse('lists:create'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ma liste")


    def test_create_only_one_list(self):
        """
        If trying to create more than one list, an appropriate message is displayed.
        """
        list = List.objects.create(owner=self.user)
        response = self.client.get(reverse('lists:create'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vous avez déjà une liste")
        self.assertQuerysetEqual(response.context['all_lists'], [repr(list)])

class ListDetailViewTests(TestCaseWithList):

    def test_can_access_list(self):
        response = self.client.get(reverse('lists:detail',kwargs={'pk': self.list.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_list_no_choices(self):
        response = self.client.get(reverse('lists:detail', kwargs={'pk': self.list.id}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucun cadeau dans cette liste")

    def test_add_choice_to_list(self):
        data = {
            'name': 'test',
            'link': 'http://www.test.fr/',
            'price': 1337.69
        }
        response = self.client.post(reverse('lists:add', kwargs={'list_id': self.list.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['name'])
        self.assertContains(response, data['price'])
        self.assertEqual(len(self.list.choice_set.all()), 1)

    def test_add_choice_to_list(self):
        data = {
            'name': 'test',
            'link': 'http://www.test.fr/',
            'price': 1337.69
        }
        response = self.client.post(reverse('lists:add', kwargs={'list_id': self.list.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['name'])
        self.assertContains(response, data['price'])
        self.assertEqual(len(self.list.choice_set.all()), 1)

    def test_ensure_current_owner_cant_mark_choice_as_bought(self):
        data = {
            'name': 'test',
            'link': 'http://www.test.fr/',
            'price': 1337.69
        }
        response = self.client.post(reverse('lists:add', kwargs={'list_id': self.list.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data['name'])
        self.assertContains(response, data['price'])
        self.assertEqual(len(self.list.choice_set.all()), 1)

        choice = self.list.choice_set.all()[0]
        self.assertFalse(choice.is_bought)
        data = {
            'choice': choice.id
        }
        response = self.client.post(reverse('lists:update', kwargs={'list_id': self.list.id}), data, follow=True)

        self.assertEqual(len(self.list.choice_set.all()), 1)
        choice = self.list.choice_set.all()[0]
        self.assertFalse(choice.is_bought)


    def test_add_bad_choice_to_list(self):
        data = {
            'name': 'test',
            'link': 'http://www.test.fr/',
            'price': 'abc'
        }
        response = self.client.post(reverse('lists:add', kwargs={'list_id': self.list.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aucun cadeau dans cette liste")
        self.assertEqual(len(self.list.choice_set.all()), 0)

    def test_mark_choice_as_bought(self):
        data = {
            'name': 'test',
            'link': 'http://www.test.fr/',
            'price': 1337.69
        }
        response = self.client.post(reverse('lists:add', kwargs={'list_id': self.list.id}), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.list.choice_set.all()), 1)
        
        choice = self.list.choice_set.all()[0]
        self.assertFalse(choice.is_bought)

        new_credentials = CREDENTIALS
        new_credentials["username"] = 'test2'
        new_user = User.objects.create_user(**new_credentials)
        login = self.client.login(**new_credentials)
        self.assertTrue(login, True)

        data = {
            'choice': choice.id
        }
        response = self.client.post(reverse('lists:update', kwargs={'list_id': self.list.id}), data, follow=True)
        self.assertContains(response, "Oui, par {}".format(new_credentials['username']))
        self.assertEqual(len(self.list.choice_set.all()), 1)
        choice = self.list.choice_set.all()[0]
        self.assertTrue(choice.is_bought)

        new_user.delete()