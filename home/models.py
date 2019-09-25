from django.db import models
from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Semestr(models.Model):
    semester_name = models.CharField(max_length=50)
    number = models.IntegerField(default=-1)

    def __str__(self):
        return f"{self.semester_name}"

class Przedmiot(models.Model):
    subject_name = models.CharField(max_length=50)
    semestr = models.ForeignKey(Semestr, on_delete=models.CASCADE,blank=True, null=True, related_name='przedmioty_z_danego_semestru')

    def __str__(self):
        return f"{self.subject_name}"

class Test(models.Model):
    test_name = models.CharField(max_length=50)
    przedmiot = models.ForeignKey(Przedmiot, on_delete=models.CASCADE,blank=True,null=True, related_name='testy_z_danego_przedmiotu')

    def __str__(self):
        return f"{self.test_name}, {self.przedmiot}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    #attachment = models.FileField(upload_to="posts/attachments/", widget=forms.ClearableFileInput(attrs={'multiple': True}))
    test = models.ForeignKey(Test, on_delete=models.CASCADE,blank=True,null=True, related_name='posty_z_danego_testu')

    def __str__(self):
        return f"{self.title}"

class Attachment(models.Model):
    att = models.FileField(upload_to="posts/multiple_attachments")
    post = models.ForeignKey(Post, related_name="attachments", on_delete=models.CASCADE)
