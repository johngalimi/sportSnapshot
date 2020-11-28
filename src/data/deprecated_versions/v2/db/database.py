import psycopg2


def connect_db(database, user, password, host):

    cxn_string = "dbname={} user={} password={} host={}".format(
        database, user, password, host
    )

    conn = psycopg2.connect(cxn_string)

    cur = conn.cursor()

    return conn, cur


def disconnect_db(connection, cursor):

    cursor.close()
    connection.close()

    del cursor
    del connection


def create_tables(connection, cursor):

    commands = (
        """
            CREATE TABLE IF NOT EXISTS teams (
                scTeamId INTEGER NOT NULL,
                scTeamAbbr VARCHAR(5) NOT NULL,
                scTeamName VARCHAR(255) NOT NULL,
                PRIMARY KEY (scTeamId)
            )
            """,
    )

    for command in commands:
        cursor.execute(command)

    connection.commit()


if __name__ == "__main__":

    db_name = "sportsnapshot"
    credential = "postgres"
    host = "localhost"

    cxn, curs = connect_db(db_name, credential, credential, host)

    create_tables(cxn, curs)

    disconnect_db(cxn, curs)
