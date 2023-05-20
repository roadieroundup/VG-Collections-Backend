from django.db import models
import uuid
from users.models import Profile
# Create your models here.

class VideogameList(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_sorted = models.BooleanField(default=False)

    #relation
    owner = models.ForeignKey(Profile, related_name='lists', on_delete=models.CASCADE)

    # blog_post = BlogPost.objects.get(id=1)
    # comments = blog_post.comment_set.all()

    def __str__(self):
        return self.title
    



class Videogame(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    #by default blank is false
    review = models.TextField(blank=True)
    image_url = models.URLField()
    
    #relation

    list = models.ForeignKey('VideogameList', related_name='videogames', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

