from django.db import models
from django.conf import settings
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BasePost(BaseModel):        

    content = models.TextField()   
    no_of_likes = models.IntegerField
    no_of_comments = models.IntegerField

    class Meta:
        abstract = True



class NormalPost(BasePost):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='normal_posts')





class Likes(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='likes')
    normal_post = models.ForeignKey(NormalPost,on_delete=models.CASCADE,related_name='likes')
