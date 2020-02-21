import flask
from flask import request, jsonify
from Crypto.Cipher import Blowfish
import json
from datetime import datetime
from datetime import timedelta
import mysql.connector


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/addUser', methods=['POST'])
def useradd():
    if  "value" in request.form:
        now = datetime.now()
        for i in range(0,10):
            cipher = Blowfish.new((now - timedelta(seconds=i)).strftime("%Y%d%S%m%H%M"))
            x=str(cipher.decrypt(str(request.form["value"]).encode('utf-8').decode('unicode-escape').encode('latin-1')))
            if "\"state\": \"okey\"" in x:
                if x.find("}*")!=-1:
                    json_txt=json.loads(str(x[2:x.find("}*")+1]))
                else:
                    json_txt = json.loads(str(x[2:len(x)-1]))

                cnx = mysql.connector.connect(user='root', password='1234',
                                              host='127.0.0.1', database='ilf',auth_plugin='mysql_native_password')
                cursor = cnx.cursor()
                sql = "INSERT INTO user (user_name,user_nickname,user_hashpass,user_gsm,user_city_id,user_district_id,user_country_id,user_town_id,user_neighborhood_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (
                    json_txt["user_name"], json_txt["user_nickname"], json_txt["user_hashpass"], json_txt["user_gsm"], json_txt["user_city_id"], json_txt["user_district_id"], json_txt["user_country_id"], json_txt["user_town_id"], json_txt["user_neighborhood_id"])
                cursor.execute(sql, val)

                cnx.commit()
                id=cursor.lastrowid
                cursor.close()
                cnx.close()
                task = {
                    'done':True,
                    'id':id
                }
                return jsonify({'state': task}), 201
        return "hata"
    else :
        return "hop2"

"""@app.route('/useradd', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        return request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
"""
app.run()