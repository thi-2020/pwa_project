from django.db import models
from django.conf import settings
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BasePost(BaseModel):    
    
    content = models.TextField(null=True,blank=True)
    image = models.FileField(null=True,blank=True)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)
    is_edited = models.BooleanField(default=False)
    is_comment_disabled = models.BooleanField(default=False)

    class Meta:
        abstract = True



class FeedPost(BasePost):
    privacy_types = [
    ('connections','connections'),
    ('everyone','everyone'),   
    ('connection_and_followers','connection_and_followers')        
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='normal_posts')
    visibilty_status = models.CharField(
        max_length=50,choices = privacy_types,null=True,blank=True)

class GroupPost(BasePost):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='group_posts')
  


class Like(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='likes')
    normal_post = models.ForeignKey(FeedPost,on_delete=models.CASCADE,related_name='likes')
    group_post = models.ForeignKey(GroupPost,on_delete=models.CASCADE,related_name='likes')


class Comment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    normal_post = models.ForeignKey(FeedPost,on_delete=models.CASCADE,related_name='comments',
        null=True,blank=True)
    group_post = models.ForeignKey(GroupPost,on_delete=models.CASCADE,related_name='comments'
        ,null=True,blank=True)
    content = models.TextField()
    is_edited = models.BooleanField(default=False)



class Activity(BaseModel):
    types = [
    ('like','like'),
    ('comment','comment'),   
    ('create_post','create_post'),   
    ('share_post','share_post'),   
            
    ]
        
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='activities')
    activity_type = models.CharField(max_length=50,choices = types,null=True,blank=True)
    like = models.ForeignKey(Like,on_delete=models.CASCADE,null=True,blank=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)
    create_post = models.ForeignKey(FeedPost,on_delete=models.CASCADE,
            related_name = 'create_post_activity',null=True,blank=True)
    share_post = models.ForeignKey(FeedPost,on_delete=models.CASCADE,
            related_name = 'share_post_activity',null=True,blank=True)




class Notification(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    like = models.ForeignKey(Like,on_delete=models.CASCADE,null=True,blank=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)   
    