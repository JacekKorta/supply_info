from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from info_channel.models import Post, PostBodyParagraph


class PostsSetUp(TestCase):
    def setUp(self):
        now = datetime.now()
        self.day = now.day
        self.month = now.month
        self.year = now.year
        self.user = User.objects.create_superuser('Artur_admin', 'artur_the_admin@example.com', 'arturadminpassword')

        sample_post1 = Post.objects.create(
            title='Draft_title',
            slug='draft-title',
            author=self.user,
            status='draft',
        )

        PostBodyParagraph.objects.create(
            post=Post.objects.get(id=sample_post1.id),
            body='unpublished body lorem ipsum...',
        )

        sample_post2 = Post.objects.create(
            title='test title 2',
            slug='test-title-2',
            author=self.user,
            category='inner_information',
            status='published',
        )

        PostBodyParagraph.objects.create(
            post=Post.objects.get(id=sample_post2.id),
            body='inner body lorem ipsum...',
        )

        sample_post3 = Post.objects.create(
            title='test title 3',
            slug='test-title-3',
            author=self.user,
            category='news',
            status='published',
        )

        PostBodyParagraph.objects.create(
            post=Post.objects.get(id=sample_post3.id),
            body='News body lorem ipsum...',
        )


class StaffUserLoggedIn(PostsSetUp):
    def setUp(self):
        super(StaffUserLoggedIn, self).setUp()
        self.user = User.objects.create_user('terry', 'terry@example.com', 'terrypassword', is_staff=True)
        self.client.login(username='terry', password='terrypassword')


class UserLoggedIn(PostsSetUp):
    def setUp(self):
        super(UserLoggedIn, self).setUp()
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')
        self.client.login(username='adam', password='adampassword')


class TestPostsListStaffLogged(StaffUserLoggedIn):
    def test_inner_posts_lists_site_staff_user_logged(self):
        response = self.client.get(reverse('info_channel:post_list', kwargs={'category':'inner_information'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_channel/post/list.html')
        self.assertContains(response, 'informacje')
        self.assertContains(response, 'test title 2')
        self.assertContains(response, 'inner body lorem ipsum...')
        # 'The post is unpublished, should be not visible'
        self.assertNotContains(response, 'Draft_title')
        self.assertNotContains(response, "unpublished body lorem ipsum...")
        # The post have different category, shouldn't be visible
        self.assertNotContains(response, 'test title 3',)
        self.assertNotContains(response, 'News body lorem ipsum...')

    def test_news_posts_list_site_staff_user_logged(self):
        response = self.client.get(reverse('info_channel:post_list', kwargs={'category': 'news'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_channel/post/list.html')
        self.assertContains(response, 'informacje')
        self.assertContains(response, 'test title 3')
        self.assertContains(response, 'News body lorem ipsum...')

    def test_news_post_detail_staff_user_logged(self):
        response = self.client.get(reverse('info_channel:post_detail',
                                           kwargs={
                                               'year': self.year,
                                               'month': self.month,
                                               'day': self.day,
                                               'slug': 'test-title-3'
                                           }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_channel/post/detail.html')
        self.assertContains(response, 'test title 3')
        self.assertContains(response, 'News body lorem ipsum...')
        self.assertContains(response, f"Opublikowano: {self.day}")
        self.assertContains(response, f"{self.year}")

    def test_inner_post_detail_staff_user_logged(self):
        response = self.client.get(reverse('info_channel:post_detail',
                                           kwargs={
                                               'year': self.year,
                                               'month': self.month,
                                               'day': self.day,
                                               'slug': 'test-title-2'
                                           }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_channel/post/detail.html')
        self.assertContains(response, 'test title 2')
        self.assertContains(response, 'inner body lorem ipsum...')
        self.assertContains(response, f"Opublikowano: {self.day}")
        self.assertContains(response, f"{self.year}")



class TestPostsListUserLogged(UserLoggedIn):
    def test_inner_posts_lists_site_standard_user_logged(self):
        response = self.client.get(reverse('info_channel:post_list', kwargs={'category': 'inner_information'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_channel/post/list.html')
        self.assertContains(response, 'informacje')
        # the inner_information shouldn't be visible for standard user
        self.assertNotContains(response, 'test title 2')
        self.assertNotContains(response, 'inner body lorem ipsum...')
        # 'The post is unpublished, should be not visible'
        self.assertNotContains(response, 'Draft_title')
        self.assertNotContains(response, "unpublished body lorem ipsum...")
        # The post have different category, shouldn't be visible
        self.assertNotContains(response, 'test title 3',)
        self.assertNotContains(response, 'News body lorem ipsum...')

    def test_news_posts_list_site_standard_user_logged(self):
        response = self.client.get(reverse('info_channel:post_list', kwargs={'category': 'news'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_channel/post/list.html')
        self.assertContains(response, 'informacje')
        self.assertContains(response, 'test title 3')
        self.assertContains(response, 'News body lorem ipsum...')

    def test_news_post_detail_user_logged(self):
        response = self.client.get(reverse('info_channel:post_detail',
                                           kwargs={
                                               'year': self.year,
                                               'month': self.month,
                                               'day': self.day,
                                               'slug': 'test-title-3'
                                           }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_channel/post/detail.html')
        self.assertContains(response, 'test title 3')
        self.assertContains(response, 'News body lorem ipsum...')
        self.assertContains(response, f"Opublikowano: {self.day}")
        self.assertContains(response, f"{self.year}")

    def test_inner_post_detail_user_logged(self):
        response = self.client.get(reverse('info_channel:post_detail',
                                           kwargs={
                                               'year': self.year,
                                               'month': self.month,
                                               'day': self.day,
                                               'slug': 'test-title-2'
                                           }))
        self.assertEqual(response.status_code, 404)

