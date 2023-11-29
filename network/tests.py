from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import *
# Create your tests here.


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user("demaxl", "demaxl@example.com", "Characters12345!")
        cls.user2 = User.objects.create_user("ron", "demaxl@example.com", "Characters12345!")
        cls.user3 = User.objects.create_user("david", "demaxl@example.com", "Characters12345!")


    def testFollow(self):
        """Test duplicate follows and same user follow"""
        # Test duplicate follows
        Follow.objects.create(following=self.user1, follower=self.user2)
        with self.assertRaises(ValidationError):
            Follow.objects.create(following=self.user1, follower=self.user2)

        # Test same user follow
        with self.assertRaises(ValidationError):
            Follow.objects.create(following=self.user1, follower=self.user1)

    def testLikes(self):
        post = Post(poster=self.user1, title="A test title", body="a body my bro")
        post.save()

        # Test like
        post.like(self.user2)
        self.assertIn(self.user2, post.likes.all())

        # Test unline
        post.like(self.user2)
        self.assertNotIn(self.user2, post.likes.all())

        


        