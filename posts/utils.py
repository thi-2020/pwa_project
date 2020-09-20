from posts.models import *






def is_post_liked(user,post_obj,post_type):
    
    if post_type=="Feed":

        res = Like.objects.filter(user=user,feed_post=post_obj).exists()
        
        if res is True:
            return True
        else:
            return False

    if post_type=='Group':
        res = Like.objects.filter(user=user,group_post=post_obj).exists()
        
        if res is True:
            return True
        else:
            return False








def create_activity_and_notification_object(user,post_obj,post_type,activity_type):
    
    if post_type == "Feed":
        like_type = 'feed_post'
        feed_post = post_obj
        group_post = None
       

    if post_type == "Group":
        like_type = 'group_post'
        group_post = post_obj
        feed_post = None


    activity_obj = Activity.objects.create(user=user,activity_type='like_post',
                    post_type=post_type,feed_post=feed_post,group_post=group_post )

    return feed_post,group_post,activity_obj


def remove_activity_and_notification_object(post_obj,post_type,activity_type):

    if post_type == "Feed":
        like_type = 'feed_post'
        feed_post = post_obj
        group_post = None
        is_liked = is_feed_post_liked(user,post_obj)

    if post_type == "Group":
        like_type = 'group_post'
        group_post = post_obj
        feed_post = None


    activity_obj = Activity.objects.create(user=user,post_id=post_obj.id,activity_type='like_post',
                    post_type=post_type,like =like_obj )

    return feed_post,group_post
