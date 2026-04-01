import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import os
from typing import Optional
import logging

from core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class S3Service:
    """Сервис для работы с MinIO (S3-совместимое хранилище)"""

    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ROOT_USER,
            aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
            config=Config(signature_version='s3v4'),
            region_name='us-east-1'
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Создает bucket, если он не существует"""
        try:
            self.client.head_bucket(Bucket=self.bucket)
            logger.info(f"Bucket '{self.bucket}' already exists")
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket)
            logger.info(f"Bucket '{self.bucket}' created")

    async def upload_file(self, file_data: bytes, key: str, content_type: str) -> str:
        """
        Загружает файл в MinIO

        Args:
            file_data: содержимое файла
            key: путь/имя файла в хранилище
            content_type: MIME тип файла

        Returns:
            s3_key: ключ файла в хранилище
        """
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=file_data,
                ContentType=content_type
            )
            logger.info(f"File uploaded: {key}")
            return key
        except ClientError as e:
            logger.error(f"Failed to upload file: {e}")
            raise

    def get_download_url(self, key: str, expires_in: int = 3600) -> str:
        """
        Генерирует подписанную ссылку для скачивания

        Args:
            key: ключ файла в хранилище
            expires_in: время жизни ссылки в секундах (по умолчанию 1 час)

        Returns:
            временная ссылка на файл
        """
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate download URL: {e}")
            raise

    def delete_file(self, key: str) -> bool:
        """
        Удаляет файл из MinIO

        Args:
            key: ключ файла в хранилище

        Returns:
            True если успешно, иначе False
        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            logger.info(f"File deleted: {key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file: {e}")
            return False

    def get_file_info(self, key: str) -> Optional[dict]:
        """
        Получает информацию о файле

        Returns:
            словарь с метаданными или None
        """
        try:
            response = self.client.head_object(Bucket=self.bucket, Key=key)
            return {
                'size': response['ContentLength'],
                'content_type': response['ContentType'],
                'last_modified': response['LastModified']
            }
        except ClientError:
            return None