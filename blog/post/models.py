from djongo import models

class Post(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    tags = models.JSONField(null=True)
    published_date = models.DateTimeField(auto_now_add=True) #알아서 날짜랑 시간 적어줌
    objects = models.DjongoManager()

    def __str__(self):
        return "{} / {}".format(self.title, self.id)