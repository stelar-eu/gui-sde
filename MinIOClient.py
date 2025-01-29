import minio
from minio import Minio
from minio.error import S3Error


class MinIOClient:
    def __init__(self, bucket_name, credentials):
        self.client = Minio(
            credentials["minio"]["endpoint"],
            access_key=credentials["minio"]["access_key"],
            secret_key=credentials["minio"]["secret_key"],
            secure=True
        )
        self.bucket_name = bucket_name

    def list_files(self):
        try:
            objects = self.client.list_objects(self.bucket_name)

            # Limit view by only showing .txt files
            return [obj.object_name for obj in objects if obj.object_name.endswith('.txt')]
        except S3Error as err:
            print(f"Error occurred: {err}")
            return []

    def load_file(self, file_name):
        try:
            response = self.client.get_object(self.bucket_name, file_name)
            data = response.read().decode('utf-8')
            return data.splitlines()  # Assuming each line is a record
        except S3Error as err:
            print(f"Error occurred: {err}")
            return []
