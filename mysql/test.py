import MySQLdb


class MySQLdbUtil:
    def __init__(self, host, user, passwd):
        connection = MySQLdb.connect(
            host=host,
            user=user,
            # port='3306',
            passwd=passwd)

        self.cursor = connection.cursor()

    def ls_db(self):
        self.cursor.execute("SHOW DATABASES")
        return [x[0] for x in self.cursor]

    def ls_tb(self):
        self.cursor.execute("SHOW TABLES")
        return [x[0] for x in self.cursor]

    def set_db(self, name):
        self.cursor.execute("USE " + name)

    def rm_db(self, name):
        self.cursor.execute("DROP DATABASE IF EXISTS " + name)


DB = MySQLdbUtil(
    host='10.224.7.28',
    user='root',
    # port='3306',
    passwd='123456'
)

DB.rm_db('zhaotong_db')

print ('all db:', DB.ls_db())

DB.set_db('test_db')

print ('all tb:', DB.ls_tb())