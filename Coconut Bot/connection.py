import psycopg2

def connect_to_database():
    try:
        # connecting to database
        connection = psycopg2.connect(user = "user",
                                      password = "password",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "coconut_bot")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        return connection, cursor

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")

def close_connection_to_database(cursor: psycopg2.extensions.cursor, connection: psycopg2.extensions.connection):
    try:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    except (Exception, psycopg2.Error) as error:
        print(f"Error while disconnection from PostgreSQL: {error}")

def insert_DiscordUser_into_databse(member_id: int, cursor: psycopg2.extensions.cursor,
                                    connection: psycopg2.extensions.connection):
    try:
        cursor.execute(sql_insert_DiscordUser_into_database, (member_id,))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error while inserting into DiscordUser on database: {error}")

def insert_DiscordUserVoiceSession_into_database(member_id: int, channel_id: int,
                                                 session_amount: float,
                                                 cursor: psycopg2.extensions.cursor,
                                                 connection: psycopg2.extensions.connection):
    try:
        cursor.execute(sql_insert_DiscordUserVoiceSession_into_Database, (member_id, channel_id, session_amount))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error while inserting into DiscordUserVoiceSession on database: {error}")

def select_DiscordUserVoiceSession_from_command_caller(member_id: int, cursor: psycopg2.extensions.cursor):
    try:
        cursor.execute(sql_select_DiscordUserVoiceSession_from_command_caller, (member_id,))
        return cursor.fetchone()

    except (Exception, psycopg2.Error) as error:
        print(f"Error while selecting from DiscordUserVoiceSession on database: {error}")

def select_DiscordUser_from_database(member_id: int, cursor: psycopg2.extensions.cursor):
    try:
        cursor.execute(sql_select_DiscordUser, (member_id,))
        return cursor.fetchone()
    except (Exception, psycopg2.Error) as error:
        print(f"Error while selecting from DiscordUser on database: {error}")

sql_select_total_time_spent = """
SELECT SUM(total_time_spent)
FROM DiscordUserVoiceSession
WHERE voice_channel_id = %s AND discord_user_id = %s"""

sql_select_DiscordUser = """
SELECT *
FROM DiscordUser
WHERE discord_user_id = %s"""

sql_insert_DiscordUser_into_database = """
INSERT INTO DiscordUser (discord_user_id)
VALUES (%s)"""

sql_insert_DiscordUserVoiceSession_into_Database = """
INSERT INTO DiscordUserVoiceSession (discord_user_id, voice_channel_id, total_time_spent)
VALUES (%s, %s, %s)"""

sql_select_DiscordUserVoiceSession_from_command_caller = """
SELECT discord_user_id, voice_channel_id, SUM(total_time_spent) AS total
FROM DiscordUserVoiceSession WHERE discord_user_id = %s
GROUP BY discord_user_id, voice_channel_id
ORDER BY total DESC
LIMIT 1"""
