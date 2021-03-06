from django.contrib import admin
from .models import *
# Register your models here.


class FeedPostAdmin(admin.ModelAdmin):
    list_display = ['id','user','content',"created_at",'modified_at']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','user','feed_post',"group_post"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','user','feed_post',"group_post",'content','is_edited']



admin.site.register(FeedPost,FeedPostAdmin)
admin.site.register(Activity)
admin.site.register(Like,LikeAdmin)
admin.site.register(Comment,CommentAdmin)





