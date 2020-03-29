from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from info_channel.models import Post, PostBodyParagraph


class PostTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('adam', 'adam@example.com', 'adampassword')

    def test_create_sample_post(self):
        sample_post = Post.objects.create(
            title='test title',
            slug='test-title',
            author=self.user,
        )
        self.assertTrue(isinstance(sample_post, Post))
        self.assertEqual('test title', sample_post.title, 'The titles are not the same')
        self.assertEqual('test-title', sample_post.slug)
        self.assertEqual('adam', sample_post.author.username, 'The author names are not the same')
        self.assertTrue(isinstance(sample_post.author, User))
        self.assertEqual('inner_information', sample_post.category, 'The default post category is incorrect')
        self.assertEqual('draft', sample_post.status, 'The default post status is incorrect')

    def test_post_body_paragraph(self):
        sample_post = Post.objects.create(
            title='test title',
            slug='test-title',
            author=self.user,
        )

        related_body_paragraph = PostBodyParagraph.objects.create(
            post=Post.objects.get(id=sample_post.id),
            body='Sample body lorem ipsum...',
            img_address='www.example.com',
            img_link='www.example2.com',
            img_alt='some alt text'
        )

        self.assertTrue(isinstance(related_body_paragraph, PostBodyParagraph))
        self.assertTrue(isinstance(related_body_paragraph.post, Post))
        self.assertEqual('Sample body lorem ipsum...', related_body_paragraph.body)
        self.assertEqual('www.example.com', related_body_paragraph.img_address)
        self.assertEqual('www.example2.com', related_body_paragraph.img_link)
        self.assertEqual('some alt text', related_body_paragraph.img_alt)
        self.assertEqual('center', related_body_paragraph.img_position)