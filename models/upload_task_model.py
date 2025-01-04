from models.config import connection


def insert_task(grade, day, hour, date, descr):
    curr_id = get_current_task_id()
    print("grade")
    print(grade)
    print("day")
    print(day)
    print("hour")
    print(hour)
    print("date")
    print(date)
    print("descr")
    print(descr)
    with connection.cursor() as cursor:
        query = f"insert into task values ('{grade}', {day}, '{hour}', '{date}', '{descr}');"
        cursor.execute(query)
        connection.commit()
    insert_student_task(grade, curr_id)


def get_current_task_id():
    with connection.cursor() as cursor:
        query = "SELECT IDENT_CURRENT('task') AS current_id;"
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        return result[0][0]



def get_tasks_by_class_and_date(class_, date):
    with connection.cursor() as cursor:
        query = "select homework from lesson where class = '{}' and date = {}".format(class_, date)
        cursor.execute(query)
        tasks = cursor.fetchall()
        return tasks


def get_all_students(class_):
    with connection.cursor() as cursor:
        query = f"select name_ from student where class = '{class_}'"
        cursor.execute(query)
        students = cursor.fetchall()
        return students


def insert_student_task(class_, task_id):
    students = get_all_students(class_)
    with connection.cursor() as cursor:
        for student in students:
            print("studenttttttt")
            print (student)
            query = f"insert into student_task values('{student[0]}', {task_id}, 0)"
            cursor.execute(query)
            connection.commit()
    print("insert students")
