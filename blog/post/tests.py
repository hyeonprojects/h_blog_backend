from django.test import TestCase
from .models import Post

class PostTest(TestCase):
    def setUp(self):
        Post.objects.create(
            title='안녕하세요',
            body='안녕하세요. 희선이입니다.',
            tags='희선희선',
        )
        Post.objects.create(
            title='블로그접습니다.',
            body='블로그접습니다.',
            tags='블로그접음',
        )

    def test_post(self):
        post_1 = Post.objects.get(title='안녕하세요')
        post_2 = Post.objects.get(title='블로그접습니다.')
        self.assertIn(post_1.get_body(), '희선이입니다.')
        self.assertIn(post_2.get_body(), '블로그')

    def writePost(self):
        pass

    def getPost(self):
        pass

    def getPostList(self):
        pass

    def editPost(self):
        pass

    def removePost(self):
        pass

    def login(self):
        pass

    def checklogin(self):
        pass

    def logout(self):
        pass