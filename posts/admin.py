from django.contrib import admin
from .models import *
# Register your models here.


class FeedPostAdmin(admin.ModelAdmin):
    list_display = ['id','user','content',"created_at",'modified_at']



admin.site.register(FeedPost,FeedPostAdmin)
admin.site.register(Activity)





