import pymysql as mysql

class DBHack:
    def __init__(self, host="localhost", database = None, user = None, password = None):
        self.SqlNewTeacher = 'INSERT INTO teachers (ID ,name, password) VALUES ("%s","%s", "%s");' #Hoca ıd isim ve şifre alır
        self.SqlNewBoard = 'INSERT INTO smartboards (BoardId ,ClassName, OpenCount, IP) VALUES ("%s","%s","%s", "%s");' #Tahta ıd sınıf adı açılış sayısı ıp 
        self.SqlUpdateTeacher = 'UPDATE teachers SET %s = "%s" WHERE %s = "%s";' #güncellencek ve yeni hali + neyegöre nerde güncelleneceği
        self.SqlUpdateSmartBoard = 'UPDATE smartboards SET %s = "%s" WHERE %s = "%s";'#güncellencek ve yeni hali + neyegöre nerde güncelleneceği
        self.SqlDeletTeacher = 'Delete from teachers where ID = "%s";'#Hoca ıd si
        self.SqlDeleteBoard = 'Delete from smartboards where BoardId = "%s"'#Tahta idsi
        self.SqlTeacherGet = 'select * from teachers where %s = "%s";'#whic data ,ID
        self.SqlBoardGet = 'select * from smartboards where %s = "%s";'#whic data , ID
        self.host = host
        self.database = database
        self.user = user
        self.password = password
    def OpenSv(self):
        sv = mysql.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
        return sv
    def IsUsing(self, comparedData, whicOne):
        bosTuple = ()
        try:
            sv = self.OpenSv()
            sqlTerminal = sv.cursor()
            if whicOne == 1:
                sqlTerminal.execute(self.SqlTeacherGet % ("ID", comparedData))
                feedback = sqlTerminal.fetchall()
                if feedback != bosTuple:
                    return False
                else:
                    return True
            elif whicOne == 2:
                sqlTerminal.execute(self.SqlBoardGet % ("BoardID", comparedData))
                feedback = sqlTerminal.fetchall()
                if feedback != bosTuple:
                    return False
                else:
                    return True
            elif whicOne == 3:
                sqlTerminal.execute(self.SqlBoardGet % ("ClassName", comparedData))
                feedback = sqlTerminal.fetchall()
                if feedback != bosTuple:
                    return False
                else:
                    return True
        finally:
            sqlTerminal.close()#Sanal termianli kapar
            sv.close()#DB bağlntısını kapar 
    def Add(self,id, type_, Name = None, password = None,  className = None, ip = None,count = None):
        try:
            sv = self.OpenSv()
            sqlTerminal = sv.cursor()
            if type_ == "teacher" :
                sqlTerminal.execute(self.SqlNewTeacher % (id, Name, password))
            elif type_ == "board":
                sqlTerminal.execute(self.SqlNewBoard % (id, className, count, ip))
            sv.commit()
        finally:
            sqlTerminal.close()
            sv.close()
    def GetData(self,type_,gatheredData, **kwargs):
        try:
            sv = self.OpenSv()
            sqlTerminal = sv.cursor()
            for key, value in kwargs.items():
                if type_ == "teacher":
                    sqlTerminal.execute(self.SqlTeacherGet % (key, value))
                elif type_ == "board":
                    sqlTerminal.execute(self.SqlBoardGet % (key, value))
                feedback = sqlTerminal.fetchall()
                if feedback == ():
                    return "BOS"
                else:
                    feedback = feedback[0]
                    feedback = str(feedback).replace(" ", "").replace("(", "").replace(")", "").replace("'", "")
                    feedback = feedback.split(",")
                    return feedback[gatheredData]
        finally:
            sqlTerminal.close()
            sv.close()
    def UpdateData(self,type_, **kwargs):
        try:
            sv = self.OpenSv()
            sqlTerminal = sv.cursor()
            datas = []
            for key, value in kwargs.items():
                datas.append(key)
                datas.append(value)
            whichData = datas[0]
            whatTheyBecome = datas[1]
            where = datas[2]
            whereİsHere = datas[3]
            if type_ == "teacher":
                sqlTerminal.execute(self.SqlUpdateTeacher % (whichData, whatTheyBecome, where, whereİsHere))
            elif type_ == "board":
                sqlTerminal.execute(self.SqlUpdateSmartBoard % (whichData, whatTheyBecome, where, whereİsHere))
        finally:
            sv.commit()
            sqlTerminal.close()
            sv.close()
    def DeleteData(self,type_, **kwargs):
        try:
            sv = self.OpenSv()
            sqlTerminal = sv.cursor()
            datas = []
            for key, value in kwargs.items():
                datas.append(key)
                datas.append(value)
            where = datas[1]
            if type_ == "teacher":
                sqlTerminal.execute(self.SqlDeletTeacher % where)
            elif type_ == "board":
                sqlTerminal.execute(self.SqlDeleteBoard % where)
            sv.commit()
        finally:
            sqlTerminal.close()
            sv.close()
    def getOneType(self, type_, data):
        try:
            sv = self.OpenSv()
            sqlTerminal = sv.cursor()
            if type_ == "teacher":
                sqlTerminal.execute("select %s from teachers" % data)
                data = sqlTerminal.fetchall()
                return data
            elif type_ == "board":
                sqlTerminal.execute("select %s from smartboards" % data)
                data = sqlTerminal.fetchall()
                ips = []
                for datas in data:
                    datas = str(datas).replace(" ", "").replace("(", "").replace(")", "").replace("'", "")
                    datas = datas.split(",")
                    datas = datas[0]
                    print(datas)
                    ips.append(datas)
                return ips
        finally:
            sqlTerminal.close()
            sv.close()