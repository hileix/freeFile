import re
import sys
import json
import redis
# import pymysql
import subprocess
from flask_cors import CORS
from flask import render_template,redirect
from flask import Flask,request,Response,jsonify

app = Flask(__name__)
CORS(app, resources=r'/*')


# redisCli = redis.Redis(host=redisDb, port=6379, decode_responses=True, db=0)  


@app.route('/applyupload')
def Upload():
    FIN = request.args.get("FIN")
    time = request.args.get("time")
    expiredTime = request.args.get("expired")
    nameSpace = request.args.get("nameSpace")
    fileName = request.args.get("fileName")
    if isinstance(FIN, str) or isinstance(nameSpace, str):
        # 接下来先检查是否存在FIN, 没有则将文件信息写入数据库[Mysql]
        # 返回准许上传的临时Url
        if isinstance(expiredTime, str):
            result = subprocess.check_output("mc share upload minio/test/"+FIN, shell=True)
            shareUrl = re.findall(r"Share: ([a-zA-Z0-9\.\/\:\-\s\=\_\@]+)<FILE>", str(result))[0]
            response = Response(json.dumps({"message":"Success Get share power", "shareUrl":shareUrl, "statusCode":200}), mimetype = 'application/json')
        else:
            if 'h' in expiredTime or 'm' in expiredTime or 's' in expiredTime:
                result = subprocess.check_output("mc share upload --expire %s minio/test/%s"%(expiredTime, FIN), shell=True)
                shareUrl = re.findall(r"Share: ([a-zA-Z0-9\.\/\:\-\s\=\_\@]+)<FILE>", str(result))[0]
                response = Response(json.dumps({"message":"Success Get share power", "shareUrl":shareUrl, "statusCode":200}), mimetype = 'application/json')
            else:
                response = Response(json.dumps({"message":"Unprocessable Entity.", "statusCode":422}), mimetype = 'application/json')
    else:
        response = Response(json.dumps({"message":"Argument Error", "shareUrl":"", "statusCode":422}), mimetype = 'application/json')

    response.headers.add('Server','python flask')       
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'            
    return response


@app.route('/applydownload')
def Download():

    FIN = request.args.get("FIN")
    time = request.args.get("time")
    expiredTime = request.args.get("expired")    
    name = request.args.get("nameSpace/fileName")
    try:

        if FIN != None or FIN != "":
            result = subprocess.check_output("mc share download --expire %s minio/test/%s"%(expiredTime, FIN), shell=True)
        elif name != None or name != "":
            result = subprocess.check_output("mc share download --expire %s minio/test/%s"%(expiredTime, name), shell=True)

        shareUrl = re.findall(r"Share: ([a-zA-Z0-9\.\/\:\-\s\=\_\@]+)", str(result))[0]
        
        response = Response(json.dumps({"message":"Success Get share power", "shareUrl":shareUrl, "statusCode":200}), mimetype = 'application/json')
    except:
        response = Response(json.dumps({"message":"Server Error", "shareUrl":"", "statusCode":500}), mimetype = 'application/json')
    finally:
        response.headers.add('Server','python flask')       
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'            
        return response




    

# @app.before_request
# def redirect():
#     AceessToken = request.headers['AceessToken']
#     ipaddr = request.headers['ipaddress']
#     ip = request.remote_addr
#     if ip != ipaddr or AceessToken == None or AceessToken == '':
#         return {"statusCode":"404", 
#                 "body": json.dumps('Forbiden Request.')}
#     else:
#         pass        
#         # if redisCli.get(token):
#             # pass
            
if __name__ == '__main__':

    app.run(host="127.0.0.1", port=int(9090), debug = True)



