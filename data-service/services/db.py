import psycopg2
from psycopg2.extras import RealDictCursor
from config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def execute_query(query, params=None, fetch=True):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        if fetch:
            result = cur.fetchall()
        else:
            result = None
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise e
    finally:
        cur.close()
        conn.close()