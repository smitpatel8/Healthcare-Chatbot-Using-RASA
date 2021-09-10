import mysql.connector as mysql

# connecting to the database using 'connect()' method
# it takes 3 required parameters 'host', 'user', 'passwd'


def userinfo(Name, Mobile_number, Email, Age, Gender, Reason, Time):
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="appointment"
    )

    cursor = db.cursor()
    sql = 'insert into user_details (Name, Mobile_number, Email, Age, Gender, Reason, Time) values ("{0}","{1}", "{2}", "{3}", "{4}", "{5}", "{6}");'.format(Name, Mobile_number, Email, Age, Gender, Reason, Time)
    cursor.execute(sql)
    db.commit()



def hospitals_near_me(city_name):
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="appointment"
    )

    name = str(city_name)


    cursor = db.cursor()
    sql = "select Hosp_name FROM hospital_location WHERE Region_name ='" + name + "';"
    cursor.execute(sql)

    value = cursor.fetchall()
    try:
        if len(value) != 0:
            return value
        else:
            return "Failed"
    except TypeError:
        return "Failed"

def new_Disease(disease_name):
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="appointment"
    )

    name = str(disease_name)
    # print(name)
    # print(type(name))

    cursor = db.cursor()
    sql = "select d_info FROM disease_info WHERE d_name ='" + name + "';"
    cursor.execute(sql)

    value = cursor.fetchone()
    try:
        if len(value) != 0:
            return value
        else:
            return "Failed"

    except TypeError:
        return "Failed"

def new_Symptom(symptom_name):
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="appointment"
    )

    name = str(symptom_name)
    # print(name)
    # print(type(name))

    cursor = db.cursor()
    sql = "select d_symptoms FROM disease_info WHERE d_name ='" + name + "';"
    cursor.execute(sql)

    value = cursor.fetchone()
    try:
        if len(value) != 0:
            return value
        else:
            return "Failed"

    except TypeError:
        return "Failed"