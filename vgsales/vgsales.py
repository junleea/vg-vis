from flask import Flask, request,render_template
import pymysql
from flask_cors import CORS  # 跨域请求模块
from jinja2 import Environment, FileSystemLoader  
from datetime import datetime
import redis
import json,os
from werkzeug.utils import secure_filename
from gevent import pywsgi

app = Flask(__name__,static_folder='./static/assets',template_folder = "./static")
CORS(app)  # 处理跨域请求


@app.route("/get_info", methods=["GET"])
def get_info():
    # list1=[]
    # for i in range(1981,2017):
    #     sql1="SELECT Publisher as p FROM vgsales WHERE Year="+str(i) +" GROUP BY Publisher;"
    #     print(sql1)
    #     resualt1=get_info_mysql(sql1)
    #     list2=[]
    #     for r in resualt1:
    #         try:
    #             sql2="SELECT `Name`, `Platform`, `Year`, `Genre`, `Publisher` FROM vgsales WHERE Year="+str(i)+" AND Publisher='"+r['p']+"';"
    #             resualt2=get_info_mysql(sql2)
    #             m={r['p']:str(resualt2)}
    #             list2.append(m)
    #         except pymysql.Error as e:
    #             print(f"An error occurred while connecting to the database: {e}")
    #     m1={i:str(list2)}
    #     list1.append(m1)
    r = redis.Redis(host='localhost', port=6379, db=0,password="lj502138")
    #r.set('get_info',json.dumps(list1))
    result=json.loads(r.get('get_info'))
    r.close
    return result

@app.route("/get_race_chart_data",methods=["POST"])
def get_race_chart_data():
    data = request.get_json()
    rtype=""
    area=""
    sql=""
    try:
        rtype=data.get('type')
        area=data.get('area')
    except Exception as e:
        print(e)
    # print(data)
    sql="SELECT Year as year,"+str(rtype)+" as name,sum("+str(area)+")*1000 as value FROM vgsales GROUP BY Year,"+str(rtype)+";"
    result = get_info_mysql(sql)
    sql1="SELECT "+str(rtype)+" as name,100 as value FROM vgsales GROUP BY "+str(rtype)+" order by sum("+str(area)+") desc limit 10;"
    result1 = get_info_mysql(sql1)
    for a in range(0,len(result1)):
        result1[a]['value']=100-8*a
    # print(result[0])
    # print(sql)
    response={"word":result1,"race":result}
    return response


@app.route("/get_platform_sale", methods=["GET"])
def get_platform_sale():
    sql = "SELECT Platform,sum(Global_Sales)  as sale FROM vgsales GROUP BY Platform ORDER BY sum(Global_Sales) DESC;"
    sql1 = "SELECT Name FROM vgsales ORDER BY Global_Sales DESC LIMIT 10;"
    result = get_info_mysql(sql)
    return result

@app.route("/get_zx_info",methods=["GET"])
def get_zx_info():
    sql1="SELECT Name as name,(10-Rank)/10 as value FROM vgsales limit 10;"
    sql2="SELECT Publisher as name,sum(Global_Sales) as value from vgsales group by Publisher ORDER BY sum(Global_Sales)  DESC;"
    sql3="SELECT `Genre`, `NA_Sales`, `EU_Sales`, `JP_Sales`, `Other_Sales` FROM `vgsales` GROUP BY `Genre` limit 10;"
    result1=get_info_mysql(sql1)
    # list1=[x['Name'] for x in result1]
    result2=get_info_mysql(sql2)[0:10]
    result3=get_info_mysql(sql3)
    list2=[]
    for x in result3:
        key=x['Genre']
        del x['Genre']
        l=[]
        l.append(x['EU_Sales'])
        l.append(x['JP_Sales'])
        l.append(x['NA_Sales'])
        l.append(x['Other_Sales'])
        d={"name":key,"type":"line","stack":"Total","data":l}
        list2.append(d)
        if len(list2)==10:
            break
    result={"wordcloud":result1,"piechart":result2,"blchart":list2}
    return result

@app.route("/get_map_info", methods=["POST"])
def get_map_info():
    data = request.get_json()
    year = data.get("year")
    sql = (
        "SELECT sum(NA_Sales),sum(EU_Sales),sum(JP_Sales),sum(Other_Sales) FROM vgsales WHERE `Year`= "
        + year
        + ";"
    )
    result = get_info_mysql(sql)
    return result


