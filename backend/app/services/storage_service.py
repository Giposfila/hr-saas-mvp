import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import uuid


class StorageService:
    """S3/MinIO storage service"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
    
    async def upload_resume(
        self,
        file_content: bytes,
        file_name: str,
        candidate_id: int,
    ) -> str:
        """Upload resume to S3/MinIO"""
        # Generate unique file path
        file_extension = file_name.split(".")[-1]
        unique_filename = f"resumes/{candidate_id}/{uuid.uuid4()}.{file_extension}"
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=file_content,
            )
            return unique_filename
        except ClientError as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    
    async def download_resume(self, file_path: str) -> bytes:
        """Download resume from S3/MinIO"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_path,
            )
            return response["Body"].read()
        except ClientError as e:
            raise Exception(f"Failed to download file: {str(e)}")
    
    async def delete_resume(self, file_path: str) -> bool:
        """Delete resume from S3/MinIO"""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path,
            )
            return True
        except ClientError as e:
            raise Exception(f"Failed to delete file: {str(e)}")
    
    def get_file_url(self, file_path: str, expires_in: int = 3600) -> str:
        """Generate presigned URL for file access"""
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": file_path},
                ExpiresIn=expires_in,
            )
            return url
        except ClientError as e:
            raise Exception(f"Failed to generate URL: {str(e)}")
