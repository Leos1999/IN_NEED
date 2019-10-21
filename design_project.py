import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download("stopwords")
# nltk.download('punkt')

from flask import Flask, render_template,request,redirect,url_for
from flask_mysqldb import MySQL
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

uname = 'man'

def Recommender(sentance):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentance)
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    Specialists = ['Addiction psychiatrist', 'Immunologist', 'Cardiologist', 'Dermatologist', 'Developmental pediatrician',
                   'Gastroenterologist', 'Gynecologist', 'Hematologist', 'Nephrologist', 'Neurologist',
                   'Oncologist', 'Ophthalmologist', 'Orthopedic surgeon', 'ENT', 'Pediatrician', 'Psychiatrist', 'Urologist']

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
                  13: ['ear', 'ears', 'nose', 'throat', 'balance', 'hearing', 'infection', 'dizziness'],
                  14: ['child', 'kid', 'baby', 'new', 'born', 'fever', 'cough'],
                  15: ['mental', 'depression', 'concentration', 'addiction', 'temper', 'anxiety', 'disorder', 'illogical', 'thoughts', 'memory'],
                  16: ['urine', 'infection', 'urinating', 'pelvic', 'pain', 'fertility', 'men', 'erectile']
                  }
    Recom_list = [0] * 17
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

@app.route("/login")
def login():
    return render_template("login.html")

d={}
d1={}
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
        result = Recommender(string)
        print(string)
        #d['result'] = result
        stmt = "SELECT * FROM DOCTOR WHERE DEPT='"+result+"'"
        cur.execute(stmt)
        myresult = cur.fetchall()
        mysql.connection.commit()
        print(myresult)
        n=1
        cur.close()
        for i in myresult:
            m = "d"+str(n)
            d1['name'] = i[1]
            d1['dept'] = i[2]
            d1['sh'] = i[4]
            d[m] = d1
            n+=1
        print(d)
    return render_template("appointment.html",d=d)

@app.route("/recommend",methods=['GET','POST'])
def recommend():
    #return 'success'
    return render_template("recommend.html")

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

    
if __name__ == "__main__":
    app.run(debug=True)