@app.route("/get_type_data", methods=["GET"])
def get_type_map():
    sql = "select Year,count(Genre),Genre as num from vgsales where Year>1980 group by Year,Genre order by Year; "
    list1 = get_info_mysql(sql)
    sql1="SELECT Genre FROM vgsales group by Genre;"
    list2 = get_info_mysql(sql1)
    list1=[list(x.values()) for x in list1]
    list2=[str(list(x.values())[0]) for x in list2]
    # str1=str(list1)
    # str1=str1.replace("[", "{").replace("]", "}")  
    # s = str1[0].replace(str1[0], "[") + str1[1:]
    # s=s[:-1] + "]"
    
    result={'Genre':str(list2),"data":str(list1)}
    return result

@app.route("/get_type_data1", methods=["GET"])
def get_type_map1():
    sql = "select Year,count(Genre),Genre as num from vgsales group by Year,Genre order by Year; "
    list1 = get_info_mysql(sql)
    sql1="SELECT Genre FROM vgsales group by Genre;"
    list2 = get_info_mysql(sql1)
    list1=[list(x.values()) for x in list1]
    list2=[str(list(x.values())[0]) for x in list2]
    # str1=str(list1)
    # str1=str1.replace("[", "{").replace("]", "}")  
    # s = str1[0].replace(str1[0], "[") + str1[1:]
    # s=s[:-1] + "]"
    
    result={'Genre':list2,"data":list1}

    return result

@app.route("/get_sankey_data",methods=["POST",'GET'])
def get_sankey_data():
    minr=0
    maxr=50
    if request.method == 'POST':
        print(str(request))
        data = dict(request.get_json())
        print(data)
        minr=data['min']
        maxr=data['max']
        if maxr-minr>200:
            minr=maxr-200
    sql1="select DISTINCT Name as source,Genre as target , 1 as value from vgsales where Rank>="+str(minr)+" AND Rank<="+str(maxr)
    location=['NA_Sales', 'EU_Sales','JP_Sales', 'Other_Sales']
    list2=[]
    for l in location:
        sql2="select Genre as source,'"+l+"' as target ,ROUND(NA_Sales % 30) as value from vgsales where Rank>="+str(minr)+" AND Rank<="+str(maxr)+";"
        part2=get_info_mysql(sql2)
        for p in part2:
            list2.append(p)
    list1 = get_info_mysql(sql1)
    gamename=[]
    gtype=['Action','Adventure','Fighting','Misc','Platform','Puzzle','Racing','Role-Playing','Shooter','Simulation','Sports']
    for i in list1:
        s={}
        s['name']=i['source']
        s['depth']=0
        gamename.append(s)
    for i in gtype:
        s={}
        s['name']=i
        s['depth']=1
        gamename.append(s)
    for i in location:
        s={}
        s['name']=i
        s['depth']=2
        gamename.append(s)
    for x in list2:
        list1.append(x)
    #list3=[{"gamename":str(gamename)},{"type":str(gtype)},{"area":str(location)}]
    list3={"gamename":gamename,"type":gtype,"area":location}
    #result=[{"part1":str(list1)},{"part2":str(list2)},{"name":str(list3)}]
    result={"part1":list1,"part2":list2,"name":list3}
    result2={"nodes":gamename,"links":list1}
    return result2

@app.route("/get_publisher_data",methods=['GET'])
def get_publisher_data():
    sql1 = "SELECT Genre FROM vgsales GROUP BY Genre;"
    list1 = get_info_mysql(sql1)
    print(list1)
    result=[]
    for l in list1:
        sql2="SELECT `Rank`, `Name`, `Platform`, `Year`, `Genre`, `Publisher`, `NA_Sales`, `EU_Sales`, `JP_Sales`, `Other_Sales`, `Global_Sales` FROM `vgsales`  WHERE Genre='"+l['Genre']+"' ORDER BY Year;"
        list2 = get_info_mysql(sql2)
        m={l['Genre']:list2}
        result.append(m)
    return result

