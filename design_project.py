import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import random

nltk.download("stopwords")
nltk.download('punkt')

from flask import Flask,flash, render_template,request,redirect,url_for
from flask_mysqldb import MySQL,MySQLdb
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'csmace2017@gmail.com',
	MAIL_PASSWORD = 'macollege'
	)
mail = Mail(app)

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'rj1xkuSpuK'
app.config['MYSQL_PASSWORD'] = 'Zo7Na1yOXi'
app.config['MYSQL_DB'] = 'rj1xkuSpuK'

#git add .
#git commit -m "db resolved"
#git push heroku master
#heroku logs -n 1500
#\connect rj1xkuSpuK@remotemysql.com:3306

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
                   'Oncologist', 'Ophthalmologist', 'Orthopedic surgeon', 'ENT', 'Pediatrician', 'Psychiatrist', 'Urologist','Dentist','Physician']

    Collection = {0: ['addiction', 'alcohol', 'drugs', 'concentration'],
                  1: ['allergy', 'immunity', 'pollen', 'sneezing', 'itchy', 'rash', 'swollen'],
                  2: ['heart', 'blood', 'pain', 'beat', 'chest', 'dizzy', 'dizziness', 'faint', 'cholesterol'],
                  3: ['skin', 'hair', 'nail', 'acne'],
                  4: ['autism', 'inactive', 'child', 'kid', 'baby', 'disabilities', 'mental', 'communication', 'response', 'delay', 'attention'],
                  5: ['heartburn', 'digestion', 'stomach', 'pain', 'cramps'],
                  6: ['pregnancy', 'birth', 'fertility', 'women', 'menstruation', 'disorders'],
                  7: ['blood', 'clotting', 'blood-clotting', 'anemia', 'weakness', 'weight', 'infection', 'bruising', 'excessive', 'bleeding', 'energy'],
                  8: ['pressure', 'high', 'blood', 'diabetes', 'kidney', 'urine', 'back', 'smelly', 'appetite', 'skin', 'yellow', 'weight'],
                  9: ['headache', 'chronic', 'pain', 'dizziness', 'movement', 'problems', 'weakness', 'loss', 'consciousness', 'memory', 'confusion', 'sleep','sleeping','confusing'],
                  10: ['cancer'],
                  11: ['eye', 'vision', 'eyes', 'see', 'pain'],
                  12: ['shoulder', 'pain', 'bone', 'twisted', 'angles', 'joints', 'numb', 'hands', 'swollen', 'bend', 'wrist', 'neck', 'broken', 'painful', 'stiff', 'muscles','leg','back','hand','joint'],
                  13: ['ear', 'ears', 'nose', 'throat', 'balance', 'hearing', 'infection', 'dizziness','bleeding'],
                  14: ['child', 'kid', 'baby', 'new', 'born', 'fever', 'cough'],
                  15: ['mental', 'depression', 'concentration', 'addiction', 'temper', 'anxiety', 'disorder', 'illogical', 'thoughts', 'memory'],
                  16: ['urine', 'infection', 'urinating', 'pelvic', 'pain', 'fertility', 'men', 'erectile'],
                  17: ['teeth','toothache'],
                  18: ['head','headache','leg','injury','hand','pain','throat','eye','fever','body','vomiting','gas','problems']
                  }
    Recom_list = [0] * 19
    for i in filtered_sentence:
        for k, v in Collection.items():
            if i in v:
                Recom_list[k] += 1
    print('Please consult :', Specialists[Recom_list.index(max(Recom_list))])
    if max(Recom_list)>1:
        return Specialists[Recom_list.index(max(Recom_list))]
    else:
        return Specialists[18]

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
h_data = {}
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
        hos=()
        for i in myresult:
            y={}
            m = "d"+str(n)
            y['name'] = i[1]
            y['dept'] = i[2]
            y['host'] = i[3]
            y['sh'] = i[4]
            y['rating']=i[5]
            y['q'] = i[6]
            l=list(hos)
            l.append(str(i[3]))
            hos = tuple(l)
            print(y)
            d[m] = y
            print(d)
            n+=1
        print(hos)
        stmt = "SELECT * FROM HOSPITAL WHERE NAME IN "+str(hos)
        cur.execute(stmt)
        out = cur.fetchall()
        mysql.connection.commit()
        print(out)
        k=1
        for i in out:
            z={}
            j = "h"+str(k)
            z['name']=i[0]
            z['address']=i[1]
            z['phone']=i[2]
            z['rating']=i[3]
            h_data[j] = z
            k+=1
        print(h_data)
        global data
        data = {'name':name,'a_date':a_date}
        cur.close()
    return render_template("appointment.html",d=d,data=data,h_data=h_data)
