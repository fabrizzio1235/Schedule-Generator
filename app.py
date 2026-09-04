from flask import Flask, flash, redirect, render_template, request, jsonify
import pandas as pd
from db import init_db
import sqlite3
import itertools
import re #hour format


app = Flask(__name__)

def validateHour(hora_str):
    # check format
    pattern = r"^(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})$"
    match = re.match(pattern, hora_str.strip())
    if not match:
        return False  

    h1, m1, h2, m2 = map(int, match.groups())

    # cheack hour/minutes format
    if not (0 <= h1 <= 23 and 0 <= h2 <= 23 and 0 <= m1 <= 59 and 0 <= m2 <= 59):
        return False

    # Logical format begin starts before end
    if h1*60 + m1 >= h2*60 + m2:
        return False

    return True

def get_db_connection():#para usar la conexion como cursor y no usar cursor() (simplemente simplfica codigo)
    conn = sqlite3.connect('schedule.db')
    conn.row_factory = sqlite3.Row  # ← this allows to  access as a dict
    return conn

def AllSubjectCombinationS(subjects):
    subject_names = list(subjects.keys()) #convert into an array of subjects
    id_lists = [subjects[subj] for subj in subject_names] #convert the values in array as element of the id_lis array [[1,2], [3,4]...]

    all_combinations = list(itertools.product(*id_lists)) #all the combinations possible

    return list(all_combinations)

def toInt(string):
    if not string or string.strip() == "":
        return None, None #freeday
    b, e = string.split("-")  # ("0:50", "1:45")
    b = b.replace(":", "")      # "050"
    e = e.replace(":", "")      # "145"
    return int(b), int(e)

def valid(dayweek, begin, end):
    if(begin is None or end is None):
        return True
    valido = True
    for k in range(len(dayweek)):
        if dayweek[k][0]is None or dayweek[k][1] is None:  
            continue
        if((begin<=dayweek[k][0] and end <=dayweek[k][0]) or(begin>=dayweek[k][1] and end >=dayweek[k][1])):
            continue
        else:
            valido = False
            break
    return valido
    
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect ("/submit")
    else:
        return render_template("index.html") 
    
    
    

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == '':
            return "Error: No file selected", 400
        try:
            if file.filename.endswith('.csv'):
                
                df = pd.read_csv(file) # dataframe
                
            elif file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
                
                df = pd.read_excel(file)# dataframe
            else:
                return "Error: Invalid file format. Only CSV or Excel allowed.", 400
                
        except Exception as e:# if there's an error in the procces of reading the file, as e is a variable created at the moment
            
            return f"Error reading file: {str(e)}", 400
        
        # check the column that we request to the user
        if "Subject" not in df.columns:
            return "Error: Missing column 'Subject'", 400

        if "Teacher's name" not in df.columns:
            return "Error: Missing column 'Teacher's name'", 400
        
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            if day not in df.columns:
                return f"Error: Missing column '{day}'", 400
            
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            for idx, value in enumerate(df[day]):
                if pd.isna(value) or value.strip() == "" or value.strip() =="Asíncrona" or value.strip() == "Por definir":
                    continue
                if not validateHour(value):
                    return f"Error: Invalid time format or logic in row {idx+1}, column '{day}' -> '{value}'", 400
        
        conn = sqlite3.connect('schedule.db') #connect or create a db called schedule.db
        db = conn.cursor() # create a cursor to execute SQL
        
        #_ = 0, 1, 2, 3 , ...
        #row = is literally the row of each file of the dataframe, very similar to a dict
        #iterrows() returns two values index, and row
        db.execute("DELETE FROM schedule") 
        db.execute("DELETE FROM sqlite_sequence WHERE name='schedule'")
        for _, row in df.iterrows():
            
            if pd.isna(row['Subject']) or pd.isna(row["Teacher's name"]): #skip row wich have NaN = No value
                continue
            
            db.execute(''' INSERT INTO schedule (subject, teacher, monday, tuesday,wednesday,thursday, friday) VALUES (?,?,?,?,?,?,?)''',
            (row['Subject'],
            row["Teacher's name"],
            row['Monday'],
            row['Tuesday'],
            row['Wednesday'],
            row['Thursday'],
            row['Friday']))
        conn.commit() # save changes
        conn.close() # close connection
        
        return redirect("/filter")
    else:
        conn = sqlite3.connect('schedule.db')
        db = conn.cursor()
        db.execute("DELETE FROM schedule")
        db.execute("DELETE FROM sqlite_sequence WHERE name='schedule'")
        conn.commit()
        conn.close()
        return render_template("submit.html")



