from flask import Flask, render_template, request, redirect
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",        
    password="",        
    database="coursedb" 
)
cursor = db.cursor(dictionary=True)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ajcademy0415@gmail.com' #Use the email id of your's   
app.config['MAIL_PASSWORD'] = 'yyoa pncu sylr ksnv'#use your own security password from Google.

mail = Mail(app)

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/register-page')
def register_page():
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    return render_template('register.html', courses=courses)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    course_id = request.form['course']

    cursor.execute("INSERT INTO student (name, email) VALUES (%s, %s)", (name, email))
    db.commit()
    student_id = cursor.lastrowid

    cursor.execute("INSERT INTO registration (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
    db.commit()

    cursor.execute("SELECT course_name FROM course WHERE course_id = %s", (course_id,))
    row = cursor.fetchone()
    course_name = row['course_name'] if row else "your course"

    subject = "Course Registration Successful"
    body = f"Hi {name},\n\nYou have successfully registered for {course_name}.\n\nThank you!\nAJcademy"

    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = body

    status = "Failed"
    try:
        mail.send(msg)
        status = "Sent"
        print(f"Confirmation Email sent to {email}")
    except Exception as e:
        status = f"Error: {str(e)}"
        print(" Error in sending Confirmation email:", e)

    cursor.execute(
        "INSERT INTO email_log (student_id, message, status) VALUES (%s, %s, %s)",
        (student_id, body, status)
    )
    db.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


