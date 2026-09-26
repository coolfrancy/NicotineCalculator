def get_nicotine_concentration(id:int -> int):
    try:
        from backend.db_conn import connect_to_db

        
        conn = connect_to_db
        cursor = conn.cursor()

        cursor.execute("""
        SELECT nicotine_concentration_mg_per_ml FROM user_to_vape WHERE id=%s
        """, (id,))

        info = cursor.fetchall()
        conn.close()

    
    except Exception as e:
        raise Exception(f'Unexpected error occured when getting use nicotine concentration {e}')
    finally:
        if conn:
            conn.close()

if __name__=='__main__':
    get_nicotine_concentration()
