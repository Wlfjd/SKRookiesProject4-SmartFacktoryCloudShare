import boto3
from io import BytesIO
from flask import send_file

class S3:
    def __init__(self):
        self.s3        = None
        self.s3_client_download = None
        self.s3_client_upload   = None
        self.BUCKET_NAME        = 's3-mask'
        self.UPLOAD_BUCKET_NAME = 's3-carscratch'

    def connect(self):
        self.s3        = boto3.resource('s3')
        self.s3_client_download = boto3.client('s3')
        self.s3_client_upload   = boto3.client('s3')
        
    def take_bucket(self):
        bks = [ bk.name for bk in self.s3.buckets.all() ]
        
        return bks
        
    def upload(self, bks, img, file_name):

        folders     = ['raw_image','mask','','']

        for bk in bks:
            if bk == self.UPLOAD_BUCKET_NAME:
                print('업로드 완료')
                self.s3_client_upload.upload_file( img, bk, f'{ folders[0] }/{ file_name }' )
                
                
    def download(self, bks, file_name):
        folders     = ['raw_image','mask','','']
        
        self.s3_client_download.download_file(
            self.BUCKET_NAME, 
            f'{ folders[1] }/{ file_name }',
            f'./mask/{ file_name }'
            )
            
        print('다운로드 완료')
   
        return f'./{__name__}/{file_name}'
        
    def get_image(self, folder, file_name):
        # S3 버킷에서 이미지 객체를 가져옴
        s3_object = self.s3_client_download.get_object(Bucket=self.UPLOAD_BUCKET_NAME, Key=f'{folder}/{file_name}.jpg')
        # 이미지 객체의 데이터를 BytesIO 객체에 저장
        image_data = BytesIO(s3_object['Body'].read())
        # 이미지 데이터를 send_file 함수를 사용하여 전송
        return send_file(image_data, mimetype='image/jpeg')

               