d={}
h_data={}

@app.route("/booked",methods=['POST'])
def booked():
    if request.method == 'POST':
        names = request.get_json()
        print(names)
        user = 'unknown'
        name = names['names']['p_name']
        a_date = names['names']['a_date']
        d_name = names['names']['name']
        host = names['names']['host']
        dept = names['names']['dept']
        l = ['9:45am','10:00am','10:30am','10:45am','10:15am','11:00am','11:15am','11:30am','11:45am','12:00pm','12:15am','12:30am','1:30am','1:45am','2:00am','2:15am','2:30am','2:45am','3:00am',]
        alphabets = ['a','b','q','w','e','r','t','y','u','i','o','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9','0']
        code_list = random.sample(alphabets,10)
        code=''
        for i in code_list:
            code = code[:]+str(i)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO BOOKED(USERNAME,NAME,A_DATE,D_NAME,HOST,DEPT) VALUES ( %s, %s, %s, %s, %s, %s)", (user,name,a_date,d_name,host,dept))
        mysql.connection.commit()
        cur.execute("SELECT MAIL FROM APPOINTMENT WHERE NAME='"+str(name)+"' AND A_DATE='"+a_date+"'")
        myresult = cur.fetchall()
        print(myresult)
        smail = myresult[0][0]
        print(smail)
        cur.execute("SELECT LOGID FROM BOOKED WHERE NAME='"+str(name)+"' AND D_NAME='"+str(d_name)+"'")
        myresult = cur.fetchall()
        logid = 89465700 + int(myresult[0][0])
        cur.execute("SELECT ADDRESS FROM HOSPITAL WHERE NAME='"+str(host)+"'")
        myresult = cur.fetchall()
        addr = myresult[0][0]
        try:
            print("HI")
            msg = Message("Appointment Confirmation",
            sender="csmace2017@gmail.com",
            recipients=[smail])
            msg.body = "Hi "+name+",\n\tThis is about the information on your doctor appointment, below attached are the details, \nLog Id: "+str(logid)+"\nHospital: "+host+"\nAddress: "+addr+"\nAppointment Date: "+a_date+"\nAppointment Time:"+l[random.randint(0,len(l)-1)]+"\nDoctor: "+d_name+"\n\nSECURITY CODE: "+code+"\nDont share your security code to anyone!!!, This is used as verification for your appointment.\n\n Thanks & Regards,\n Team IN-NEED"
            mail.send(msg)
            return 'Mail sent!'
        except Exception as e:
            print(e)
            return(str(e)) 
        cur.close()
    return redirect(url_for('home'))
    #return render_template("booked.html")
