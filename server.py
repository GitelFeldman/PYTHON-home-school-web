import datetime
import smtplib
from flask import Flask, render_template, request, redirect, url_for
from models import schooluder_model, fun_tasks_model, upload_task_model, upload_fun_task_model, login_model, task_model, \
    people_model
from generate_charts import *


app = Flask(__name__, static_url_path='', static_folder='static', template_folder='template')

username = "Shira Levi"


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/index.html', methods=['POST', 'GET'])
def home():
    error = None
    print(request.method) 
    if request.method == 'POST':
        global username
        username = request.form['username']
        if login_model.is_student(username):
            return redirect(url_for('schedule'))  # ה-redirect עובד?
        elif login_model.is_teacher(username):
            return redirect(url_for('teacher_post_task'))  # ה-redirect עובד?
        else:
            return redirect(url_for('error_login'))  # אם לא נמצא משתמש
    return render_template('index.html', error=error)


@app.route('/error_login.html')
def error_login():
    return render_template('error_login.html')


@app.route('/schedule.html')
def schedule():
    student_name = username
    student_class = schooluder_model.get_class_by_student(student_name)
    data = schooluder_model.get_week_schedule_by_class(student_class)
    day = datetime.datetime.today().weekday()
    hour = datetime.datetime.now().hour
    date = datetime.datetime.today().strftime('%A - %B %d:')
    return render_template('schedule.html', week_schedule=data, day=day + 1, hour=hour, date=date,
                           student_class=student_class)


@app.route('/fun_task.html')
def about_fun_tasks():
    student_name = username
    student_class = schooluder_model.get_class_by_student(student_name)
    fun_tasks = fun_tasks_model.get_fun_tasks_by_grade(student_class)
    print(fun_tasks)
    fun_tasks_1 = fun_tasks[0:int(len(fun_tasks) / 2)]
    fun_tasks_2 = fun_tasks[int(len(fun_tasks) / 2):len(fun_tasks)]
    return render_template('fun_task.html', student_class=student_class, fun_tasks=fun_tasks, fun_tasks_1=fun_tasks_1,
                           fun_tasks_2=fun_tasks_2)


def send_email(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    print(f"FROM: {FROM}, TO: {TO}, SUBJECT: {SUBJECT}, BODY: {TEXT}")

    message = f"From: {FROM}\nTo: {', '.join(TO)}\nSubject: {SUBJECT}\n\n{TEXT}"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()  # נוסף קריאה נוספת ל-ehlו
        server.login(user, pwd)  # ודא שסיסמת אפליקציה כאן
        server.sendmail(FROM, TO, message)
        server.quit()
        print('successfully sent the mail')
    except Exception as e:
        print(f"Error: {e}")
        print("failed to send mail")



@app.route('/contacts.html', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        teacher_name = request.form['teacher_name']
        subject = request.form['subject']
        msg = request.form['msg']
        student_mail = request.form['student_mail']
        password = request.form['password']
        teacher_email = people_model.get_teacher_email_by_name(teacher_name)
        send_email(student_mail, password, teacher_email, subject, msg)
        return redirect(url_for('schedule'))
    return render_template('contacts.html')


@app.route('/tasks.html')
def tasks():
    global username
    print(username)
    tasks = task_model.get_student_tasks_by_name(username)
    print(tasks)
    return render_template('tasks.html', tasks=tasks)


@app.route('/check')
def check():
    global username
    is_done = request.args.get("done")
    task_id = request.args.get("task_id")
    if is_done == 'on':  # mean false
        task_model.update_student_task_is_done(task_id, 0, username)
    else:  # mean true
        task_model.update_student_task_is_done(task_id, 1, username)
    return tasks()


@app.route('/teacher_task.html', methods=['GET', 'POST'])
def teacher_post_task():
    error = None
    if request.method == 'POST':
        grade = request.form['grade']
        date = request.form['date']
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        day = (date.weekday() + 1) % 7 + 1
        print("day and date")
        print(day)
        print(date)
        hour = request.form['hour']
        subject = request.form['subject']
        descr = request.form['descr']
        upload_task_model.insert_task(grade, day, hour, date, descr)
        return redirect(url_for('teacher_post_task'))
    return render_template('teacher_task.html', error=error)


@app.route('/teacher_fun_task.html', methods=['GET', 'POST'])
def teacher_post_fun_task():
    error = None
    if request.method == 'POST':
        grade = request.form['grade']
        descr = request.form['descr']
        link = request.form['link']
        upload_fun_task_model.insert_fun_task(grade, descr, link)
        return redirect(url_for('teacher_post_fun_task'))
    return render_template('teacher_fun_task.html', error=error)


@app.route('/teacher_schedule.html', methods=['GET', 'POST'])
def teacher_post_lesson():
    error = None
    if request.method == 'POST':
        grade = request.form['grade']
        day = request.form['day']
        hour = request.form['hour']
        subject = request.form['subject']
        zoom_link = request.form['zoom_link']
        schooluder_model.insert_lesson_to_schedule(grade, day, hour, subject, zoom_link)
        return redirect(url_for('teacher_post_lesson'))
    return render_template('teacher_schedule.html', error=error)

@app.route('/charts')
def charts():
    # יצירת הגרפים
    create_task_count_chart()
    create_weekly_hours_chart()
    task_chart_url = url_for('static', filename='charts/task_count_chart.png')
    hours_chart_url = url_for('static', filename='charts/weekly_hours_chart.png')
    return render_template('charts.html', task_chart_url=task_chart_url, hours_chart_url=hours_chart_url)

if __name__ == '__main__':
    app.debug = True
    app.run(port=3000)