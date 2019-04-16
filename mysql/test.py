import MySQLdb


class MySQLdbUtil:
    def __init__(self, host, user, passwd):
        self.connection = MySQLdb.connect(
            host=host,
            user=user,
            # port='3306',
            passwd=passwd)

        self.cursor = self.connection.cursor()

    def _execute(self, cmd):
        print ('[execute cmd]', cmd)
        # self.cursor.execute(cmd)

        try:
            # Execute the SQL command
            self.cursor.execute(cmd)
            # Commit your changes in the database
            self.connection.commit()
        except Exception as e:
            print ('[error msg]', e)
            print ('[error cmd]', cmd)
            # Rollback in case there is any error
            self.connection.rollback()

    def _get_list(self):
        return [x[0] for x in self.cursor]

    def _get_one(self):
        return self.cursor.fetchone()[0]

    def _get_all(self):
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    def version(self):
        self._execute("SELECT VERSION()")
        return self._get_one()

    def ls_db(self):
        self._execute("SHOW DATABASES")
        return self._get_list()

    def ls_tb(self):
        self._execute("SHOW TABLES")
        return self._get_list()

    def set_db(self, name):
        self._execute("USE %s" % name)

    def rm_db(self, name):
        self._execute("DROP DATABASE IF EXISTS " + name)

    def create_table(self, name, requirements):
        self._execute("CREATE TABLE %s (%s)" % (name, ','.join(requirements)))

    def insert_into_table(self, name, value_dict):
        k = ','.join(value_dict.keys())
        v = ','.join("'%s'" % str(x) for x in value_dict.values())
        self._execute("INSERT INTO %s (%s) VALUES (%s)" % (name, k, v))

    def select(self, name, requirements=None):
        if requirements:
            self._execute("SELECT * FROM %s WHERE %s" % (name, requirements))
        else:
            self._execute("SELECT * FROM %s" % (name))
        return self._get_all()

    def delete(self, name, requirements=None):
        if requirements:
            self._execute("DELETE FROM %s WHERE %s" % (name, requirements))
        else:
            self._execute("DELETE FROM %s" % (name))

    def update(self, name, assignments, requirements=None):
        if requirements:
            self._execute("UPDATE %s SET %s WHERE %s" % (name, assignments, requirements))
        else:
            self._execute("UPDATE %s SET %s" % (name, assignments))


DB = MySQLdbUtil(
    host='10.224.7.28',
    user='root',
    # port='3306',
    passwd='123456'
)

print (DB.version())
print (DB.ls_db())

DB.rm_db('test_db')
print (DB.ls_db())
# DB.set_db('test_db')

# DB.create_table('EMPLOYEE', ['FIRST_NAME  CHAR(20) NOT NULL',
#                              'LAST_NAME  CHAR(20)',
#                              'AGE INT',
#                              'SEX CHAR(1)',
#                              'INCOME FLOAT',
#                              ])
#
# print ('all tb:', DB.ls_tb())
#
# tb = 'EMPLOYEE'
#
# DB.insert_into_table(tb, {'FIRST_NAME': 'A',
#                           'LAST_NAME': 'B',
#                           'AGE': '10',
#                           'SEX': 'M',
#                           'INCOME': '2000'})
#
# DB.delete(tb, 'AGE > 11')
#
# print (DB.select('EMPLOYEE'))
#
# DB.update('EMPLOYEE', 'AGE = AGE + 1')
# DB.update('EMPLOYEE', 'AGE = AGE * 10')
# print (DB.select('EMPLOYEE'))
