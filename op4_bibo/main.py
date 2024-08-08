from flask import Flask,render_template, request, jsonify, redirect
import math
import time
from datetime import date
from datetime import datetime
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import mysql.connector

#charset_1=lat
#charset_22=long


app = Flask(__name__,template_folder="templates")

mydb = mysql.connector.connect(
    host="localhost",
    database="BiboData",
    user="Rahul",
    password="Rahul@2004VJ"
)

db = mydb.cursor(buffered=True) 


def decrypt(enc,key,iv):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc),16)


key = 'AAAAAAAAAAAAAAAA'
iv =  'BBBBBBBBBBBBBBBB'.encode('utf-8')

def day_calc(date1, date2):
    # Assume date2 > date1 using date_function

    day1 = int(date1[0:2])
    month1 = int(date1[2:4])
    year1 = int(date1[4:8])

    day2 = int(date2[0:2])
    month2 = int(date2[2:4])
    year2 = int(date2[4:8])

    date_a = date(year1, month1, day1)
    date_b = date(year2, month2, day2)
    delta = date_b - date_a

    return delta.days

@app.route("/")
def hello():
    mydb = mysql.connector.connect(
    host="localhost",
    database="BiboData",
    user="Rahul",
    password="Rahul@2004VJ")

    db = mydb.cursor(buffered=True)
    today = str(time.strftime("%d%m%Y"))
    print(today)
    dates = db.execute("SELECT date FROM data GROUP BY date")
    dates=db.fetchall()

    '''for day in dates:
        day = day[0]
        if day == None:
            break
        else:
            if day_calc(day, today) > 60:
                db.execute("DELETE FROM data WHERE date = %s", (day,))'''
            
    table_data_1 = db.execute("SELECT trp_name AS name, bookin_time, bookout_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND plt = %s) ORDER BY bookin_time DESC", (today, 1))
    table_data_1 = db.fetchall()
    print("table_data_1:",table_data_1)
    table_data_2 = db.execute("SELECT trp_name AS name, bookin_time, bookout_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND plt = %s) ORDER BY bookin_time DESC", (today, 2))
    table_data_2 = db.fetchall()
    table_data_3 = db.execute("SELECT trp_name AS name, bookin_time, bookout_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND plt = %s) ORDER BY bookin_time DESC", (today, 3))
    table_data_3 = db.fetchall()
    table_data_4 = db.execute("SELECT trp_name AS name, bookin_time, bookout_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND plt = %s) ORDER BY bookin_time DESC", (today, 4))
    table_data_4 = db.fetchall()
    table_data_5 = db.execute("SELECT trp_name AS name, bookin_time, bookout_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND plt = %s) ORDER BY bookin_time DESC", (today, 5))
    table_data_5 = db.fetchall()
    table_data_6 = db.execute("SELECT trp_name AS name, bookin_time, bookout_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND plt = %s) ORDER BY bookin_time DESC", (today, 6))
    table_data_6 = db.fetchall()
    table_data_7 = db.execute("SELECT trp_name AS name, bookin_time, bookout_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND plt = %s) ORDER BY bookin_time DESC", (today, 7))
    table_data_7 = db.fetchall()
    trp = db.execute("SELECT trp_name FROM trp order by plt, trp_name asc;")
    trp = db.fetchall()
    print(trp)
    
    mydb.commit()
    
    return render_template('index.html', today=today, table_data_1=table_data_1, table_data_2=table_data_2, table_data_3=table_data_3, table_data_4=table_data_4, table_data_5=table_data_5, table_data_6=table_data_6, table_data_7=table_data_7, trp=trp)
    


@app.route('/process', methods=['POST'])