err=None
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
        stmt = "SELECT * FROM USERS WHERE USERNAME='"+str(username)+"' OR EMAIL='"+str(mail)+"'"
        cur.execute(stmt)
        myresult = cur.fetchall()
        global err
        err = None
        if myresult:
            err = "User Already Exists!!!!"
            cur.close()
            return redirect(url_for('signup'))
        else:
            cur.execute("INSERT INTO USERS(USERNAME,FNAME,LNAME,DOB,EMAIL,PHONE,PASSWORD,GENDER,ADDRESS,DISTRICT,TOWN) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username,firstName, lastName,dob,mail,phone,password,gender,address,district,town))
            mysql.connection.commit()
            cur.close()
            global uname
            uname = username
            return redirect(url_for('logged'))
        cur.close()
        # global uname
        # uname = username
    return render_template("signup.html",err=err)

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
message = None
@app.route("/logged",methods=['GET','POST'])
def logged():
    global uname
    if request.method == 'POST':
        name = request.get_json()
        print(name)
        uname = name['Username']
        print(uname)
    return render_template("logged.html",uname=uname,message=message)

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
        print(uname)
        print(myresult)
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
        hos=()
        for i in myresult:
            y={}
            m = "d"+str(n)
            y['name'] = i[1]
            y['host'] = i[3]
            y['dept'] = i[2]
            y['sh'] = i[4]
            y['rating']=i[5]
            y['q']=i[6]
            l=list(hos)
            l.append(str(i[3]))
            hos = tuple(l)
            print(y)
            d[m] = y
            n+=1
            print(d)
        print(hos)
        stmt = "SELECT * FROM HOSPITAL WHERE NAME IN "+str(hos)
        cur.execute(stmt)
        out = cur.fetchall()
        mysql.connection.commit()
        print(out)
        k=1
        for i in out:
            z={}
            j = "h"+str(k)
            z['name']=i[0]
            z['address']=i[1]
            z['phone']=i[2]
            z['rating']=i[3]      
            h_data[j] = z
            k+=1
        print(h_data)
        print(d)
        global data
        data = {'name':name,'a_date':a_date}
        cur.close()
    return render_template("logged_appointment.html",d=d,data=data,h_data=h_data,uname=uname)

@app.route("/logged_booked",methods=['GET','POST'])
def logged_booked():
    if request.method == 'POST':
        names = request.get_json()
        print(names)
        #global uname
        #user = uname
        name = names['names']['p_name']
        a_date = names['names']['a_date']
        d_name = names['names']['name']
        host = names['names']['host']
        dept = names['names']['dept']
        user = names['names']['uname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO BOOKED(USERNAME,NAME,A_DATE,D_NAME,HOST,DEPT) VALUES ( %s, %s, %s, %s, %s, %s)", (user,name,a_date,d_name,host,dept))
        mysql.connection.commit()
        cur.execute("SELECT MAIL FROM APPOINTMENT WHERE NAME='"+str(name)+"' AND A_DATE='"+a_date+"'")
        myresult = cur.fetchall()
        print(myresult)
        smail = myresult[0][0]
        print(smail)
        cur.execute("SELECT LOGID FROM BOOKED WHERE NAME='"+str(name)+"' AND D_NAME='"+str(d_name)+"'")
        myresult = cur.fetchall()
        logid = 89465700 + int(myresult[0][0])
        l = ['9:45am','10:00am','10:30am','10:45am','10:15am','11:00am','11:15am','11:30am','11:45am','12:00pm','12:15am','12:30am','1:30am','1:45am','2:00am','2:15am','2:30am','2:45am','3:00am',]
        alphabets = ['a','b','q','w','e','r','t','y','u','i','o','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9','0']
        code_list = random.sample(alphabets,10)
        code=''
        for i in code_list:
            code = code[:]+str(i)
        cur.execute("SELECT ADDRESS FROM HOSPITAL WHERE NAME='"+str(host)+"'")
        myresult = cur.fetchall()
        addr = myresult[0][0]
        try:
            print("HI")
            msg = Message("Appointment Confirmation",
            sender="csmace2017@gmail.com",
            recipients=[smail])
            msg.body = "Hi "+name+",\n\tThis is about the information on your doctor appointment, below attached are the details, \nLog Id: "+str(logid)+"\nHospital: "+host+"\nAddress: "+addr+"\nAppointment Date: "+a_date+"\nAppointment Time:"+l[random.randint(0,len(l)-1)]+"\nDoctor: "+d_name+"\n\nSECURITY CODE: "+code+"\nDont share your security code to anyone!!!, This is used as verification for your appointment.\n\n Thanks & Regards,\n Team IN-NEED"
            mail.send(msg)
            return 'Mail sent!'
        except Exception as e:
            print(e)
            return(str(e)) 
        cur.close()
    global message
    message="Your Booking has been registered!!!"
    return redirect(url_for('logged'))
    #return render_template("booked.html")

pdata = {}
p_data={}
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
    stmt = "SELECT * FROM BOOKED WHERE USERNAME='"+uname+"'"
    cur.execute(stmt)
    myresult = cur.fetchall()
    mysql.connection.commit()
    l = ['9:45am','10:00am','10:30am','10:45am','10:15am','11:00am','11:15am','11:30am','11:45am','12:00pm','12:15am','12:30am','1:30am','1:45am','2:00am','2:15am','2:30am','2:45am','3:00am',]
    j=1
    for i in myresult:
        pd={}
        k = "pd"+str(j)
        pd['name'] = i[1]
        pd['a_date'] = i[2]
        pd['d_name'] = i[3]
        pd['host'] = i[4]
        pd['dept'] = i[5]
        pd['logid'] = 89465700+i[6]
        pd['time'] = l[random.randint(0,len(l)-1)]
        print(i[4])
        stmt = 'SELECT ADDRESS FROM HOSPITAL WHERE NAME="'+str(i[4])+'"'
        print(stmt)
        cur.execute(stmt)
        myresult = cur.fetchall()
        if myresult:
            pd['h_address'] = myresult[0][0]
        p_data[k]=pd
        j+=1
    cur.close()
    print(pdata)
    uname=pdata['uname']
    return render_template("profile.html",pdata=pdata,p_data=p_data,uname=uname)

@app.route("/blog")
def blog():
    return render_template("blog-single.html")

if __name__ == "__main__":
    app.run(debug=True)