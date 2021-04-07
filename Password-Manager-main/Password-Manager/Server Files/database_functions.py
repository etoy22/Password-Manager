import sqlite3
#using sqlite3
#Database functions for manipulating our tables for users and services(groupings)

def connect():
    """Create a connection to the sqlite database"""
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    return conn, cursor


def disconnect(conn):
    """Destroy the connection to the sqlite database"""
    conn.commit()
    conn.close()


def create_database():
    """Create the passwords ans users database if it doesn't exists"""
    conn, cursor = connect()

    cursor.execute('''
        CREATE TABLE "users" (
        "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "username" TEXT NOT NULL,
        "master_password" BLOB NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE "services" (
        "service_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "service_name" TEXT NOT NULL,
        "username" TEXT NOT NULL,
        "password" BLOB NOT NULL,
        "tag" BLOB NOT NULL,
        "cipher_key" BLOB NOT NULL,
        "mac_key" BLOB NOT NULL,
        "user_id" INT NOT NULL,
        CONSTRAINT fk_users
        FOREIGN KEY ("user_id")
        REFERENCES users(id)
        );
    ''')

    cursor.execute('''
                  CREATE TABLE "sending" (
                    "sending_id" INTEGER NOT NULL,
                    "recieve_id" INTEGER NOT NULL,
                    "service_id" INTEGER NOT NULL,
                    "password" TEXT NOT NULL,
                    FOREIGN KEY ("sending_id")
                    REFERENCES users(id),
                    FOREIGN KEY ("recieve_id")
                    REFERENCES user(id),
                    FOREIGN KEY ("service_id")
                    REFERENCES services(service_id)
                    );
                   ''')
    disconnect(conn)


def get_usernames_list():
    """SQL query to get the list of usernames"""
    conn, cursor = connect()

    cursor.execute('SELECT username FROM users')
    users_list = cursor.fetchall()

    disconnect(conn)

    return users_list


def add_user(username, master_hashed):
    """
    SQL query to add new user into users table

    Parameters:
      username (string): username of the new user
      master_hashed (bytestring): hash of the password of the new user
      key (bytestring): key to encrypt and decrypt the new user passwords

    """
    conn, cursor = connect()

    cursor.execute(f'''INSERT INTO users ("username", "master_password")
                    VALUES ("{username}", "{master_hashed}")''')

    disconnect(conn)


def get_master_pwd(username):
    """
    SQL query to retrive master password of a given user

    Parameters:
      username(string): name of the user wich master password is required

    Returns:
      master_password_hashed[0] (bytestring): hash of the user's master password

    """
    conn, cursor = connect()

    cursor.execute(f'SELECT master_password FROM users WHERE username="{username}"')
    master_password = cursor.fetchone()

    disconnect(conn)

    return master_password[0]

def get_username(ID):
    '''
     SQL query to retrieve id of a given user

    Parameters:
      username(string): name of the user wich id password is required

    Returns:
      user_id (integer): id of the user  
    '''
    conn, cursor = connect()
    cursor.execute(f'SELECT username FROM USERS WHERE id="{ID}"')
    username = cursor.fetchone()[0]
    
    disconnect(conn)
    
    return username
    

def get_user_id(username):
    """
    SQL query to retrieve id of a given user

    Parameters:
      username(string): name of the user wich id password is required

    Returns:
      user_id (integer): id of the user

    """
    conn, cursor = connect()

    cursor.execute(f'SELECT id FROM USERS WHERE username="{username}"')
    user_id = cursor.fetchone()[0]
    disconnect(conn)

    return user_id


def delete_user(user_id):
    """
    SQL query to delete a given user

    Parameters:
      user_id(integer): id of the user to be deleted

    """
    conn, cursor = connect()

    cursor.execute(f'DELETE FROM users WHERE id={user_id}')
    cursor.execute(f'DELETE FROM services WHERE user_id={user_id}')
    cursor.execute(f'DELETE FROM sending WHERE sending_id={user_id} OR recieve_id={user_id}')
    disconnect(conn)


def list_saved_services(user_id):
    """
    SQL query to retrieve all services from a given user

    Parameters:
      user_id(integer): id of the user wich services are required

    Returns:
      services (list): list of services names

    """
    conn, cursor = connect()

    cursor.execute(f'SELECT service_id,service_name, username,password FROM services WHERE user_id="{user_id}"')
    services = cursor.fetchall()
    disconnect(conn)

    return services


def get_key(user_id):
    """
    Get encryption key of the given user

    Parameters:
      user_id(integer): id of the user which key is required

    Returns:
      key (bytestring): encryption key of the user
    """
    conn, cursor = connect()

    cursor.execute(f'SELECT key FROM users where id="{user_id}"')
    key = cursor.fetchone()[0]
    key = key[2:]
    disconnect(conn)

    return key.encode()


def add_service(service_name, username, encrypted_password, user_id, tag, cipher_key, mac_key):
    """
    SQL query to add a service to the services database

    Parameters
      service_name (string): name of the service to be added
      username (string): username of user on service to be added
      encrypted_password (bytestring): encrypted password of user on service to be added
      user_id (integer): id of the user
      tag: result of encryption
      cipher_key: cipher_key for encryption
      mac_key: mac_key for encryption
    """
    conn, cursor = connect()
    cursor.execute(f'''
                    INSERT INTO services (service_name, username, password, user_id, tag,  cipher_key, mac_key)
                    VALUES (?, ?, ?,?,?,?,?)''', (service_name, username, encrypted_password, user_id, tag,  cipher_key, mac_key))
    disconnect(conn)


