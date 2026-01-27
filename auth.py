import bcrypt
from db import get_connection

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

salt = bcrypt.gensalt()

#print(salt)
#password_hash = print(hash_password('nin'))

def verify_password(password, password_hash):
    """Verify a password to its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def register_user(username, password):
    """Registers a new user and creates their account"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        # string interpolation will make code vulnerable to sql injection
        cursor.execute("select id from users where username = %s", (username,))
        if cursor.fetchone():
            print(f"username: {username} already exists!")
            return False
        
        #hash password and insert user
        password_hash = hash_password(password)
        
        cursor.execute(
            "insert into users (username, password_hash) values (%s, %s) returning id", (username, password_hash)
        )
        
        result = cursor.fetchone()
        
        if result == None:
            raise Exception ('Error')
    
        user_id = result[0]
        
        #Create new account for user with balance of 0
        cursor.execute(
            "insert into accounts (user_id, balance) values (%s, 0.00)",
            (user_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Registration successful!")
        
    except Exception as e:
        print(f"Error registering user:{e}")
        return False
        
        
def login_user(username, password):
    """Authenticate user and return user id if successful"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute('select id, password_hash from users where username = %s', (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result:
            print('Invalid username or password!')
            return None 
        
        user_id, password_hash = result
        
        if verify_password(password, password_hash):
            return user_id
        else:
            print('Invalid username or password!')
            return None
    except Exception as e:
        print("Error logging in: {e}")
        return None
    
    
register_user('gevorkiani3', 'secret')
register_user('tsertsvadzel', 'secret')

logged_in = login_user('gevorkiani3', 'secret')
print(logged_in)