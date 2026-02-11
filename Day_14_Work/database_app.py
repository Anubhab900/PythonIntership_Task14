import sqlite3
from tabulate import tabulate

def connectDB():
    return sqlite3.connect("users.db")

# 2. Create Table Programmatically
def createTables():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# 3. Insert User Records
def insertUser(name, email):
    conn = connectDB()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email) VALUES (?, ?)
        ''', (name, email))
        conn.commit()
        print("User inserted successfully.")
    except sqlite3.IntegrityError:
        print("Error: Email must be unique.")
    finally:
        conn.close()

# 4. Fetch Records (SELECT)
def fetchUsers():
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# 5. Update Records
def updateUser(user_id, name=None, email=None):
    conn = connectDB()
    cursor = conn.cursor()
    if name and email:
        cursor.execute('''
            UPDATE users SET name = ?, email = ? WHERE id = ?
        ''', (name, email, user_id))
    elif name:
        cursor.execute('''
            UPDATE users SET name = ? WHERE id = ?
        ''', (name, user_id))
    elif email:
        cursor.execute('''
            UPDATE users SET email = ? WHERE id = ?
        ''', (email, user_id))
    else:
        print("No fields to update.")
        return
    conn.commit()
    print("User updated successfully.")
    conn.close()

# 6. Delete Records
def deleteUser(user_id):
    conn = connectDB()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    print("User deleted successfully.")
    conn.close()

# 7. Display Results Neatly
def displayUsers(users):
    if users:
        print(tabulate(users, headers=["ID", "Name", "Email"], tablefmt="grid"))
    else:
        print("No users found.")

# 8. Main Execution
if __name__ == "__main__":
    createTables()
    
    # Insert some users
    insertUser("Alice", "alice@example.com")
    insertUser("Bob", "bob@example.com")
    insertUser("Charlie", "charlie@example.com")

    # Display all users
    users = fetchUsers()
    displayUsers(users)

    # Update a user
    updateUser(1, name="Alice Smith")

    # Display updated users
    users = fetchUsers()
    displayUsers(users)

    # Delete a user
    deleteUser(3)

    # Display final users list
    users = fetchUsers()
    displayUsers(users)
