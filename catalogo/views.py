from rest_framework.views import APIView
from rest_framework.response import Response

from .s3 import S3Uploader

class UploadImageView(APIView):
    def __init__(self, uploader: S3Uploader):
        self.uploader = uploader

    def post(self, request):
        file = request.data.get('file')
        file_name = file.name
        file_data = file.read()
        url = self.uploader.upload_image(file_name, file_data)
        return Response({'url': url})