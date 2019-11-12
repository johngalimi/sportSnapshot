import psycopg2


def connect_db(database, user, password, host):

    cxn_string = "dbname={} user={} password={} host={}".format(
            database, user, password, host)

    conn = psycopg2.connect(cxn_string)

    cur = conn.cursor()

    return conn, cur


def disconnect_db(connection, cursor):
    
    del cursor
    connection.close()


if __name__ == '__main__':

    db_name = 'sportsnapshot'
    credential = 'postgres'
    host = 'localhost'

    cxn, curs = connect_db(db_name, credential, credential, host))

    disconnect_db(cxn, curs)
