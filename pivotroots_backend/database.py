import os
import time
import psycopg2
from psycopg2 import pool

## i am entrusting these creds for testin purposes
DB_NAME = os.environ.get('POSTGRES_USER', 'test-ephemeral')
DB_HOST = os.environ.get('POSTGRES_HOST','ep-nameless-cake-05539415.ap-southeast-1.aws.neon.tech')
DB_USER = os.environ.get('POSTGRES_USER', 'akashjaiswar')
DB_PASS = os.environ.get('POSTGRES_PASSWORD','4Fu6yibqtNoR')
DB_PORT = os.environ.get('POSTGRES_PORT','5432')

conn_pool = psycopg2.pool.ThreadedConnectionPool (
    1,
    2,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    dbname=DB_NAME,
    port=DB_PORT)

print("Database connction established")

class DB():
    # def __init__ (self,num):
    #     self.num = num

    def run(self, query, args=()):
        global conn_pool
        conn = self._getConnection()

        if conn is None:
            print("EXIT from db.run")
            self.recon()

        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(query, args)
        cur.close ()
        conn_pool.putconn(conn)
        return True

    def execute(self, query, args=()):
        global conn_pool
        conn = self._getConnection()

        if conn is None:
            print("EXIT from db.execute")
            self.recon()

        cur = conn.cursor()
        cur.execute(query, args)
        result = cur.fetchone()
        cur.close()
        conn_pool.putconn(conn)
        return result

    def query_db(self, query, args=(), one=False):
        global conn_pool
        conn = self._getConnection()

        if conn is None:
            print("EXIT from db.querydb")
            self.recon()

        cur = conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        result = (r[0] if r else None) if one else r
        cur.close()
        conn_pool.putconn(conn)
        return result

    def recon(self):
        global conn_pool
        conn_pool = psycopg2.pool.ThreadedConnectionPool (
                    1,
                    2,
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASS,
                    dbname=DB_NAME,
                    port=DB_PORT)

    def _getConnection(self):
        global conn_pool

        while 1:
            conn = None
            if not conn_pool:
                time.sleep(1)
                self.recon()            
                continue
            try:
                conn = conn_pool.getconn()
            except psycopg2.pool.PoolError:
                time.sleep(1)
            except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
                self.recon()
            except Exception as e:
                print("Odd Exception",e)
            if conn:
                return conn
