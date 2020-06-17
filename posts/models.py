from django.db import models
from django.utils import timezone
# Create your models here.
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel



class PostCategory(DjangoCassandraModel):
    category_id = columns.Integer(partition_key=True)
    name = columns.Text()

    def save(self, *args, **kwargs):
        print("@15")
        if PostCategory.objects.filter(category_id = self.category_id).exists():
            raise ValueError("Alreday have a category with id: {}".format(self.category_id))

        if PostCategory.objects.filter(name = self.name).exists():
            raise ValueError("Alreday have a category with name: {}".format(self.name))
        super().save(*args, **kwargs)

class Post(DjangoCassandraModel):        
    category_id = columns.Integer(partition_key=True)
    post_id = columns.UUID(primary_key=True,default=uuid.uuid4)
    user_id = columns.UUID()
    created_at = columns.DateTime(default=timezone.now)
    group_id = columns.UUID()
    event_id = columns.UUID()    
    content = columns.Text()
    created_date = columns.Text()
    no_of_likes = columns.Integer()
    no_of_comments = columns.Integer()
    first_name = columns.Text()
    last_name = columns.Text()

    
    class Meta:
        get_pk_field='post_id'


class PostByUser(DjangoCassandraModel):
    user_id = columns.UUID(partition_key = True)
    category_id = columns.Integer(primary_key=True)
    first_name = columns.Text()
    last_name = columns.Text()
    created_at = columns.DateTime(default=timezone.now,primary_key=True,clustering_order="DESC")
    post_id = columns.UUID(primary_key=True,clustering_order="ASC")
    content = columns.Text()
    no_of_likes = columns.Integer()
    no_of_comments = columns.Integer()
    class Meta:
        get_pk_field='post_id'


class LatestPost(DjangoCassandraModel):
    created_date = columns.Text(partition_key = True)
    category_id = columns.Integer(primary_key=True)
    created_datetime = columns.DateTime(default=timezone.now,primary_key=True,clustering_order="DESC")
    post_id = columns.UUID(primary_key=True,clustering_order="ASC")
    user_id = columns.UUID()
    content = columns.Text()
    first_name = columns.Text()
    last_name = columns.Text()
    no_of_likes = columns.Integer()
    no_of_comments = columns.Integer()

    class Meta:
        get_pk_field='post_id'  



# class LikeByPost(DjangoCassandraModel):