@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.method == "POST":
        
        
        selected = request.form.get("subject").split(",")
        

        db = get_db_connection()
        
        db.execute("DELETE FROM scheduleCopy1") #juts in case if there is data
        db.execute("DELETE FROM sqlite_sequence WHERE name='scheduleCopy1'")
        
        all_subjects = [row[0] for row in db.execute("SELECT DISTINCT subject FROM schedule").fetchall()]
        
        for subject in all_subjects:
            if subject in selected:
                db.execute('''
                        INSERT INTO scheduleCopy1 (subject, teacher, monday, tuesday, wednesday, thursday, friday)
                        SELECT subject, teacher, monday, tuesday, wednesday, thursday, friday
                        FROM schedule
                        WHERE subject = ?
                    ''', (subject,))            
        db.commit() 
        db.close() 
        
        return redirect("/generator")

    else:
        
        db = get_db_connection() # transform db to a dict
        db.execute("DELETE FROM scheduleCopy1") 
        db.execute("DELETE FROM sqlite_sequence WHERE name='scheduleCopy1'")
        table = db.execute("SELECT DISTINCT subject FROM schedule ORDER BY subject").fetchall()
        db.close()
        return render_template("filter.html", table=table)
    
@app.route("/generator",  methods=["GET", "POST"])
def generator():
    if request.method == "POST":
        db = get_db_connection() # transform db to a dict
        table = db.execute("SELECT * FROM scheduleCopy1 GROUP BY subject").fetchall()
        
        db.execute("DELETE FROM scheduleCopy2")   #just in case there is data
        db.execute("DELETE FROM sqlite_sequence WHERE name='scheduleCopy2'")
        
        #get in an array the teachers selected.
        teachers = []
        subjectSelected = []
        for subj_row in table:
            subject = subj_row["subject"]
            teacher = request.form.get(subject)

            # Si por alguna razón ese subject no viene del form, saltamos
            if not teacher:
                continue

            rows = db.execute(
                "SELECT * FROM scheduleCopy1 WHERE subject = ? AND teacher = ?",
                (subject, teacher)
            ).fetchall()  # Trae filas concretas

            for r in rows:
                teachers.append(r["id"])
                subjectSelected.append((subject, r["id"]))
        
        if teachers:
                
            placeholders = ",".join("?" * len(teachers))

            insert_query = f"""
                INSERT INTO scheduleCopy2 (id, subject, teacher, monday, tuesday, wednesday, thursday, friday)
                SELECT id, subject, teacher, monday, tuesday, wednesday, thursday, friday
                FROM scheduleCopy1
                WHERE id IN ({placeholders})
            """
            db.execute(insert_query, teachers)
            db.commit()
        subjects = {} #subjects will be after the for like this {Math: [2,45,23], History[...]...}
        for subject, id in subjectSelected:
            if subject not in subjects:
                subjects[subject] = [] 
            subjects[subject].append(id)
            
        #print(subjects)
        comb = AllSubjectCombinationS(subjects) 
        print(teachers)
        
        #VALID SHCEDULE
        schedules = []
        for i in comb:
            isvalid = True
            LU = []
            MA = []
            MI = []
            JU = []
            VI = []
            for j in range(len(i)):
                row = db.execute("SELECT * FROM scheduleCopy2 WHERE id = ?",( i[j],)).fetchone() #example comb = [(5, 113, 64, 229, 81), (97, 113, 64, 229, 81), (98, 113, 64, 229, 81), (99, 113, 64, 229, 81)]
                
                duration = row["monday"]
                begin, end = toInt(duration)
                if(valid(LU, begin, end)):
                    LU.append((begin, end))
                else:
                    isvalid = False
                    break
                duration = row["tuesday"]
                begin, end = toInt(duration)
                if(valid(MA, begin, end)):
                    MA.append((begin, end))
                else:
                    isvalid = False
                    break
                duration = row["wednesday"]
                begin, end = toInt(duration)
                if(valid(MI, begin, end)):
                    MI.append((begin, end))
                else:
                    isvalid = False
                    break
                duration = row["thursday"]
                begin, end = toInt(duration)
                if(valid(JU, begin, end)):
                    JU.append((begin, end))
                else:
                    isvalid = False
                    break
                duration = row["friday"]
                begin, end = toInt(duration)
                if(valid(VI, begin, end)):
                    VI.append((begin, end))
                else:
                    isvalid = False
                    break
            if(isvalid):
                schedules.append(i)
        print(schedules)
        #schedule all the valid schedules :)    
        rows = db.execute("SELECT * FROM scheduleCopy2")
        data = [dict(row) for row in rows]
        table = db.execute("SELECT * FROM scheduleCopy1 ORDER BY subject").fetchall() #for the next condition  in case that is not possible (combiintion)
        db.close()
        isPossible = True
        if(len(schedules) == 0):
            isPossible = False
            return render_template("generator.html", table=table,  schedules=[], data=[], isPossible=isPossible)
        return render_template("generator.html", schedules=schedules, data=data, isPossible=isPossible)
    else:
        db = get_db_connection() # transform db to a dict
        
        db.execute("DELETE FROM scheduleCopy2")   #just in case there is data
        db.execute("DELETE FROM sqlite_sequence WHERE name='scheduleCopy2'")
        table = db.execute("SELECT * FROM scheduleCopy1 ORDER BY subject").fetchall()
        db.close()
        return render_template("generator.html", table=table,  schedules=[], data=[])
        
if __name__ == "__main__":
    init_db() #the db.py function
    app.run(debug=True)
