import sqlite3
from datetime import datetime
from req import get_views_from_Id

def create_table():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE projects (
        userId TEXT,
        project_url TEXT,
        project_id TEXT,
        date_added DATETIME,
        date_updated DATETIME,
        views INTEGER
    )
''')
    
    conn.commit()
    c.close()
    conn.close()
    
def add_one(userId, project_url, project_id, date_added, date_updated, views):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
        
    c.execute('''INSERT INTO projects 
              VALUES (?,?,?,?,?,?)''', (userId, project_url, project_id, date_added, date_updated, views))

    conn.commit()
    
    c.close()
    conn.close()

def search(attr, value, operation):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()

    # print(f"SELECT * from projects WHERE {attr} {operation} {value}")
    c.execute(f"SELECT * from projects WHERE {attr} {operation} {value}")
    items = c.fetchall()
        
    conn.commit()
    conn.close()
    return items

def search_with_userId(attr, value, operation, userId):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()

    # print(f"SELECT * from projects WHERE {attr} {operation} '{value}' AND userId = {userId}")
    c.execute(f"SELECT * from projects WHERE {attr} {operation} '{value}' AND userId = {userId}")
    items = c.fetchall()
        
    conn.commit()
    conn.close()
    return items
    
def show_all():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    # print("SELECT * from projects")
    c.execute("SELECT * from projects")
    items = c.fetchall()
        
    conn.commit()
    conn.close()
    return items

def delete_record(attr, value, operation, userId):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()

    # print(f"DELETE from projects WHERE {attr} {operation} '{value}' AND userId = {userId}")
    c.execute(f"DELETE from projects WHERE {attr} {operation} '{value}' AND userId = {userId}")

    conn.commit()
    c.close()
    conn.close()
    
def update(new_views, project_id, userId):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    
    # print(f'UPDATE projects SET views = {new_views}, date_updated = "{datetime.now()}" WHERE project_id = "{project_id}" AND userId = "{userId}"')
    c.execute(f'UPDATE projects SET views = {new_views}, date_updated = "{datetime.now()}" WHERE project_id = "{project_id}" AND userId = "{userId}"')
        
    conn.commit()

    c.close()
    conn.close()

def update_all():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    
    items = show_all()
    for item in items:
        new_views, status_code = get_views_from_Id(item[2])
        # print(f'UPDATE projects SET views = {new_views} , date_updated = "{datetime.now()}" WHERE project_id = "{item[2]}"')
        c.execute(f'UPDATE projects SET views = {new_views} , date_updated = "{datetime.now()}" WHERE project_id = "{item[2]}"')
    
    conn.commit()
    
    c.close()
    conn.close()
    return True

def clean_print(items):
    for item in items:
        # print(f'UserId: {item[0]} \nProject_url: {item[1]} \nProject_id: {item[2]} \ndate_added: {item[3]} \ndate_updated: {item[4]} \nview count: {item[5]}')
        print()