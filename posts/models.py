from django.db import models
from django.utils import timezone
# Create your models here.
import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


class Post(DjangoCassandraModel):
    post_id = columns.UUID(primary_key=True,default=uuid.uuid4)
    user_id = columns.UUID()
    created_at = columns.DateTime(default=timezone.now)    
    content = columns.Text()
    created_date = columns.Text()
    
    class Meta:
        get_pk_field='post_id'


class PostByUser(DjangoCassandraModel):
    user_id = columns.UUID(partition_key = True)
    created_at = columns.DateTime(default=timezone.now,primary_key=True,clustering_order="DESC")
    post_id = columns.UUID(primary_key=True,clustering_order="ASC",default=uuid.uuid4)
    content = columns.Text()
    class Meta:
        get_pk_field='post_id'


class LatestPost(DjangoCassandraModel):
    created_date = columns.Text(partition_key = True)
    created_datetime = columns.DateTime(default=timezone.now,primary_key=True,clustering_order="DESC")
    post_id = columns.UUID(primary_key=True,clustering_order="ASC")
    user_id = columns.UUID()
    content = columns.Text()
    class Meta:
        get_pk_field='post_id'  