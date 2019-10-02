from django.db import models
from home.models import Post
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Komentarz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, related_name='komentarze')

    def __str__(self):
        return f"komentarz: {self.content}"