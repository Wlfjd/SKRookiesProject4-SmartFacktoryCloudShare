from s3 import S3
import sqs
import time
import datetime
import requests

cnt = 0
while True:
    file_name = sqs.receive_message()
    print(datetime.datetime.now(),'통신중')

    if file_name :
        file_name = file_name.split('/')[-1]
        print(file_name)
        s3 = S3()
        s3.connect()
        bks = s3.take_bucket()
        img_file = s3.download( bks, file_name )

        # 나중에는 도메인으로 등록하면 되기때문에
        # 지금은 아이피 하드코딩하겠다
        worker_ip = '18.246.48.15'
        
        
        response = requests.get(f'http://{worker_ip}:8000/main/c',params={'file_name':file_name})
        
        
    time.sleep(1)
    

            
    