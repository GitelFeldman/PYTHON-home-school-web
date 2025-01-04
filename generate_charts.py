import matplotlib.pyplot as plt
from models.charts_model import get_task_count_by_class, get_weekly_hours_by_class

def create_task_count_chart():
    data = get_task_count_by_class()
    print("Data for task count:", data)
    classes = [row[0] for row in data]
    task_counts = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.bar(classes, task_counts, color="skyblue")
    plt.title("Task Count by Class")
    plt.xlabel("Class")
    plt.ylabel("Number of Tasks")
    plt.grid(axis="y")
    
    try:
        plt.savefig("C:/Learning/python/project/home-school-web/static/charts/task_count_chart.png")
        print("Task count chart saved successfully.")
    except Exception as e:
        print(f"Error saving task count chart: {e}")
    
    plt.close()

def create_weekly_hours_chart():
    data = get_weekly_hours_by_class()
    print("Data for weekly hours:", data)
    classes = [row[0] for row in data]
    weekly_hours = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.bar(classes, weekly_hours, color="lightgreen")
    plt.title("Weekly Hours by Class")
    plt.xlabel("Class")
    plt.ylabel("Weekly Hours")
    plt.grid(axis="y")
    
    try:
        plt.savefig("C:/Learning/python/project/home-school-web/static/charts/weekly_hours_chart.png")
        print("Weekly hours chart saved successfully.")
    except Exception as e:
        print(f"Error saving weekly hours chart: {e}")
    
    plt.close()



