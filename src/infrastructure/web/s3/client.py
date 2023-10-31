from datetime import datetime

from boto3.session import Session


class S3Client:
    def __init__(
            self, aws_access_key_id: str,
            aws_secret_access_key: str,
            service_name: str,
            bucket: str,
            path: str,
            location: str
    ):
        self._service_name = service_name
        self._key_id = aws_access_key_id
        self._access_key = aws_secret_access_key
        self._bucket = bucket
        self._path = path
        self._location = location
        session = Session(aws_access_key_id=self._key_id,
                          aws_secret_access_key=self._access_key)
        self.presigned = session.client("s3")
        s3_resource = session.resource(service_name=self._service_name)
        self._client = s3_resource.Bucket(self._bucket)

    def upload_file(self, file) -> str:
        self._client.upload_fileobj(Fileobj=file,
                                    Key=f"{self._path}cat.jpg")
        return (f"https://{self._bucket}.{self._service_name}."
                f"{self._location}.amazonaws.com/{self._path}{file.filename}")

    def s3_put_object(self, body):
        datetime_timestamp = datetime.utcnow().timestamp()
        self._client.put_object(Key=f"{self._path}file_{datetime_timestamp}.jpg", Body=body)
        return (f"https://{self._bucket}.{self._service_name}."
                f"{self._location}.amazonaws.com/{self._path}file_{datetime_timestamp}.jpg")

    def remove_files(self, objects: list[str]) -> None:
        self._client.delete_objects(
            Delete={
                'Objects': [{"Key": f"{self._path}{name}"} for name in objects]
            }
        )
