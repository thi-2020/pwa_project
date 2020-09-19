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
    version = models.IntegerField(default=1)

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

    def __str__(self):
        # return str(self.user) 
        return str(self.user) + " " + "post_id: "+str(self.id)  



class GroupPost(BasePost):    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='group_posts')
  


class Like(BaseModel):
    types = (('feed_post','feed_post'),
            ('group_post','group_post'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='likes')
    feed_post = models.ForeignKey(FeedPost,on_delete=models.CASCADE,related_name='likes',
        null=True,blank=True)
    group_post = models.ForeignKey(GroupPost,on_delete=models.CASCADE,related_name='likes',
        null=True,blank=True)

    like_type = models.CharField(max_length=50,null=True,blank=True,choices=types)


    class Meta:
        unique_together = (('user', 'feed_post'),
                           ('user', 'feed_post'))

    def __str__(self):
        return str(self.user)


class Comment(BaseModel):
    types = (('feed_post','feed_post'),
            ('group_post','group_post'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    feed_post = models.ForeignKey(FeedPost,on_delete=models.CASCADE,related_name='comments',
        null=True,blank=True)
    group_post = models.ForeignKey(GroupPost,on_delete=models.CASCADE,related_name='comments'
        ,null=True,blank=True)
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    version = models.IntegerField(default=1)
    comment_type = models.CharField(max_length=50,null=True,blank=True,choices=types)


    class Meta:
        unique_together = (('user', 'feed_post'),
                           ('user', 'feed_post'))

    def __str__(self):
        return self.user



class Activity(BaseModel):
    types = [
    ('like_feed_post','like_feed_post'),
    ('comment_feed_post','comment_feed_post'),   
    ('create_feed_post','create_feed_post'),   
    ('share_feed_post','share_feed_post'),   
            
    ]
        
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='activities')
    activity_type = models.CharField(max_length=50,choices = types,null=True,blank=True)
    like = models.ForeignKey(Like,on_delete=models.CASCADE,null=True,blank=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)
    post_id = models.IntegerField(null=True,blank=True)




class Notification(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications')
    like = models.ForeignKey(Like,on_delete=models.CASCADE,null=True,blank=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True,blank=True)   
    