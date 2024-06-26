from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    def follow(self, user):
        Follow.objects.create(follower=self, following=user)
    
    def is_following(self, user):
        return Follow.objects.filter(follower=self, following=user).exists()

    def unfollow(self, user):
        try:
            Follow.objects.get(follower=self, following=user).delete()
        except Follow.DoesNotExist:
            ...

    def get_followers(self):
        return [follow.follower for follow in self.followers.all()]
    
    def get_followings(self):
        return [follow.following for follow in self.following.all()]
        

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.body[:20]
        
    def like(self, user):
        if self.likes.contains(user):
            self.likes.remove(user)
            return "UNLIKED"
        else:
            self.likes.add(user)
            return "LIKED"

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

