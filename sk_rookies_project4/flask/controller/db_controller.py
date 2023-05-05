from controller import bp_db as db
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from s3 import S3
import base64

def init_database():
    app = Flask(__name__)
    username = 'admin'
    password = '123456789'
    host     = 'dbdbdb.c5rhgzrich8t.us-west-2.rds.amazonaws.com:3306'
    db_name  = 'db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return SQLAlchemy(app), app

mysql, app = init_database()

@db.route('/login', methods=['get','post'])
def db_login( ):
    uid          = request.form.get('id')
    pwd         = request.form.get('pwd')
    
    try:
        with app.app_context():
            cur = mysql.session.execute(text(
                f"""
                    SELECT * FROM members 
                    WHERE user_id='{uid}'
                    AND passward='{pwd}'
                """
                ))
            if not cur.fetchall() : 
                return redirect(url_for('main_bp.login', uid=uid))
    except Exception as e:
        print(e)
    # redirect(url_for('main_bp.login'))
    
    return redirect(url_for('main_bp.main22'))

@db.route('/register' ,methods=['get','post'])
def register( ):
    uid         = request.form.get('id')
    pwd         = request.form.get('pwd')
    name        = request.form.get('name')
    phone       = request.form.get('phone')
    email       = request.form.get('email')
    employee_id = request.form.get('employee_id')
    
    try:
        with app.app_context():
            cur = mysql.session.execute(text(
                f"""
                    INSERT INTO members 
                    VALUES ( 
                        '{uid}',
                        '{pwd}',
                        '{name}',
                        '{phone}',
                        '{email}',
                        '{employee_id}'
                    )
                """
                ))
            mysql.session.flush()
            mysql.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for('main_bp.login'))
    
@db.route('/double_check', methods=['get','post'])
def double_check( ):
    id          = request.form.get('id')
    
    try:
        with app.app_context():
            cur = mysql.session.execute(text(
                f"""
                    SELECT * FROM members 
                    WHERE user_id='{id}'
                """
                ))
            if not cur.fetchall() :
                message = "사용 가능한 아이디 입니다."
                flash(message)
                return render_template('signup.html',message=message)
                
    except Exception as e:
        print(e)
    message = "아이디가 중복되었습니다"
    flash(message)
    return render_template('signup.html',message=message)
    
@db.route('/image_selector', methods=['get','post'])
def image_selector( ):
    year  = request.form.get('year')
    month = request.form.get('month')
    day   = request.form.get('day')
    file_names = list()
    try:
        with app.app_context():
            cur = mysql.session.execute(text(
                f"""
                    SELECT file_name FROM condition_image 
                    WHERE saved_date 
                    BETWEEN '{year}-{month}-{day} 00:00:00' AND '{year}-{month}-{day} 23:59:59'
                """
                ))
            
            for file_name in cur.fetchall():
                print(file_name)
                s3 = S3()
                s3.connect()
                image = s3.get_image( 'raw_image', file_name[0] )
                print(image)
                encoded_image = base64.b64encode(image).decode('utf-8')
                
                file_names.append(encoded_image)
                break
            
    except Exception as e:
        print(e)
        
    print(file_names)
        
        
    return redirect(url_for('main_bp.start', names=file_names))
    