import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords")
nltk.download('punkt')

from flask import Flask,flash, render_template,request,redirect,url_for
from flask_mysqldb import MySQL,MySQLdb
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12309268'
app.config['MYSQL_PASSWORD'] = 'gVV6qlKy6c'
app.config['MYSQL_DB'] = 'sql12309268'

#git add .
#git commit -m "db resolved"
#git push heroku master
#heroku logs -n 1500
#\connect sql12309268@sql12.freemysqlhosting.net

mysql = MySQL(app)

uname = 'user'

def Recommender(sentance):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentance)
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    Specialists = ['Addiction psychiatrist', 'Immunologist', 'Cardiologist', 'Dermatologist', 'Developmental pediatrician',
                   'Gastroenterologist', 'Gynecologist', 'Hematologist', 'Nephrologist', 'Neurologist',
                   'Oncologist', 'Ophthalmologist', 'Orthopedic surgeon', 'ENT', 'Pediatrician', 'Psychiatrist', 'Urologist','Dentist']

    Collection = {0: ['addiction', 'alcohol', 'drugs', 'concentration'],
                  1: ['allergy', 'immunity', 'pollen', 'sneezing', 'itchy', 'rash', 'swollen'],
                  2: ['heart', 'blood', 'pain', 'beat', 'chest', 'dizzy', 'dizziness', 'faint', 'cholesterol'],
                  3: ['skin', 'hair', 'nail', 'acne'],
                  4: ['autism', 'inactive', 'child', 'kid', 'baby', 'disabilities', 'mental', 'communication', 'response', 'delay', 'attention'],
                  5: ['heartburn', 'digestion', 'stomach', 'pain', 'cramps'],
                  6: ['pregnancy', 'birth', 'fertility', 'women', 'menstruation', 'disorders'],
                  7: ['blood', 'clotting', 'blood-clotting', 'anemia', 'weakness', 'weight', 'infection', 'bruising', 'excessive', 'bleeding', 'energy'],
                  8: ['pressure', 'high', 'blood', 'diabetes', 'kidney', 'urine', 'back', 'smelly', 'appetite', 'skin', 'yellow', 'weight'],
                  9: ['headache', 'chronic', 'pain', 'dizziness', 'movement', 'problems', 'weakness', 'loss', 'consciousness', 'memory', 'confusion', 'sleep'],
                  10: ['cancer'],
                  11: ['eye', 'vision', 'eyes', 'see', 'pain'],
                  12: ['shoulder', 'pain', 'bone', 'twisted', 'angles', 'joints', 'numb', 'hands', 'swollen', 'bend', 'wrist', 'neck', 'broken', 'painful', 'stiff', 'muscles','leg','back','hand','joint'],
                  13: ['ear', 'ears', 'nose', 'throat', 'balance', 'hearing', 'infection', 'dizziness','bleeding'],
                  14: ['child', 'kid', 'baby', 'new', 'born', 'fever', 'cough'],
                  15: ['mental', 'depression', 'concentration', 'addiction', 'temper', 'anxiety', 'disorder', 'illogical', 'thoughts', 'memory'],
                  16: ['urine', 'infection', 'urinating', 'pelvic', 'pain', 'fertility', 'men', 'erectile'],
                  17: ['teeth']
                  }
    Recom_list = [0] * 18
    for i in filtered_sentence:
        for k, v in Collection.items():
            if i in v:
                Recom_list[k] += 1
    print('Please consult :', Specialists[Recom_list.index(max(Recom_list))])
    return Specialists[Recom_list.index(max(Recom_list))]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")

d={}
data = {}
@app.route("/appointment",methods=['GET','POST'])
def appointment():
    if request.method == "POST":
        details = request.form
        name = details['name']
        phone = details['phone']
        mail = details['email']
        dob = details['dop']
        a_date = details['adate']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO APPOINTMENT(NAME,PHONE,MAIL,DOB,A_DATE) VALUES ( %s, %s, %s, %s, %s)", (name,phone,mail,dob,a_date))
        string = details['description']
        string = string.lower()
        result = Recommender(string)
        print(string)
        print(result)
        stmt = "SELECT * FROM DOCTOR WHERE DEPT='"+str(result)+"'"
        cur.execute(stmt)
        myresult = cur.fetchall()
        mysql.connection.commit()
        print(myresult)
        n=1
        cur.close()
        for i in myresult:
            y={}
            m = "d"+str(n)
            y['name'] = i[1]
            y['dept'] = i[2]
            y['sh'] = i[4]
            print(y)
            d[m] = y
            n+=1
            print(d)
        print(d)
        global data
        data = {'name':name,'a_date':a_date}
    return render_template("appointment.html",d=d,data=data)

