import pymssql


def main():
    server = r"192.168.0.3"
    user = "nyjj"
    password = "nyjj"
    database = "nyjj"

    with pymssql.connect(server=server, user=user, password=password, database=database, charset="GBK") as db:
        with db.cursor(as_dict=True) as cursor:
            sql = "SELECT * FROM GBD"

            cursor.execute(sql)

            rows = cursor.fetchall()

            print(rows[0])


if __name__ == '__main__':
    main()







