import pymysql as mysql

class DBHack:
    def __init__(self):
        self.SqlUpdateTeacher = 'UPDATE %s_teacher_info SET %s = "%s" WHERE %s = "%s";' #güncellencek ve yeni hali + neyegöre nerde güncelleneceği
        self.SqlUpdateSmartBoard = 'UPDATE %s_class_info SET %s = "%s" WHERE %s = "%s";'#güncellencek ve yeni hali + neyegöre nerde güncelleneceği
        self.SqlDeletTeacher = 'Delete from teachers where ID = "%s";'#Hoca ıd si
        self.SqlDeleteBoard = 'Delete from smartboards where BoardId = "%s"'#Tahta idsi
        self.SqlBoardGet = 'select * from %s_class_info where %s = "%s";'#whic data , ID
        self.SqlTeacherGet = 'select * from %s_teacher_info where %s = "%s";'#whic data , ID
        self.SqlAddSmartBoard = 'INSERT INTO %s (class,ip) VALUES ("%s","%s");'#class ip currentpassword
        self.host = "localhost"
        self.database = None
        self.user = "root"
        self.password = "fcal123"


    def OpenSv(self,database = None):#Bağlantıyı açma
        sv = mysql.connect(
                host=self.host,
                database=database,
                user=self.user,
                password=self.password,
                charset="utf8mb4"
            )
        return sv
    

    def GetTables(self):#Bütün tabloları listeleme
        """Return the all databases in a str"""
        sv = self.OpenSv()
        sqlTerminal = sv.cursor()
        sqlTerminal.execute("use aquamain;")
        sqlTerminal.execute("show tables;")
        tables = []
        for i in sqlTerminal.fetchall():
           for a in i:
               tables.append(a)
        sqlTerminal.close()
        sv.close()
        return tables

    def IsUsing(self,schoolName, comparedData, whicOne):
        """okul adı neye göre = İp ad ...          1 2 3"""
        bosTuple = ()
        sv = self.OpenSv("aquamain")
        sqlTerminal = sv.cursor()
        if whicOne == 1:# hoca ID sine göre
            sqlTerminal.execute()
            feedback = sqlTerminal.fetchall(self.SqlTeacherGet % (schoolName,"ID",comparedData))
            if feedback != bosTuple:
                return False
            else:
                return True
        elif whicOne == 2:#ip sine göre
            sqlTerminal.execute()
            feedback = sqlTerminal.fetchall(self.SqlBoardGet % (schoolName,"ip",comparedData))
            if feedback != bosTuple:
                return False
            else:
                return True
        elif whicOne == 3:#sınıf adına göre
            sqlTerminal.execute(self.SqlBoardGet % (schoolName,"class",comparedData))
            feedback = sqlTerminal.fetchall()
            if feedback != bosTuple:
                return False
            else:
                return True
        sqlTerminal.close()
        sv.close()
    def UpdateData(self,type_,schoolName,**kwargs):
        sv = self.OpenSv("aquamain")
        sqlTerminal = sv.cursor()
        data = []
        for key,value in kwargs.items():
            data.append(key)
            data.append(value)
        if type_ == "teacher":
            sqlTerminal.execute(self.SqlUpdateTeacher % (schoolName,data[0], data[1], data[2], data[3]))
        elif type_ == "board":
            sqlTerminal.execute(self.SqlUpdateSmartBoard % (schoolName,data[0], data[1], "class", data[3]))
        sv.commit()
        sqlTerminal.close()
        sv.close()
        
    def GetWholeData(self,schoolName,data):
        sv = self.OpenSv("aquamain")
        sqlTerminal = sv.cursor()
        sqlTerminal.execute(self.SqlTeacherGet % (schoolName,"teacher",data))
        feedback = sqlTerminal.fetchall()
        bosTuple = ()
        if feedback == bosTuple:
            sqlTerminal.execute(self.SqlTeacherGet % (schoolName,"ID",data))
            feedback = sqlTerminal.fetchall()
            if feedback == bosTuple:
                return "0"
        sqlTerminal.close()
        sv.close()
        return feedback[0]

    def MakeNewSchool(self,schoolName):#okul ekleme
        sv = self.OpenSv("aquamain")
        sqlTerminal = sv.cursor()
        sqlTerminal.execute(f"CREATE TABLE {schoolName}_teacher_info (ID INT PRIMARY KEY,teacher VARCHAR(100),password VARCHAR(100));")
        sv.commit()
        sqlTerminal.execute(f"CREATE TABLE {schoolName}_class_info (class VARCHAR(100),ip VARCHAR(50));")
        sv.commit()
        sqlTerminal.close()
        sv.close()

    def GetIp(self,schoolName,className):
        sv = self.OpenSv("aquamain")
        sqlTerminal = sv.cursor()
        sqlTerminal.execute(self.SqlBoardGet % (schoolName,"class",className))
        feedback = sqlTerminal.fetchall()
        feedback = feedback[0]
        feedback = feedback[1]
        sqlTerminal.close()
        sv.close()
        return feedback
    def NewSmartBorad(self,schoolName,className,ip):#tahta ekleme
        sv = self.OpenSv(database="aquamain")
        sqlTerminal = sv.cursor()
        print(className)
        sqlTerminal.execute(self.SqlAddSmartBoard % (f"{schoolName}_class_info",className,ip))
        sv.commit()
        sqlTerminal.close()
        sv.close()