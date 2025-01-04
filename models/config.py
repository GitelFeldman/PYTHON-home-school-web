import pyodbc

# יצירת החיבור למסד הנתונים
try:
    connection = pyodbc.connect(r'Driver={ODBC Driver 18 for SQL Server};Server=localhost;Database=homeschooldb;Trusted_Connection=yes;TrustServerCertificate=yes;')
    print("Connection successful!")
except pyodbc.Error as ex:
    print("Connection failed:", ex)
    connection = None

if connection:
    queries = [
        """
    insert into student
    VALUES
    ('GitelFeldman','fourth','gitel.feldman@gmail.com','0533179500')"""
    ]
    print("connection is not None")
    # הרצת השאילתות
    try:
        cursor = connection.cursor()
        for query in queries:
            try:
                cursor.execute(query)
                print("Query executed successfully.")
            except pyodbc.Error as e:
                print(f"Error executing query: {e}")
        connection.commit()
        
    except Exception as e:
        print(f"General error: {e}")
    finally:
        # if 'cursor' in locals():
        #     cursor.close()
        # connection.close()
        print("Database setup completed.")
