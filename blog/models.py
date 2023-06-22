from django.db import models


class Users(models.Model):
    DoesNotExist = None
    objects = None
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class BlogPost(models.Model):
    DoesNotExist = None
    objects = None
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.TextField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
