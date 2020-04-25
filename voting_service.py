from flask import Flask, Flask,request, g, jsonify
from flask_restful import Resource, Api
import json
import sqlite3
import datetime
from DatabaseInstance import get_db
from authentication import *
from multiprocessing import Value


app = Flask(__name__)
api = Api(app, prefix="/api/v1")

'''
Upvote a post
Downvote a post
Report the number of upvotes and downvotes for a post
List the n top-scoring posts to any community
Given a list of post identifiers, return the list sorted by score.

5 --> [1,2, 3,4, 5]
i =0 
while i <len(up):
    scor

'''

'''

    return jsonify(count=out)

conn.execute('CREATE TABLE if not exists users (user_name TEXT PRIMARY KEY NOT NULL,  hashed_password TEXT NOT NULL, full_name TEXT NOT NULL, email_id TEXT NOT NULL,  date_created DATE NOT NULL, is_active INTEGER NOT NULL)')
conn.execute('CREATE TABLE if not exists post (post_id INTEGER PRIMARY KEY NOT NULL, user_name TEXT NOT NULL, title TEXT, content TEXT NOT NULL, is_active_article TEXT, date_created INTEGER, date_modified INTEGER, url TEXT, community TEXT, UpVote INT, DownVote INT,FOREIGN KEY (user_name) REFERENCES users(user_name))')

print("Successfully created reddit database")
conn.close()


'''
@api.route("/voting/upvote/<int:id>")
class UpVote(Resource):
    def post(self, id):
        data = request.get_json(force = True)
        executionState:bool = False
        try:
            cur = get_db().cursor()
            counter = cur.execute("SELECT UpVote from post WHERE post_id="+id)
            counter += 1
            cur.execute("UPDATE post set UpVote=? where post_id=?", (counter, id))
            if(cur.rowcount >=1):
                    executionState = True
            get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Upvote Sucessfully done"), 201
            else:
                return jsonify(message="Failed to upvote a post"), 409

@api.route("voting/downvote/<int:id>")
class DownVote(Resource):
    def post(self, id):
        executionState:bool = False
        try:
            cur = get_db().cursor()
            counter = cur.execute("SELECT UpVote from post WHERE post_id="+id)
            if counter >0:
                counter -= 1
                cur.execute("UPDATE post set DownVote=? where post_id=?", (counter, id))
            if(cur.rowcount >=1):
                    executionState = True
            get_db().commit()
        except:
            get_db().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="DownVote Sucessfully done"), 201
            else:
                return jsonify(message="Failed to upvote a post"), 409
                
@api.route("/voting")
class Post(Resource):
    def get(self, id):
        executionState:bool = False
        cur = get_db().cursor()
        post_id = request.args.get('post_id')
        community = request.args.get('community')
        try:
            executionState = True
            data = request.get_json(force = True)
            if post_id is not None and community is None:
                cur.execute("SELECT UPVote, DownVote from post WHERE post_id=?", (id,))
                UpVote, DownVote = cur.fetchall()
                get_db().commit()
                if UpVote == 0 and DownVote == 0:
                    return "No such value exists\n", 204
                return jsonify((UpVote, DownVote)), 200
            if post_id is None and community is not None:
                cur.execute("SELECT UPVote from post WHERE community=?", (community,))
                UpVote = cur.fetchall()
                cur.execute("SELECT DownVote from post WHERE community=?", (community,))
                DownVote = cur.fetchall()
                i = 0
                scoreList = []
                while i<len(UpVote):
                    scoreList.append(UpVote[i]-DownVote[i])
                score = max(scoreList)
                return jsonify(score), 200
            if post_id is None and community is  None:
                UpVote_result = []
            downvote_Result = []
            for post_id in data:
                upvote = cur.execute("SELECT UPVote from post WHERE post_id=?", (post_id,))
                UpVote_result.append(upvote)
                downvote = cur.execute("SELECT DownVote from post WHERE post_id=?", (post_id,))
                downvote_Result.append(downvote)
            i = 0
            scoreList = []
            while i<len(UpVote_result):
                scoreList.append(UpVote[i]-DownVote[i])


            Z = [x for _,x in sorted(zip(scoreList, list(data)))]
            return jsonify(Z), 200

        except:
            get_db().rollback() #if it fails to execute rollback the database
            executionState = False

        finally:
            if executionState == False:
                return jsonify(message="Fail"), 204
    #score by comminuty
    # def get(self, community):
    #     executionState:bool = False
    #     cur = get_db().cursor()
    #     try:
    #         executionState = True
    #         if community is not None:

    #     except:
    #         get_db().rollback() #if it fails to execute rollback the database
    #         executionState = False

    #     finally:
    #         if executionState == False:
    #             return jsonify(message="Fail"), 204