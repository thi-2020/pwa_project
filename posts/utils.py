from posts.models import *






def is_feed_post_liked(user,post_obj):
    # post_obj = FeedPost.objects.get(id = post_id)

    res = Like.objects.filter(user=user,feed_post=post_obj).exists()
    
    if res is True:
        return True
    else:
        return False

