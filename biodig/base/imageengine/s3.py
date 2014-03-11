from biodig.base.imageengine.engine import ImageEngine
from django.conf import settings

import boto
from boto.s3.key import Key

class S3ImageEngine(ImageEngine):
    AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
    AWS_SECRET_KEY = settings.AWS_SECRET_KEY
    
    THUMBNAIL_BUCKET = settings.THUMBNAIL_BUCKET_NAME if hasattr(settings, 'THUMBNAIL_BUCKET_NAME') else 'thumbnail'
    IMAGE_BUCKET = settings.IMAGE_BUCKET_NAME if hasattr(settings, 'IMAGE_BUCKET_NAME') else 'images'

    def save(self, image, bucketname):
        conn = boto.connect_s3(S3ImageEngine.AWS_ACCESS_KEY, S3ImageEngine.AWS_SECRET_KEY)

        bucket = conn.create_bucket(bucketname, location=boto.s3.connection.Location.DEFAULT)

        k = Key(bucket)
        k.key = os.path.basename(image)
        k.set_contents_from_filename(image)

        url = k.generate_url(expires=None, query_auth=False)

        conn.close()

        return url

    def delete(self, image, bucketname):
        conn = boto.connect_s3(S3ImageEngine.AWS_ACCESS_KEY, S3ImageEngine.AWS_SECRET_KEY)

        bucket = conn.create_bucket(bucketname, location=boto.s3.connection.Location.DEFAULT)

        k = Key(bucket)
        k.key = os.path.basename(image)

        b.delete_key(k)

        conn.close()

    
    def save_image(self, image):
        return self.save(image, S3ImageEngine.IMAGE_BUCKET)

    def save_thumbnail(self, thumbnail):
        return self.save(thumbnail, S3ImageEngine.THUMBNAIL_BUCKET)

    def delete_image(self, image):
        self.delete(image, S3ImageEngine.IMAGE_BUCKET)

    def delete_thumbnail(self, thumbnail):
        self.delete(thumbnail, S3ImageEngine.THUMBNAIL_BUCKET)

