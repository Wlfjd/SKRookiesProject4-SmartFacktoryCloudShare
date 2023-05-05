from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from controller import bp_main as main
from s3 import S3

@main.route('/', methods=['get','post'])
def home():
    return render_template( 'main.html' )
    
@main.route('/main22', methods=['get','post'])
def main22():
    return render_template('main22.html')

@main.route('/login', methods=['get','post'])
def login():
    uid = request.args.get('uid')
    return render_template('login.html', uid=uid)

@main.route('/signup', methods=['get'])
def signup():
    return render_template('signup.html')

@main.route('/start', methods=['get'])
def start():
    names = request.args.getlist('names')
    print(names)
    return render_template('start.html', names=names)

@main.route('/find', methods=['get'])
def find():
    return render_template('find.html')

@main.route('/aboutus', methods=['get'])
def aboutus():
    return render_template('aboutus.html')

@main.route('/test', methods=['get'])
def test():
    return render_template('test.html')
    
@main.route('/c', methods=['get','post'])
def home2( ):
    
    file_name = request.args.get('file_name')
    s3 = S3()
    s3.connect()
    bks = s3.take_bucket()
    img_file = s3.download( bks, file_name )
    
    return 'get요청을 받았습니다.'
    
@main.route('/upload')
def upload():
    
    file_name='204_101_20_ffb2c9f4-3ab6-4ce6-b160-92933443ee1e.jpg'
    s3 = S3()
    s3.connect()
    bks = s3.take_bucket()
    s3.upload(bks, img='./image/'+ file_name, file_name=file_name)
    return '업로드를 시작합니다'
    