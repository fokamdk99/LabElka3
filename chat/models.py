from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Conversation(models.Model):
    name = models.CharField(max_length=64)
    related_users = models.ManyToManyField(User, related_name="rozmowcy")
    last_spoken_with = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.name}"

class Message(models.Model):
    author = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)
    belongs_to_conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)

    def __str__(self):
        return f"author: {self.author}, content:{self.content}"
