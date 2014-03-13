from biodig.base.imageengine.engine import ImageEngine
from django.conf import settings

import boto
from boto.s3.key import Key
import time
import os

class S3ImageEngine(ImageEngine):
    AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
    AWS_SECRET_KEY = settings.AWS_SECRET_KEY
    
    THUMBNAIL_BUCKET = settings.THUMBNAIL_BUCKET_NAME
    IMAGE_BUCKET = settings.IMAGE_BUCKET_NAME

    URL_FORMAT = "https://s3.amazonaws.com/{0}/{1}"

    def save(self, image, bucketname):
        conn = boto.connect_s3(S3ImageEngine.AWS_ACCESS_KEY, S3ImageEngine.AWS_SECRET_KEY)

        bucket = conn.lookup(bucketname)
        if bucket is None:
            bucket = conn.create_bucket(bucketname, location=boto.s3.connection.Location.DEFAULT)

        k = Key(bucket)
        k.key = os.path.basename(image)
        k.set_contents_from_filename(image)
        k.set_acl('public-read')
        k.make_public()
        conn.close()

        return S3ImageEngine.URL_FORMAT.format(bucketname, k.key)

    def delete(self, image, bucketname):
        conn = boto.connect_s3(S3ImageEngine.AWS_ACCESS_KEY, S3ImageEngine.AWS_SECRET_KEY)

        bucket = conn.lookup(bucketname)
        if bucket is None:
            return # no bucket means no delete necessary

        k = Key(bucket)
        k.key = os.path.basename(image)

        bucket.delete_key(k)

        conn.close()

    
    def save_image(self, image):
        return self.save(image, S3ImageEngine.IMAGE_BUCKET)

    def save_thumbnail(self, thumbnail):
        return self.save(thumbnail, S3ImageEngine.THUMBNAIL_BUCKET)

    def delete_image(self, image):
        self.delete(image, S3ImageEngine.IMAGE_BUCKET)

    def delete_thumbnail(self, thumbnail):
        self.delete(thumbnail, S3ImageEngine.THUMBNAIL_BUCKET)

