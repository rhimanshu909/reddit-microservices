from flask import Flask, Flask,request, g, jsonify
from flask_restful import Resource, Api
import json
import sqlite3
import datetime
from dbinstance import get_userdb
from authentication import *
from multiprocessing import Value


app = Flask(__name__)


#helper function to convert the string values to integer in a list
def convert_string_to_integer_list(array):
    for i in range(0, len(array)): 
        array[i] = int(array[i])
    return array

#Upvote a post
@app.route('/voting/upvote',methods = ['POST'])
def UpVote():
    if request.method == 'POST':
        executionState:bool = False
        post_id = request.args.get('post_id')
        cur = get_userdb().cursor()
        try:     
            counter = cur.execute("Update post Set UpVote = UpVote + 1 WHERE post_id=?",(post_id,))
            if(cur.rowcount >=1):
                    executionState = True
            get_userdb().commit()
        except:
            get_userdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="Upvote Sucessfully done"), 201
            else:
                return jsonify(message="Failed to upvote a post"), 409

#Downvote a post

@app.route('/voting/downvote',methods = ['POST'])
def DownVote():
    if request.method == 'POST':
        post_id = request.args.get('post_id')
        executionState:bool = False
        try:
            cur = get_userdb().cursor()
            cur.execute("SELECT UpVote from post WHERE post_id="+post_id)
            counter = cur.fetchone()
            print(counter)
            if counter[0] >0:
                counter = counter[0]-1
                cur.execute("UPDATE post set DownVote=? where post_id=?", (counter, post_id))
            if(cur.rowcount >=1):
                    executionState = True
            get_userdb().commit()
        except:
            get_userdb().rollback()
            print("Error")
        finally:
            if executionState:
                return jsonify(message="DownVote Sucessfully done"), 201
            else:
                return jsonify(message="Failed to upvote a post"), 409

'''
Report the number of upvotes and downvotes for a post
List the n top-scoring posts to any community
Given a list of post identifiers, return the list sorted by score.
'''
                
@app.route('/voting',methods = ['GET'])
def Voting():
    executionState:bool = False
    cur = get_userdb().cursor()
    post_id = request.args.get('post_id')
    community = request.args.get('community')
    data = request.args.getlist('post_ids')
    print(data)
    try:
        executionState = True

        #Report the number of upvotes and downvotes for a post
        if post_id is not None and community is None:
            cur.execute("SELECT UpVote, DownVote from post WHERE post_id=?", (post_id,))
            res=cur.fetchall()
            UpVote, DownVote = res[0]
            get_userdb().commit()
            if UpVote == 0 and DownVote == 0:
                return "No such value exists\n", 204
            return jsonify((UpVote, DownVote)), 200

        #List the n top-scoring posts to any community
        if post_id is None and community is not None:
            cur.execute("SELECT UPVote from post WHERE community=?", (community,))
            UpVote = cur.fetchall()
            cur.execute("SELECT DownVote from post WHERE community=?", (community,))
            DownVote = cur.fetchall()
            i = 0
            scoreList = []
            while i<len(UpVote):
                scoreList.append(UpVote[i][0]-DownVote[i][0])
                i += 1
            score = max(scoreList)
            return jsonify(score), 200

        #Given a list of post identifiers, return the list sorted by score.
        if post_id is None and community is None and data is not None:
            UpVote_result = []
            downvote_Result = []
            post_ids_data = ' '.join(data)[1:-1]
            post_ids_data_list = post_ids_data.split(',')
            convert_string_to_integer_list(post_ids_data_list)
            for post_id in post_ids_data_list:
                cur.execute("SELECT UPVote from post WHERE post_id=? ", (post_id,))
                upvote = cur.fetchone()
                UpVote_result.append(upvote[0])
                cur.execute("SELECT DownVote from post WHERE post_id=?", (post_id,))
                downvote = cur.fetchone()
                downvote_Result.append(downvote[0])
            i = 0
            scoreList = []
            while i <len(UpVote_result):
                if UpVote_result[i] is not None and downvote_Result[i] is not None:
                    scoreList.append(UpVote_result[i]-downvote_Result[i])
                i += 1
            print(scoreList)
            Z = [x for _,x in sorted(zip(scoreList, post_ids_data_list))]
            return jsonify(Z), 200

    except:
        get_userdb().rollback() #if it fails to execute rollback the database
        executionState = False

    finally:
        if executionState == False:
            return jsonify(message="Fail"), 204

if __name__ == '__main__':
    app.run(debug=True, port=5002)