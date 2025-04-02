import sqlite3
from contextlib import closing

def get_connection():
    return closing(sqlite3.connect("main.db", timeout=3))

def set_movie_items(code, name, genre, duration, country, movie_id):
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            sql = "INSERT INTO kinolar (kino_nomi, kino_kodi, davomiyligi, janri, davlati, kino_id) VALUES (?, ?, ?, ?, ?, ?)"
            val = (name, code, duration, genre, country, movie_id)
            cursor.execute(sql, val)
            connection.commit()
        return "Ma'lumotlar saqlandi."
    except Exception as e:
        return f"Ma'lumotlar saqlanishida xatolik! \n {e}"

def get_movie_items(code):
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            ans = cursor.execute(f"SELECT * FROM kinolar WHERE kino_kodi = {code};")
            for i in ans:
                name = i[0]
                duration = i[2]
                genre = i[3]
                country = i[4]
                movie_id = i[5]
        return name, duration, genre, country, movie_id
    except Exception:
        return "Bu kodda kino topilmadi"

def get_movie_code():
    try:
        with get_connection() as connection:
            movie_codes = []
            cursor = connection.cursor()
            ans = cursor.execute(f"SELECT kino_kodi FROM kinolar kinolar")
            for i in ans:
                movie_codes.append(i[0])
        return movie_codes
    except Exception as e:
        raise e

def update_item(column_name, value, movie_code):
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE kinolar SET {column_name} = ? WHERE kino_kodi = ?", (value, movie_code))
            connection.commit()
    except Exception as e:
        raise e

def delete_item(movie_code):
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM kinolar WHERE kino_kodi = ?", (movie_code,))
            connection.commit()
    except Exception as e:
        raise e

def get_movies_info():
    try:
        kino_nomlari, kino_kodlari = [], []
        with get_connection() as connection:
            cursor = connection.cursor()
            ans = cursor.execute("SELECT kino_nomi, kino_kodi FROM kinolar")
            for i in ans:
                kino_nomlari.append(i[0])
                kino_kodlari.append(i[1])
            return kino_nomlari, kino_kodlari
    except Exception as e:
        raise e