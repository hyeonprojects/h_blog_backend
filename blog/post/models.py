# from django.db import models
from djongo import models
import uuid

class Comment(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Post(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    tags = models.CharField(max_length=300)
    published_date = models.DateTimeField(auto_now_add=True) #알아서 날짜랑 시간 적어줌
    comment = models.EmbeddedField(
        model_container=Comment,
        null=False
    )
    objects = models.DjongoManager()

    def __str__(self):
        return "{} / {}".format(self.title, self.id)