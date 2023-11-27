from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    def follow(self, user):
        Follow.objects.create(follower=self, following=user)

    def unfollow(self, user):
        try:
            Follow.objects.get(follower=self, following=user).delete()
        except Follow.DoesNotExist:
            ...

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")

    def __str__(self):
        return self.title

class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = (("following", "follower"),)

    def clean(self) -> None:
        if self.following == self.follower:
            raise ValidationError(f"{self.follower} can not follow themselves")
        
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return f"{self.user}: {self.body[:20]}"

