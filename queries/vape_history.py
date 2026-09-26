from backend.db_conn import connect_to_db
import psycopg2
from psycopg2.extras import RealDictCursor

#--add rollback especially on save history
def save_history(user_id, vape_id, nicotine_concentration_mg_per_ml, total_nicotine_inhaled, air_inhaled, date):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        #query to add vape histoy 
        cursor.execute("""INSERT INTO vape_history (user_id, vape_id, nicotine_concentration_mg_per_ml, total_nicotine_inhaled, air_inhaled, date)
                        VALUES (%s,%s,%s,%s,%s,%s)""", (user_id, vape_id, nicotine_concentration_mg_per_ml, total_nicotine_inhaled, air_inhaled, date))
                        
        conn.commit()

        return 'success'

    #catch intergrity errors
    except psycopg2.errors.UniqureViolation as e:
        conn.rollback()
        return f'database integrity error: {e}'

    except Exception as e:
        return f"Unexpected error occured in saving history data: {e}"

    finally:
        if conn:
            conn.close()



def get_all_history_data() -> dict:
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