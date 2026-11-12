from backend.db_conn import connect_to_db
import psycopg2
from psycopg2.extras import RealDictCursor

#--add rollback especially on save history
def save_history(user_id, vape_id, nicotine_concentration_mg_per_ml, air_inhaled, temperature, date):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        #query to add vape histoy 
        cursor.execute("""INSERT INTO vape_history (user_id, vape_id, nicotine_concentration_mg_per_ml, air_inhaled, temperature, date)
                        VALUES (%s,%s,%s,%s,%s,%s)""", (user_id, vape_id, nicotine_concentration_mg_per_ml, air_inhaled, temperature, date))
                        
        conn.commit()

        return 'success'

    #catch intergrity errors
    except psycopg2.errors.UniqueViolation as e:
        conn.rollback()
        return f'database integrity error: {e}'

    except Exception as e:
        return f"Unexpected error occured in saving history data: {e}"

    finally:
        if conn:
            conn.close()



def update_total_nicotine(history_id, total_nicotine_inhaled):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        #query to set total nicotine inhaled for a single history row
        cursor.execute("""UPDATE vape_history SET total_nicotine_inhaled = %s WHERE id = %s""",
                       (total_nicotine_inhaled, history_id))

        if cursor.rowcount == 0:
            conn.rollback()
            return f'No history row found with id {history_id}'

        conn.commit()
        return 'success'

    except Exception as e:
        if conn:
            conn.rollback()
        return f"Unexpected error occured in updating total nicotine inhaled: {e}"

    finally:
        if conn:
            conn.close()


def get_all_history_data() -> dict:
    conn = None
    try:

        conn=connect_to_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
        SELECT * FROM all_vape_history_view
        """)
        info = cursor.fetchall()
        return info
    
    except Exception as e:
        return f'Error occured in getting all history data: {e}'
    finally:
        if conn:
            conn.close()