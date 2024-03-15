"""Functions"""

from datetime import datetime
import uuid
import database as db

def create_user(user_id, name, password):
    """Luo käyttäjän"""
    db.C.execute("INSERT OR IGNORE INTO users (user_id, name, password) VALUES (?, ?, ?)",
               (user_id, name, password))
    db.CONN.commit()
    print("Käyttäjä on luotu onnistuneesti")

def del_user(admin_id, user_id):
    """Poistaa käyttäjän"""
    if admin_id != '1':
        print("Vain pääkäyttäjällä on oikeus poistaa käyttäjiä.")
        return

    if user_id == admin_id:
        print("Et voi poistaa pääkäyttäjää.")
        return

    db.C.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    db.CONN.commit()

    db.C.execute("DELETE FROM history WHERE user_id=?", (user_id,))
    db.CONN.commit()
    print("Käyttäjä poistettu onnistuneesti.")

def login(user_id, password):
    """Kirjaa käyttäjän sisään"""
    db.C.execute("SELECT * FROM users WHERE user_id=? AND password=?", (user_id, password))
    user = db.C.fetchone()
    if user:
        start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.C.execute("INSERT INTO history (user_id, start_date) VALUES (?, ?)",
                  (user_id, start_date))
        db.CONN.commit()

        token = str(uuid.uuid4())
        db.C.execute("UPDATE users SET token = ? WHERE user_id = ?", (token, user[1]))
        db.CONN.commit()

        print("Kirjauduttu sisään onnistuneesti.")

        return user[1], token

    print("Virheellinen käyttäjätunnus tai salasana.")
    return None, None

def logout(user_id):
    """Kirjaa käyttäjän ulos"""
    end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.C.execute("UPDATE history SET end_date=? WHERE user_id=? AND end_date IS NULL",
              (end_date, user_id))
    db.CONN.commit()
    print("Kirjauduttu ulos onnistuneesti")

def get_userid(token):
    """Hankkii käyttäjätunnuksen"""
    db.C.execute("SELECT user_id FROM users WHERE token=?", (token,))
    user_id = db.C.fetchone()

    return user_id[0] if user_id else None

def check_status(user_id):
    """Tarkistaa statuksen"""
    db.C.execute("SELECT start_date, end_date FROM history WHERE user_id=?", (user_id,))
    status_records = db.C.fetchall()

    total_time = 0

    if not status_records:
        print(f"Ei kirjautumis historiaa löytynyt käyttäjätunnukselle {user_id}")
    else:
        print(f"Status käyttäjälle {user_id}:")
        for record in status_records:
            start_date, end_date = record
            end_date_str = "*Currently logged in*" if end_date is None else end_date

            if end_date is None:
                print(f"Start date: {start_date}, End date: {end_date_str}\n")
            else:
                total_time_str = total(start_date, end_date)
                print(f"Start date: {start_date}, End date: {end_date}, Total: {total_time_str}\n")

            total_time += total_seconds(start_date, end_date)

        total_time_format = format_time(total_time)
        print(f"\nTotal time: {total_time_format}")

def total_seconds(start_time, end_time):
    """Laskee total sekunnit"""
    if end_time is None:
        return 0

    start_time_str = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time_str = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    total_time = (end_time_str - start_time_str).total_seconds()
    return total_time

def format_time(time):
    """Muotoilee ajan"""
    time = int(time)
    years = time // (365 * 24 * 3600)
    time %= (365 * 24 * 3600)
    months = time // (30 * 24 * 3600)
    time %= (30 * 24 * 3600)
    days = time // (24 * 3600)
    time %= (24 * 3600)
    hours = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time

    return f"{years} years, {months} months, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

def total(start_time, end_time):
    """Laskee total ajan"""
    if end_time is None:
        return "Currently logged in"

    start_time_str = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time_str = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    total_time = end_time_str - start_time_str

    years = total_time.days // 365
    months = (total_time.days % 365) // 30
    days = total_time.days % 30
    hours = total_time.seconds // 3600
    minutes = (total_time.seconds % 3600) // 60
    seconds = total_time.seconds % 60

    return f"{years} years, {months} months, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