@app.route("/gps_data", methods=["POST"])
def gps_data():
    data = request.get_json()
    print(data)
    lon = data.get("longitude")
    lat = data.get("latitude")
    speed = data.get("speed")
    ISOTIMEFORMAT = "%Y-%m-%d %H:%M:%S"
    now = datetime.now().strftime(ISOTIMEFORMAT)
    sql1 = "delete from gps_realtime where device_id=%s;"
    sql = "insert into gps_realtime(device_id,gps_time,longitude,latitude,speed) values(%s,%s,%s,%s,%s);"
    print(sql)
    conn = pymysql.connect(
        host="www.ylxteach.net",
        port=3366,
        user="Administrator",
        passwd="XWClassroom20202023",
        db="ydbc2023",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor,
    )
    # 在这里进行数据库操作
    cursor = conn.cursor()
    values = ("2021141461138", str(now), str(lon), str(lat), str(speed))
    #cursor.execute(sql1, ("2021141461138"))
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    list1 = [{"succuss": 0}]
    return list1


def get_info_mysql(sql):
    result = []
    # 使用 cursor() 方法创建一个游标对象 cursor
    try:
        # 创建数据库连接
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="testdb",
            passwd="nbWzJMW73fB7x3BB",
            db="testdb",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
        )
        # 在这里进行数据库操作
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    finally:
        cursor.close()
    return result


@app.route("/post_info", methods=["POST"])
def post_info():
    # 从请求中获取POST数据
    data = request.get_json()
    list = [{"data": str(data)}, {"succuss": 0}]
    # 返回响应
    return list

@app.route("/get_gps_data", methods=["GET"])
def get_gps_data():
    sql1="select id,'../../marker.png' as iconPath,latitude,longitude,30 as width,30 as height,location as title FROM gps_realtime ;"
    sql="select * from gps_realtime;"
    conn = pymysql.connect(
        host="www.ylxteach.net",
        port=3366,
        user="Administrator",
        passwd="XWClassroom20202023",
        db="ydbc2023",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor,
    )
    # 在这里进行数据库操作
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.execute(sql1)
    result1 = cursor.fetchall()
    cursor.close()
    conn.close()
    result={"data":result,"markers":result1}
    return result

@app.route("/get_gps_st_data",methods=["GET"])
def get_gps_st_data():
    sql="SELECT device_id,COUNT(device_id) as num FROM gps_history WHERE gps_time>'2023-01-01 00:00:00' GROUP BY device_id ORDER BY COUNT(device_id) DESC LIMIT 10;"
    sql1="SELECT creator,message_content as message FROM user_chat ORDER BY send_time DESC LIMIT 5;"
    conn = pymysql.connect(
        host="www.ylxteach.net",
        port=3366,
        user="Administrator",
        passwd="XWClassroom20202023",
        db="ydbc2023",
        charset="utf8",
        cursorclass=pymysql.cursors.DictCursor,
    )
    # 在这里进行数据库操作
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.execute(sql1)
    result1=cursor.fetchall()
    title="2023 GPS数据前十"
    data=[]
    categories=[]
    for r in result:
        data.append(r['num'])
        categories.append(r['device_id'])
    msg_result={}
    for a,i in enumerate(result1):
        msg_result['message'+str(a)]=i['message']
        msg_result['creator'+str(a)]=i['creator']
    result1={"title":title,"data":data,"categories":categories,"message": msg_result}
    return result1

# 上传图片
@app.route('/upload',methods=['GET','POST'])
def upload_images():
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    UPLOAD_FOLDER = 'images/'
    if request.method == 'POST':
        print('request======>',request.files.get('file').filename) #get('photo')是input标签 name的名称，切忌写错！
        file = request.files['file']
        if file and file.filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            url = UPLOAD_FOLDER+filename
            return {"code":200,"url":url}
    else:
        return render_template('hello.html')

@app.route('/',methods=['GET','POST'])
def init():
    return render_template('index.html')

if __name__ == "__main__":
    static_folder='./static' #设置静态文件夹目录
    app.config["JSON_AS_ASCII"] = False
    app.config["UPLOAD_FOLDER"] = "images/"
    # 以下是服务器对外公开可以改为:app.run()
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    # server.serve_forever()
    app.run(host="0.0.0.0", port=5000)
