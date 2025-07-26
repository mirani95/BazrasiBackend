from botocore.exceptions import NoCredentialsError
import boto3
import logging
from PIL import Image
import io
import base64

LIARA_ENDPOINT = 'https://storage.c2.liara.space'
LIARA_BUCKET_NAME = 'ticket-rasadyar'
LIARA_ACCESS_KEY = "gvqohestrakmqi6n"
LIARA_SECRET_KEY = '7240fdd8-59bc-4f02-b5e6-4a124e37fa0e'


def upload_to_liara(file_obj, file_name):
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=LIARA_ENDPOINT,
            aws_access_key_id=LIARA_ACCESS_KEY,
            aws_secret_access_key=LIARA_SECRET_KEY
        )

        s3.upload_fileobj(
            file_obj,
            LIARA_BUCKET_NAME,
            file_name,
            ExtraArgs={'ACL': 'public-read'}  # دسترسی عمومی
        )

        return f"{LIARA_ENDPOINT}/{LIARA_BUCKET_NAME}/{file_name}"

    except NoCredentialsError:
        raise Exception("اعتبارنامه‌های AWS معتبر نیستند")
    except Exception as e:
        raise Exception(f"خطا در آپلود فایل: {e}")


def connect():
    logging.basicConfig(level=logging.INFO)

    try:
        s3 = boto3.client(
            's3',
            endpoint_url=LIARA_ENDPOINT,
            aws_access_key_id=LIARA_ACCESS_KEY,
            aws_secret_access_key=LIARA_SECRET_KEY
        )
    except Exception as exc:
        logging.info(exc)
    return s3


def upload_object_resize_to_liara(image_data, object_name):
    try:
        imgdata = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(imgdata))

        img.thumbnail((500, 500))

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        s3_resource = boto3.resource(
            's3',
            endpoint_url=LIARA_ENDPOINT,
            aws_access_key_id=LIARA_ACCESS_KEY,
            aws_secret_access_key=LIARA_SECRET_KEY
        )

        bucket = s3_resource.Bucket(LIARA_BUCKET_NAME)
        bucket.put_object(
            ACL='public-read',
            Body=buffer,
            Key=object_name,
            ContentType='image/png'
        )

        return f"{LIARA_ENDPOINT}/{LIARA_BUCKET_NAME}/{object_name}"

    except Exception as e:
        raise Exception(f"خطا در آپلود فایل: {e}")


def delete_file_from_liara(file_name):
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=LIARA_ENDPOINT,
            aws_access_key_id=LIARA_ACCESS_KEY,
            aws_secret_access_key=LIARA_SECRET_KEY
        )

        s3.delete_object(Bucket=LIARA_BUCKET_NAME, Key=file_name)

    except NoCredentialsError:
        raise Exception("اعتبارنامه‌های AWS معتبر نیستند")
    except Exception as e:
        raise Exception(f"خطا در آپلود فایل: {e}")
