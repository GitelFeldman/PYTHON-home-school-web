from models.config import connection

def get_task_count_by_class():
    with connection.cursor() as cursor:
        query = "SELECT class, COUNT(*) AS task_count FROM task GROUP BY class;"
        cursor.execute(query)
        return cursor.fetchall()

def get_weekly_hours_by_class():
    with connection.cursor() as cursor:
        query = "SELECT class, COUNT(*) AS weekly_hours FROM week_schedule GROUP BY class;"
        cursor.execute(query)
        return cursor.fetchall()
