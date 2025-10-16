import minio
import streamlit as st
from minio import Minio
from minio.error import S3Error


class MinIOClient:
    secret_key = None
    session_token = None
    credentials = None

    def __init__(self, bucket_name, credentials):
        self.client = Minio(
            endpoint=credentials["minio"]["endpoint"],
            access_key=credentials["minio"]["access_key"],
            secret_key=credentials["minio"]["secret_key"],
            session_token=credentials["minio"]["session_token"],
            secure=True
        )
        self.bucket_name = bucket_name
        self.credentials = credentials

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

    def get_object(self, bucket_name, object_name):
        try:
            response = self.client.get_object(bucket_name, object_name)
            data = response.read().decode("utf-8").split("\n")
            response.close()
            response.release_conn()
            return data
        except S3Error as err:
            st.write(f"Error occurred: {err}")
            return None

    def object_exists(self, bucket_name, object_name):
        try:
            self.client.stat_object(bucket_name, object_name)
            return True
        except S3Error as err:
            print(f"Object does not exist: {err}")
            return False

    def load_file_bucketname(self, bucket_name, file_name):
        try:
            response = self.client.get_object(bucket_name, file_name)
            data = response.read().decode('utf-8')
            return data.splitlines()  # Assuming each line is a record
        except S3Error as err:
            print(f"Error occurred: {err}")
            return []

    def get_secret_key(self):
        return self.secret_key

    def get_session_token(self):
        return self.session_token
