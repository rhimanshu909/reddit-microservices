from flask import Flask, request, jsonify, g, Response
from passlib.apps import custom_app_context as pwd_context
import sqlite3
import datetime
from passlib.apps import custom_app_context as pwd_context
from dbinstance import get_userdb
from authentication import *

app = Flask(__name__)

#create user other
@app.route('/post/user', methods=['POST'])
def InsertUser():
    if request.method == 'POST':
        executionState:bool = False
        cur = get_userdb().cursor()
        data =request.get_json(force= True)
        try:
            date_created = datetime.datetime.now()
            is_active = 1
            hash_password = pwd_context.hash(data['hashed_password'])
            cur.execute( "INSERT INTO users ( user_name, hashed_password, full_name, email_id, date_created, is_active ) VALUES (:user_name, :hashed_password, :full_name, :email_id, :date_created, :is_active)",
            {"user_name":data['user_name'], "hashed_password":hash_password, "full_name":data['full_name'], "email_id":data['email_id'], "date_created":date_created,"is_active":is_active})
            if(cur.rowcount >=1):
                executionState = True
            get_userdb().commit()

        except:
            get_userdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data Instersted Sucessfully"), 201
            else:
                return jsonify(message="Failed to insert data"), 409


#update user
@app.route('/post/user', methods=['PATCH'])
@requires_auth
def UpdateUser():
    if request.method == 'PATCH':
        executionState:bool = False
        cur = get_userdb().cursor()
        try:
            data  = request.get_json(force=True)
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            hash_password = pwd_context.hash(data['hashed_password'])
            cur.execute("UPDATE users SET hashed_password= :hashed_password WHERE user_name= :user_name AND EXISTS(SELECT 1 FROM users WHERE user_name=:user_name AND is_active=1)", (hash_password, uid, uid))
            if(cur.rowcount >=1):
                executionState = True
                get_userdb().commit()
        except:
            get_userdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Updated SucessFully"), 201
            else:
                return jsonify(message="Failed to update the data"), 409



#delete user
@app.route('/post/user', methods=['DELETE'])
@requires_auth
def DeleteUser():
    if request.method =="DELETE":
        executionState:bool = False
        cur = get_userdb().cursor()
        try:
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("DELETE FROM users where user_name= :user_name ", {"user_name":uid})

            if cur.rowcount >= 1:
                executionState = True
            get_userdb().commit()

        except sqlite3.Error as er:
            print(er)
            get_userdb().rollback()
             #save
        finally:
            if executionState:
                return jsonify(message="Data SucessFully deleted"), 200
            else:
                return jsonify(message="Failed to delete data"), 409
"""
-----------------------------------------------------------------
"""

#127.0/post/user userdata --> user reg, dele, login
#link/post post_data  --> article reg, del,
#insert post

@app.route('/post',methods = ['POST'])
@requires_auth
#remove requires_auth while installing the nginx
def insertPost():
    if request.method == 'POST':
        data = request.get_json(force = True)
        executionState:bool = False
        try:
            cur = get_userdb().cursor()
            current_time= datetime.datetime.now()
            is_active_article=1
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("INSERT INTO post(user_name,title,content,is_active_article,date_created,date_modified,url,community) VALUES (:user_name, :title, :content, :is_active_article, :date_created, :date_modified, :url, :community)", {"user_name":uid,"title":data['title'],"content":data['content'],"is_active_article":is_active_article, "date_created":current_time,"date_modified":current_time,"url":'NULL',"community":data['community']})
            last_inserted_row = cur.lastrowid
            url_post=("http://127.0.0.1:5000/post/"+str(last_inserted_row)+"")
            cur.execute("UPDATE post set url=:url where post_id=:post_id",(url_post,last_inserted_row))
            if(cur.rowcount >=1):
                    executionState = True
            get_userdb().commit()
        except:
            get_userdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Data Inserted Sucessfully"), 201
            else:
                return jsonify(message="Failed to insert data"), 409



#get(retrive) post and get all posts
@app.route('/post',methods = ['GET'])
@requires_auth
#remove requires_auth while installing the nginx
#localhost/post?n
"""


This space is for writing function to:
-- Retrieve an existing post
-- List the n most recent posts to a particular community
-- List the n most recent posts to any community


"""


# update article
@app.route('/post',methods = ['PUT'])
@requires_auth
#remove requires_auth while installing the nginx
def updatePost():
    if request.method == 'PUT':
        executionState:bool = False
        cur = get_userdb().cursor()
        try:
            data = request.get_json(force = True)

            tmod= datetime.datetime.now()
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("select * from post where post_id=:post_id",(data['post_id'],))
            res=cur.fetchall()
            if len(res) >0:
                cur.execute("UPDATE post set title=:title, content=:content, date_modified=:date_modified, url=:url, community=:community where post_id=:post_id and user_name =:user_name", (data['title'],data['content'],tmod,"url":data['url'],"community":data['community'],data['post_id'], uid))
                if(cur.rowcount >=1):
                    executionState = True
                get_userdb().commit()
            else:
                return jsonify(message="Post does not exist"), 409
        except:
            get_userdb().rollback()
            print("Error in update")
        finally:
            if executionState:
                return jsonify(message="Updated Post SucessFully"), 201
            else:
                return jsonify(message="Failed to update Post"), 409


#delete post by post id
@app.route('/post', methods = ['DELETE'])
@requires_auth
#remove requires_auth while installing the nginx
def deletePost():
    if request.method == 'DELETE':
        cur = get_userdb().cursor()
        executionState:bool = False
        try:
            data = request.get_json(force=True)
            uid = request.authorization["username"]
            pwd = request.authorization["password"]
            cur.execute("select * from post where post_id=:post_id",(data['post_id'],))
            res=cur.fetchall()
            if len(res) >0:
                cur.execute("UPDATE post set is_active_article=0 where post_id= :post_id and user_name= :user_name AND EXISTS(SELECT 1 FROM post WHERE user_name=:user_name AND is_active_article=1)",{"post_id":data['post_id'], "user_name":uid})
                row = cur.fetchall()
                if cur.rowcount >= 1:
                    executionState = True
                get_userdb().commit()

        except:
            get_userdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Deleted Article SucessFully"), 200
            else:
                return jsonify(message="Failed to delete Article"), 409



if __name__ == '__main__':
    app.run(debug=True)
