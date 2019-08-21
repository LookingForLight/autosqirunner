import pymysql
from autosqli.config import Conf
from autosqli.main.form import TaskInfo
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

class sqlalchemy_op:
    def __init__(self):
        self._dburl = "mysql+pymysql://root:root@localhost/taskinfo?charset=utf8"
class database:

    def __init__(self):

        self._dbhost = Conf.DATABASES['HOST']
        self._dbport = Conf.DATABASES['PORT']
        self._dbname = Conf.DATABASES['DBNAME']
        self._dbuser = Conf.DATABASES['USER']
        self._dbpwd = Conf.DATABASES['PWD']
        self._conn = self.connectMySQL()
        if (self._conn):
            self._cursor = self._conn.cursor()

    def connectMySQL(self):
        conn = False
        try:
            conn = pymysql.connect(host=self._dbhost,port=self._dbport,user=self._dbuser,
                                   password=self._dbpwd,db=self._dbname,charset='utf8')
        except Exception as e:

            conn = False
        return conn

    def select_data(self,sql):

        self._cursor.execute(sql)
        res = self._cursor.fetchall()
        self._cursor.close()
        return res
def task_list():
    sql = "select * from taskinfo order by id desc "
    db = database()
    rows = db.select_data(sql)
    db._conn.close()
    return rows

def insert_task(taskid):
    sql = """insert into taskinfo(taskid,status) value (%s,"not running")"""
    db = database()
    db._cursor.execute(sql,taskid)
    db._conn.commit()
    db._conn.close()
if __name__ =="__main__":
    dburl="mysql+mysqlconnector://root:root@localhost/dbtest?charset=utf8"
    engine = create_engine(dburl)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    rows = session.query(TaskInfo.taskid)
    print("count:"+str(rows.count()))
    for row in rows:
        print(row.taskid)
    session.close()

    # print(task_list())