def process():
    mydb = mysql.connector.connect(
    host="localhost",
    database="BiboData",
    user="Rahul",
    password="Rahul@2004VJ")

    db = mydb.cursor(buffered=True)

    data = request.get_json() # retrieve the data sent from JavaScript
    # process the data using Python code
    name = str(data['trp'])
    print("The name given isssssssssssssssss:",name*2+"8")
    type = str(data['type'])
    lat=data['lat1']
    long=data['long1']
    decrypt_lat=decrypt(enc=lat,key=key,iv=iv)
    decrypt_long=decrypt(enc=long,key=key,iv=iv)
    my_lat = float(decrypt_lat.decode("utf-8", "ignore"))
    my_long =float(decrypt_long.decode("utf-8", "ignore"))
    iti_lat = 1.33948
    iti_long = 103.68446

    today = str(time.strftime("%d%m%Y"))
    x = (my_lat - iti_lat)**2
    y = (my_long - iti_long)**2
    dist = math.sqrt(x+y)

    info = db.execute("SELECT id, book_status FROM trp WHERE trp_name = %s", (name,))
    info = db.fetchall()
    print("info:",info)
    
    
    if info!=[]:
        id = info[0][0]
        status = info[0][1]
        today = str(time.strftime("%d%m%Y"))
        name = str(data['trp'])
        date_in = db.execute("SELECT bookin_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND trp.trp_name = %s)", (today, name))
        date_in = db.fetchall()
        #date_in=date_in[0]
        print("date_in:",date_in)
        date_out = db.execute("SELECT bookout_time FROM data JOIN trp ON data.data_id = trp.id WHERE (date = %s AND trp.trp_name = %s)", (today, name))
        date_out = db.fetchall()
        #date_out = date_out[0]
        print("date_out:",date_out)
        
        if date_in != []:
            date_in = date_in[0][0]
        else:
            date_in = None

        if date_out != []:
            date_out = date_out[0][0]
        else:
            date_out = None
        

        if (str(type) == str(status)) or (date_in != None and date_out != None):
            print(str(type) == str(status),(date_in != None), (date_out != None),str(type),str(status))
            result = "Cannot book in/out twice consecutively"

        elif type == "IN":
            if dist > 0.004:
                result = "Not in camp"

            else:
                today = str(time.strftime("%d%m%Y"))
                now = time.strftime("%H:%M:%S")
                name = str(data['trp'])
                ip = str(data['ip'])


                check_data = db.execute("SELECT * FROM data JOIN trp ON data.data_id = trp.id WHERE date = %s", (today,))
                check_data=db.fetchall()
                print("check_data:",check_data)

                if check_data != []:
                    for x in check_data:
                        if str(x[6]) == str(name):
                            if x[1] != None:
                                result = "Form already submitted"
                                break

                        if str(x[4]) == str(ip):
                            if x[1] != None:
                                result = "Form already submitted"
                                break

                    else:
                        prev = db.execute("SELECT bookout_time FROM data join trp on data.data_id = trp.id WHERE (date = %s AND trp_name = %s)", (today, name))
                        prev = db.fetchall()
                        print("prev_table:",prev)

                        if prev == "" or prev == [] or prev == {}:
                            db.execute("INSERT INTO data (data_id, bookin_time, date, ip) VALUES (%s,%s,%s,%s)", (id, now, today, ip))

                        else:
                            db.execute("UPDATE data SET bookin_time = %s WHERE (data_id = %s AND date = %s)", (now, id, today))

                        db.execute("UPDATE trp SET book_status = 'IN' WHERE trp_name = %s", (name,))
                        result = "Booked In"



                else:
                    print("cool I am here")
                    db.execute("INSERT INTO BiboData.data (data_id, bookin_time, date, ip) VALUES (%s,%s,%s,%s)", (id, now, today, ip))
                    print("cool next step")
                    db.execute("select * from data;")
                    print("data_table:",db.fetchall())
                    db.execute("UPDATE trp SET book_status = 'IN' WHERE trp_name = %s", (name,))
                    print("cooler next step")
                    result = "Booked In"



        elif type == "OUT":
            if dist > 0.004:
                result = "Must be in camp to register bookout"

            else:
                today = str(time.strftime("%d%m%Y"))
                now = time.strftime("%H:%M:%S")
                name = str(data['trp'])
                ip = str(data['ip'])

                check_data = db.execute("SELECT * FROM data JOIN trp ON data.data_id = trp.id WHERE date = %s", (today,))
                check_data = db.fetchall()
                if check_data != []:
                    for x in check_data:
                        if str(x[6]) == str(name):
                            if x[2] != None:
                                result = "Form already submitted"
                                break

                        if str(x[4]) == str(ip):
                            if x[2] != None:
                                result = "Form already submitted"
                                break



                    else:
                        prev = db.execute("SELECT bookin_time FROM data join trp on data.data_id = trp.id WHERE (date = %s AND trp_name = %s)", (today, name))
                        prev =db.fetchall()

                        if prev == "" or prev == [] or prev == {}:
                            db.execute("INSERT INTO data (data_id, bookout_time, date, ip) VALUES (%s,%s,%s,%s)", (id, now, today, ip))

                        else:
                            db.execute("UPDATE data SET bookout_time = %s WHERE (data_id = %s AND date = %s)", (now, id, today))

                        db.execute("UPDATE trp SET book_status = 'OUT' WHERE trp_name = %s", (name,))
                        result = "Booked Out"


                else:
                    db.execute("INSERT INTO data (data_id, bookout_time, date, ip) VALUES (%s,%s,%s,%s)", (id, now, today, ip))
                    db.execute("UPDATE trp SET book_status = 'OUT' WHERE trp_name = %s", (name,))
                    result = "Booked Out"

        else:
            result = "Choose correct type"
    else:
        result="please select valid name"
    mydb.commit()


    return jsonify(result=result)


