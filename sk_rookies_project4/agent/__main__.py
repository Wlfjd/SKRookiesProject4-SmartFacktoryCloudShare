from s3 import S3
from DataGen import DataGen
from model import Model
import numpy as np
from PIL import Image 
import sqs
import time
from PIL import Image 
import cv2
import os
import mysql.connector
import glob
import datetime

def preprocess_mask(s3, prd, file_name):
    rsize_mask     = np.reshape(prd, (128,128))
    rsize_mask     = Image.fromarray((rsize_mask * 255).astype(np.uint8))
    rsize_mask     = np.reshape(rsize_mask, (128,128,1))
    file_name = file_name.split('/')[-1]
    cv2.imwrite( './agent/mask/' + file_name , rsize_mask )
    
    s3.upload(bks, img='./agent/mask/' + file_name, file_name='mask_'+ file_name)
    
def save_img_info_from_db(file_name, form=0, condition=0):
    config = {
      'user': 'admin',
      'password': '123456789',
      'host': 'dbdbdb.c5rhgzrich8t.us-west-2.rds.amazonaws.com:3306',
      'database': 'db'
    }
    
    # RDS에 연결
    cnx = mysql.connector.connect(**config)
    
    # 연결된 커서 가져오기
    cursor = cnx.cursor()
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    
    
    # SQL 쿼리 실행
    query = f"""
        insert into condition_image
        values ('{file_name}','{formatted_date}', 1, 1)
    """

    cursor.execute(query)

    
    # 결과 가져오기
    for result in cursor:
        print(result)
    
    # 커넥션 닫기
    cnx.close() 

if __name__=='__main__':

    # 이미지 가져오기
    

    while True:
        file_name = sqs.receive_message()
        

        if file_name :
            file_name = file_name.split('/')[-1]
            print(file_name)
            
            s3 = S3()
            s3.connect()
            bks = s3.take_bucket()
            img_file = s3.download( bks, file_name )
            
            model = Model()
            prds = model.predict(DataGen('./agent/image', batch_size=5))
            
            for prd in prds:
                preprocess_mask(s3, prd,file_name)
            
            save_img_info_from_db(file_name, form=0, condition=0)

            for file in glob.glob('./agent/image/*') :
              os.remove(file)
             
            for file in glob.glob('./agent/mask/*') :
              os.remove(file)

        time.sleep(1)
        
            
    