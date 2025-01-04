from models.config import connection
from datetime import date, timedelta


def get_student_tasks_by_name(name):
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    
    with connection.cursor() as cursor:
        query = """
            SELECT 
                id, 
                homework, 
                CAST(date_ AS DATE) AS date_ 
            FROM 
                task 
            JOIN 
                student_task 
            ON 
                student_task.task_id = task.id 
            WHERE 
                student_task.name_ = ? 
                
                AND student_task.is_done = 0 
            ORDER BY 
                date_ DESC
        """
        cursor.execute(query, [name])  # השתמש בפרמטרים כדי למנוע SQL Injection
        tasks = cursor.fetchall()
        print("tasks")
        print(tasks)
        # שינוי התאריכים "היום" ו"אתמול" לטקסט מתאים
        updated_tasks = []
        for task in tasks:
            # יצירת דיקשנרי עם מפתחות מותאמים
            task_dict = {
                'id': task[0],
                'homework': task[1],
                'date_': task[2]
            }
            print("all tasks")
            print(task_dict)
            if task_dict['date_'] == today:
                task_dict['date_'] = 'today'
            elif task_dict['date_'] == yesterday:
                task_dict['date_'] = 'yesterday'
            updated_tasks.append(task_dict)
        return updated_tasks

# change name to get from cookie
def update_student_task_is_done(task_id, is_done, username):
    with connection.cursor() as cursor:
        query = "update student_task " \
                "set student_task.is_done = {} " \
                "where student_task.task_id = {} and student_task.name_ = '{}' ".format(is_done, task_id,username)
        cursor.execute(query)
        connection.commit()