@app.route('/history', methods=["GET", "POST"])
def view():
    mydb = mysql.connector.connect(
    host="localhost",
    database="BiboData",
    user="Rahul",
    password="Rahul@2004VJ")

    db = mydb.cursor(buffered=True)
    if request.method == "GET":
        names = db.execute("SELECT trp_name FROM trp")
        names = db.fetchall()
        return render_template('history.html',names=names)

    else:
        key = request.form.get("key")
        check_date = request.form.get("date")
        plt = request.form.get("plt")
        name = request.form.get("name")
        
        """if key != "OPFOR":
            message = "Incorrect Key"
            return render_template("error.html", message=message)


        data = db.execute("SELECT trp_name, bookin_time AS bookin, bookout_time AS bookout FROM data JOIN trp ON trp.id = data.data_id WHERE (date = %s AND plt = %s) order by trp_name", (check_date, plt))
        data = db.fetchall()
        return render_template("view.html", data=data, date=check_date)"""
        
        if name != "" and plt != "":
            message = "Choose either name or platoon"
            return render_template("error.html", message=message)

        if name != "" and (check_date != "" or plt != ""):
            message = "Only enter neccessary details"
            return render_template("error.html", message=message)

        elif name == "" and (check_date == "" or plt == ""):
            message = "Enter neccessary details"
            return render_template("error.html", message=message)

        if key != "OPFOR2023":
            message = "Incorrect Key"
            return render_template("error.html", message=message)


        if name == "":
            data = db.execute("SELECT trp_name AS type, bookin_time AS bookin, bookout_time AS bookout FROM data JOIN trp ON trp.id = data.data_id WHERE (date = %s AND plt = %s)", (check_date, plt))
            data = db.fetchall()
            type = "Name"
            other_type = check_date

        else:
            data = db.execute("SELECT date AS type, bookin_time AS bookin, bookout_time AS bookout FROM data JOIN trp ON trp.id = data.data_id WHERE trp_name = %s", (name,))
            data = db.fetchall()
            type = "Date"
            other_type = name


        return render_template("view.html", data=data, other_type=other_type, type=type, plt=plt)
        
    mydb.commit()

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == "GET":
        return render_template("settings.html")

    else:
        key = request.form.get("key")


        if key != "OPFOR2023":
            message = "Incorrect Key"
            return render_template("error.html", message=message)


        loops = []
        for x in range(35):
            x += 1
            number = x
            name = "name" + str(x)
            y = {'name': name, 'number': number}
            loops.append(y)

        return render_template("restricted.html", loops=loops)


@app.route('/restricted', methods=['POST'])
def edit():
    mydb = mysql.connector.connect(
    host="localhost",
    database="BiboData",
    user="Rahul",
    password="Rahul@2004VJ"
)

    db = mydb.cursor(buffered=True)
    plt = request.form.get("plt")
    new = request.form.get("new")
    conv_conf = request.form.get("conv_conf")
    ord_conf = request.form.get("ord_conf")
    key_ord = request.form.get("key_ord")
    key_conv = request.form.get("key_conv")
    key_add = request.form.get("key_add")

    table_data = db.execute("SELECT trp_name, plt FROM trp")
    table_data = db.fetchall()
    switch = "None"
    


    if ord_conf == "yes":
        if conv_conf == "yes" or key_conv != "" or key_add != "":
            message = "Select one action only"
            return render_template("error.html", message=message)


        if key_ord != "OPFOR2023":
            message = "Incorrect key"
            return render_template("error.html", message=message)

        switch = "ord"

    
    if key_add != "":
        if key_add == "OPFOR2023":
            if ord_conf == "yes" or conv_conf == "yes" or key_conv != "" or key_ord != "":
                message = "Select one action only"
                return render_template("error.html", message=message)

            if plt == "":
                message = "Select Platoon"
                return render_template("error.html", message=message)

            switch = "add"

        else:
            message = "Incorrect Key"
            return render_template("error.html", message=message)
            
    elif key_add=='' and ord_conf !="yes" and conv_conf != "yes" :
        if plt=="":
            message= "please enter platoon and key"
        else:
            message = "Please enter Key"
        return render_template("error.html", message=message)
    else:
        pass
        
     
    if conv_conf == "yes":
        if ord_conf == "yes" or key_ord != "" or key_add != "":
            message = "Select one action only"
            return render_template("error.html", message=message)

        if key_conv != "OPFOR2023":
            message = "Incorrect Key"
            return render_template("error.html", message=message)

        if new == "":
            message = "Select new platoon"
            return render_template("error.html", message=message)

        switch = "conv"
        
        
    if conv_conf == "" and ord_conf == "" and key_add == "":
        message = "Enter Key"
        return render_template("error.html", message=message)


    for x in range(35):
        x += 1
        id = "name" + str(x)
        name = request.form.get(id)

        for x in table_data:
            if name == x[0]:
                if switch == "add":
                    message = "Name already exists"
                    return render_template("error.html", message=message)


            if name == [] or name == "":
                switch = "No"


        if switch == "add":
            db.execute("INSERT INTO trp (trp_name, plt) VALUES (%s, %s)", (name, plt))

        elif switch == "conv":
            db.execute("UPDATE trp SET plt = %s WHERE trp_name = %s", (new, name))

        elif switch == "ord":
            db.execute("DELETE FROM data WHERE data_id = (SELECT id FROM trp WHERE trp_name = %s)", (name,))
            db.execute("DELETE FROM trp WHERE trp_name = %s", (name,))

        else:
            break

        print(switch)

    mydb.commit()
    return redirect("https://op4-bibo.com", code=302)

mydb.commit()








if __name__ == '__main__':
    app.run(debug=True)
