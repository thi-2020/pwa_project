from posts.models import *






def is_feed_post_liked(user,post_id):
    post_obj = FeedPost.objects.get(id = post_id)
    



