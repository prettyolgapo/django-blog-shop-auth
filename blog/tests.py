from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Post
from shop.forms import CartForm
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class PostTests(TestCase):
    def setUp(self):
        # run before each test
        user1 = User.objects.create_user('test1', 'test1@testmail.com', 'test1password')
        user2 = User.objects.create_user('test2', 'test2@testmail.com', 'test2password')
        Post.objects.create(author=user1,
                            title='Article',
                            text='lorem ipsum shmipsum',
                            created_date=timezone.now() - datetime.timedelta(days=13, weeks=2),
                            published_date=timezone.now() - datetime.timedelta(days=13, weeks=2))
        Post.objects.create(author=user2,
                            title='Postik',
                            text='lorem ipsum shmipsum pup pum',
                            created_date=timezone.now() - datetime.timedelta(days=10, weeks=2),
                            published_date=timezone.now() - datetime.timedelta(days=1, weeks=2))
        Post.objects.create(author=user1,
                            title='A',
                            text='lorem ipsum shmipsum',
                            created_date=timezone.now() - datetime.timedelta(days=6, weeks=7),
                            published_date=timezone.now() - datetime.timedelta(days=7, weeks=5))
        Post.objects.create(author=user2,
                            title='P',
                            text='lorem ipsum shmipsum pup pum',
                            created_date=timezone.now() - datetime.timedelta(days=2, weeks=4),
                            published_date=timezone.now() - datetime.timedelta(days=9))

    def test_blog_list(self):
        """
            Shows post list
        """
        response = self.client.get(reverse('blog:post_list'))
        self.assertQuerysetEqual(list(response.context['posts']), ['<Post: A>',
                                                                   '<Post: Article>',
                                                                   '<Post: Postik>',
                                                                   '<Post: P>'])

    def test_post_detail(self):
        """
             Displayed post detail by id
        """
        article = Post.objects.get(title="Article")
        response = self.client.get(reverse('blog:post_detail', args=(article.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], article)

    def test_search(self):
        """
           Displayed search results from response
        """
        response = self.client.get(reverse('blog:search_results'), {'q': 'A'})
        self.assertQuerysetEqual(list(response.context['object_list']), ['<Post: Article>', '<Post: A>'])