@app.route("/booked",methods=['GET','POST'])
def booked():
    values = request.get_json()
    print(values)
    name = values['name']
    a_date = values['a_date']
    d_name = values['d_name']
    host = values['host']
    dept = values['dept']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO BOOKED(NAME,A_DATE,D_NAME,HOST,DEPT) VALUES ( %s, %s, %s, %s, %s)", (name,a_date,d_name,host,dept))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == "POST":
        details = request.form
        username = details['uname']
        firstName = details['fname']
        lastName = details['lname']
        dob = details['dob']
        mail = details['mail']
        phone = details['phone']
        password = details['password']
        gender = details['gender']
        address = details['address']
        district = details['district']
        town = details['town']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO USERS(USERNAME,FNAME,LNAME,DOB,EMAIL,PHONE,PASSWORD,GENDER,ADDRESS,DISTRICT,TOWN) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username,firstName, lastName,dob,mail,phone,password,gender,address,district,town))
        mysql.connection.commit()
        cur.close()
        global uname
        uname = username
        return redirect(url_for('logged'))
    return render_template("signup.html")

@app.route("/logged",methods=['GET','POST'])
def logged():
    return render_template("logged.html",uname=uname)

@app.route("/logged_appointment",methods=['GET','POST'])
def logged_appointment():
    if request.method == "POST":
        global uname
        cur = mysql.connection.cursor()
        stmt = "SELECT * FROM USERS WHERE USERNAME='"+uname+"'"
        cur.execute(stmt)
        myresult = cur.fetchall()
        mysql.connection.commit()
        details = request.form
        name = details['name']
        phone = myresult[0][6]
        mail = myresult[0][5]
        dob = myresult[0][4]
        a_date = details['adate']
        # cur = mysql.connection.cursor()
        cur.execute("INSERT INTO APPOINTMENT(NAME,PHONE,MAIL,DOB,A_DATE) VALUES ( %s, %s, %s, %s, %s)", (name,phone,mail,dob,a_date))
        string = details['description']
        string = string.lower()
        result = Recommender(string)
        print(string)
        print(result)
        stmt = "SELECT * FROM DOCTOR WHERE DEPT='"+str(result)+"'"
        cur.execute(stmt)
        myresult = cur.fetchall()
        mysql.connection.commit()
        print(myresult)
        n=1
        cur.close()
        for i in myresult:
            y={}
            m = "d"+str(n)
            y['name'] = i[1]
            y['dept'] = i[2]
            y['sh'] = i[4]
            print(y)
            d[m] = y
            n+=1
            print(d)
        print(d)
        global data
        data = {'name':name,'a_date':a_date}
    return render_template("logged_appointment.html",d=d,data=data)


error=None
@app.route("/login",methods=['GET','POST'])
def login():
    myresult=()
    password='null'
    if request.method == 'POST':
        details = request.form
        global uname
        uname = details['uname']
        email = details['mail']
        password = details['password']
        cur = mysql.connection.cursor()
        try:
            stmt = "SELECT PASSWORD FROM USERS WHERE EMAIL='"+email+"'"
            cur.execute(stmt)
            myresult = cur.fetchall()
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            return None
        mysql.connection.commit()
        print(myresult)
        global error
        error = None
        if myresult:
            if password != myresult[0][0]:
                error = "Invalid Login Credentials!!!!"
            else:
                error = None
                return redirect(url_for('logged'))
        else:
            error = "Invalid Login Credentials!!!!"
    return render_template("login.html",error=error)

pdata = {}
pd = {}
@app.route("/profile",methods=['GET','POST'])
def profile():
    global uname
    cur = mysql.connection.cursor()
    stmt = "SELECT * FROM USERS WHERE USERNAME='"+uname+"'"
    cur.execute(stmt)
    myresult = cur.fetchall()
    mysql.connection.commit()
    for i in myresult:
        pdata['uname'] = i[1]
        pdata['fname'] = i[2]
        pdata['lname'] = i[3]
        pdata['dob'] = i[4]
        pdata['mail'] = i[5]
        pdata['phone'] = i[6]
        pdata['gender'] = i[8]
        pdata['address'] = i[9]
        pdata['district'] = i[10]
        pdata['town'] = i[11]
    stmt = "SELECT * FROM BOOKED WHERE NAME='"+uname+"'"
    cur.execute(stmt)
    myresult = cur.fetchall()
    mysql.connection.commit()
    j=1
    for i in myresult:
        k = "pd"+str(j)
        pd['name'] = i[0]
        pd['a_date'] = i[1]
        pd['d_name'] = i[2]
        pd['host'] = i[3]
        pd['dept'] = i[4]
        pdata[k]=pd
        j+=1
    cur.close()
    return render_template("profile.html",pdata=pdata)
    
if __name__ == "__main__":
    app.run(debug=True)