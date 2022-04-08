from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Group, Post
from posts.forms import PostForm

User = get_user_model()


class PostFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_auth_client = Client()
        self.authorized_auth_client.force_login(self.post.author)
        self.user_1 = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_1)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'test_text',
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': f'{self.user_1.username}'}
        ))
        self.assertEqual(Post.objects.count(), post_count +1 )
        self.assertTrue(
            Post.objects.filter(
                text='test_text',
            ).exists()
        )

    def test_edit_post(self):
        """Проверка формы редактирования поста"""
        form_data = {
            'text': 'test_text',
            'group': self.group.pk
        }
        response = self.authorized_auth_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.pk}'}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post.pk}'}
            ))
        self.assertTrue(
            Post.objects.filter(
                text='test_text',
            ).exists()
        )
