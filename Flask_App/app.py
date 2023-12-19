from flask import Flask,request,render_template,make_response,jsonify
import mysql.connector
from mysql.connector import Error
import json
import csv
import os
from werkzeug.utils import secure_filename
from datetime import datetime


app=Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/regdata', methods =  ['GET','POST'])
def regdata():
    #Data gathering
    nm=request.args['uname']
    em=request.args['email']
    ph=request.args['phone']
    gen=request.args['gender']
    pswd=request.args['pswd']
    addr=request.args['addr']

    
    #Data transmission to db
    connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
    sqlquery="insert into userdata(uname,email,phone,gender,pswd,addr) values('"+nm+"','"+em+"','"+ph+"','"+gen+"','"+pswd+"','"+addr+"')"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    connection.commit() 
    connection.close()
    cursor.close()
    msg="Data Saved Successfully"
    #return render_template('register.html')
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    #return render_template('register.html',data=msg)
    return resp



@app.route('/logdata', methods =  ['GET','POST'])
def logdata():
    #Data gathering
    em=request.args['email']
    pswd=request.args['pswd']

    
    #Data transmission to db
    connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
    sqlquery="select count(*) from  userdata where email='"+em+"' and pswd='"+pswd+"'"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
    msg=""
    if data[0][0]==0:
        msg="Failure"
    else:
        msg="Success"
    #return render_template('register.html')
    resp = make_response(json.dumps(msg))
    
    print(msg, flush=True)
    #return render_template('register.html',data=msg)
    return resp




    
@app.route('/dataloader')
def dataloader():
    return render_template('dataloader.html')
    
@app.route('/savedataset', methods = ['POST'])
def savedataset():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
        cursor = connection.cursor()
    
        prod_mas = request.files['dt_file']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/Uploads/", filename))

        #csv reader
        fn = os.path.join("./static/Uploads/", filename)

        # initializing the titles and rows list 
        fields = [] 
        rows = []
        
        with open(fn, 'r') as csvfile:
            # creating a csv reader object 
            csvreader = csv.reader(csvfile)  
  
            # extracting each data row one by one 
            for row in csvreader:
                rows.append(row)
                print(row)

        try:     
            #print(rows[1][1])       
            for row in rows[1:]: 
                # parsing each column of a row
                if row[0][0]!="":                
                    query="";
                    query="insert into dataset2 values (";
                    for col in row: 
                        query =query+"'"+col+"',"
                    query =query[:-1]
                    query=query+");"
                print("query :"+str(query), flush=True)
                cursor.execute(query)
                connection.commit()
        except:
            print("An exception occurred")
        csvfile.close()
        
        print("Filename :"+str(prod_mas), flush=True)       
        
        
        connection.close()
        cursor.close()
        return render_template('dataloader.html',data="Data loaded successfully")

    
@app.route('/cleardataset', methods = ['POST'])
def cleardataset():
    print("request :"+str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
        sqlquery="delete from dataset2"
        print(sqlquery)
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        connection.commit() 
        connection.close()
        cursor.close()
        return render_template('dataloader.html',data="Data cleared successfully")
   
@app.route('/planning')
def planning():
    connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
    sqlquery="select * from dataset2"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
    return render_template('planning.html',patdata=data)

@app.route('/predict')
def predict():
    time="19:00"
    time=time+".00"
    print(time)
    return render_template('prediction.html')

@app.route('/pred')
def pred():
    date=request.args['date']
    # date='10/03/2004'
    # time="19:00:00"
    time=request.args['time']
    time=time+":00"
    # date=date[::-1]
    date_object = datetime.strptime(date, '%Y-%m-%d')

# Format the date object as 'dd-mm-yyyy'
    date = date_object.strftime('%d-%m-%Y')
    time=time.replace(":",".")
    date=date.replace("-","/")
    sql = "select Co, PT08, NMHC, C6H6, PT081, NOx, PT082, NO2, PT083, PT084, T, RH, AH FROM dataset2 where Date = '" + date + "' and time = '" + time + "'"
    print(sql)
    connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
    print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    print(data) 
    connection.close()
    cursor.close()
        # Convert the data to a dictionary for JSON serialization
    result = {
        "data": data
    }
    # result=json.dump(result)
    # Return the data in JSON format
    return jsonify(result)


@app.route('/dashboard')
def dashboard():
    connection = mysql.connector.connect(host='localhost',database='skitdb',user='root',password='')
    # sql = "select Co, PT08, NMHC, C6H6, PT081, NOx, PT082, NO2, PT083, PT084, T, RH, AH FROM dataset2 where Date and time"

    cursor = connection.cursor()
    sqlco='select date,PT081,PT082 from dataset2'
    cursor.execute(sqlco)
    dataco=cursor.fetchall()
    # dataco = [[i, int(item[0]), int(item[1])] for i, item in enumerate(dataco)]
    dataco = [[item[0], int(item[1]), int(item[2])] for i, item in enumerate(dataco) if i % 50 == 0]
    sqlco='select T,RH,AH from dataset2'
    cursor.execute(sqlco)
    dataT=cursor.fetchall()
    # dataco = [[i, int(item[0]), int(item[1])] for i, item in enumerate(dataco)]
    dataT = [[item[0], item[1], item[2]] for i, item in enumerate(dataT) if i % 50 == 0]
    # dataT = [[[element.replace(',', '.') for element in row] for row in matrix] for matrix in dataT]

    print(dataco)
    connection.close()
    cursor.close()
    return render_template('dashboard.html',dataco=dataco,dataT=dataT)




if __name__=="__main__":
    app.run(debug=True)