def check_data_from_service(user_id, service_id):
    """
    SQL query to retrieve data from a service from the services database

    Parameters:
      user_id (integer): id of the user
      service_id (string): name of the service to be checked

    Returns:
      results[0] (string): username on the given service
      results[1][2:] (bytestring): encrypted password on the given service
    """
    conn, cursor = connect()

    cursor.execute(f'''
                    SELECT password, tag, cipher_key, mac_key
                    FROM services
                    WHERE user_id="{user_id}"
                    AND service_id="{service_id}"
                    ''')

    results = list(cursor.fetchone())
    disconnect(conn)
    return results[0], results[1], results[2], results[3]


def update_service_username(user_id, service, username):
    """
    SQL query to update the username of a service in the services database

    Parameters:
      user_id (integer): id of the user updating the username
      service (string): id of the service to be updated
      username (string): new username on the service

    """
    conn, cursor = connect()

    cursor.execute(f'''
                    UPDATE services
                    SET username= ?
                    WHERE user_id= ?
                    AND service_id=?
                    ''', (username,user_id,service))
    disconnect(conn)


def update_service_password(user_id, service, password,tag, cipher_key, mac_key):
    """
    SQL query to update the password of a service in the services database

    Parameters:
      user_id (integer): id of the user updating the username
      service (string): id of the service to be updated
      password (string): new encrypted password on the service

    """
    conn, cursor = connect()

    cursor.execute(f'''
                    UPDATE services
                    SET password= ?,
                    tag = ?,
                    cipher_key = ?,
                    mac_key = ?
                    WHERE user_id= ?
                    AND service_id=?''', (password,tag,cipher_key,mac_key,user_id,service))
    disconnect(conn)


def update_service_name(user_id, service, name):
    """
    SQL query to update the username of a service in the services database

    Parameters:
      user_id (integer): id of the user updating the name of the name
      service (string): id of the service to be updated
      name (string): new name of the service

    """
    conn, cursor = connect()

    cursor.execute(f'''
                    UPDATE services
                    SET service_name="{name}"
                    WHERE user_id="{user_id}"
                    AND service_id="{service}"''')
    disconnect(conn)


def delete_service(user_id, serviceID):
    """
    SQL querry to delete a given service from the services database

    Parameters:
      user_id (integer): id of the user to have a service deleted
      serviceID (string): ID of the service to be deleted
    """
    conn, cursor = connect()

    cursor.execute(f'DELETE FROM services WHERE user_id="{user_id}" AND service_ID="{serviceID}"')
    cursor.execute(f'DELETE FROM sending WHERE recieve_id="{user_id}" AND service_id = "{serviceID}"')
    cursor.execute(f'DELETE FROM sending WHERE sending_id={user_id} AND service_id={serviceID}')
    disconnect(conn)

def send_service(user_id,rec_id,service_id,password):
    conn, cursor = connect()
    cursor.execute(f'''
                   SELECT EXISTS(
                     SELECT 1
                     FROM sending
                     WHERE sending_id = ? AND recieve_id = ? AND service_id = ?
                   );
                   ''', (user_id,rec_id,service_id))
    hold = cursor.fetchone()
    if hold[0] == 0:
      cursor.execute(f'''
                  INSERT INTO sending (sending_id,recieve_id,service_id,password)
                  VALUES (?,?,?,?)
                  ''', (user_id,rec_id,service_id,password))
    disconnect(conn)
    
    return hold[0]
def list_rec (rec_id):
    conn, cursor = connect()


    cursor.execute(f'''
                   SELECT sending_id, service_id
                   FROM sending
                   WHERE recieve_id = "{rec_id}"
                   ''')
    sending_info = cursor.fetchall()
    disconnect(conn)
    return (sending_info)
    # return sending_info

def transfer(sending_id,rec_id,service_id,password):
  conn, cursor = connect()
  cursor.execute(f'''
                   SELECT EXISTS(
                     SELECT 1
                     FROM sending
                     WHERE sending_id = ? AND recieve_id = ? AND service_id = ? AND password = ?
                   );
                   ''', (sending_id,rec_id,service_id,password))
  hold = cursor.fetchone()
  return hold[0]
  
  
def delete_sending(sending_id,rec_id,service_id):
    conn, cursor = connect()

    cursor.execute(f'''
                   DELETE FROM sending
                   WHERE sending_id= ? 
                   AND recieve_id= ?
                   AND service_id = ?
                   ''', (sending_id,rec_id,service_id))
    disconnect(conn)
    return 1

def get_password_sending(sending_id,rec_id,service_id):
    conn, cursor = connect()
    cursor.execute(f'''
                   SELECT password
                   FROM sending
                   WHERE sending_id = ? AND recieve_id = ? AND service_id = ?
                    ''', (sending_id,rec_id,service_id))
    hold = cursor.fetchone()
    disconnect(conn)
    return hold
  
def get_out_going(user_id):
  conn, cursor = connect()


  cursor.execute(f'''
                  SELECT recieve_id,service_id
                   FROM sending
                   WHERE sending_id = "{user_id}"
                   ''')
  sending_info = cursor.fetchall()
  disconnect(conn)
  return (sending_info)

def get_severice_data(user_id,service_id):
  conn, cursor = connect()
  cursor.execute(f'''
                 SELECT service_name
                 FROM services
                 WHERE user_id = ? AND service_id = ?''', (user_id,service_id))
  sending_info = cursor.fetchall()
  disconnect(conn)
  return (sending_info)

  