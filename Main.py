from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtDesigner
import sqlite3
import Forms.MainForm as MainForm

class Window(QtWidgets.QMainWindow, MainForm.Ui_MainWindow):
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.start()

    def start(self):
        self.action.setCheckable(True)
        self.action_2.setCheckable(True)
        self.action.setChecked(True)
        self.initDB()
        self.action.setChecked(True)
        self.setUniversities()
        self.setFaculties()
        self.setSpecialities()
        self.setSubjects()
        self.run()

    def initDB(self):
        self.con = sqlite3.connect("./DataBase/database_ru.db")
        self.cur = self.con.cursor()
    
    def run(self):
        self.UniversitiesCB.activated.connect(self.UniversitiesCB_Change)
        self.FacultiesCB.activated.connect(self.FacultiesCB_Change)
        self.SpecialtiesCB.activated.connect(self.SpecialtiesCB_Change)
        self.FirstSubjectCB.activated.connect(self.FirstSubjectCB_Change)
        self.SecondSubjectCB.activated.connect(self.SecondSubjectCB_Change)
        self.action.triggered.connect(self.actionChanged)
        self.action_2.triggered.connect(self.action_2Changed)
        self.SearchButton.clicked.connect(self.search)

    def setUniversities(self):
        self.UniversitiesCB.clear()
        self.UniversitiesCB.addItem('----Выберите университет-----')
        self.cur.execute("SELECT name, code FROM universities")
        for name, code in self.cur:
            self.UniversitiesCB.addItem('{0} - {1}'.format(code, name))

    def setFaculties(self):
        self.FacultiesCB.clear()
        self.FacultiesCB.addItem('----Выберите факультет-----')
        self.cur.execute("SELECT name FROM faculties")
        for name in self.cur:
            self.FacultiesCB.addItem(name[0])

    def setSpecialities(self):
        self.SpecialtiesCB.clear()
        self.SpecialtiesCB.addItem('----Выберите специальность------')
        if self.action_2.isChecked():
            self.cur.execute("SELECT name, code FROM specialities WHERE language_group = 'казахская'")
            for name, code in self.cur:
                self.SpecialtiesCB.addItem('{0} - {1}'.format(code, name))
        elif self.action.isChecked():
            self.cur.execute("SELECT name, code FROM specialities WHERE language_group = 'русская'")
            for name, code in self.cur:
                self.SpecialtiesCB.addItem('{0} - {1}'.format(code, name))

    def setSubjects(self):
        self.FirstSubjectCB.clear()
        self.SecondSubjectCB.clear()
        self.FirstSubjectCB.addItem('----Выберите предмет-----')
        self.SecondSubjectCB.addItem('----Выберите предмет-----')
        self.cur.execute("SELECT name FROM subjects")
        for name in self.cur:
            self.FirstSubjectCB.addItem(name[0])
            self.SecondSubjectCB.addItem(name[0])
                
    def changeSpecialities(self):
        if self.UniversitiesCB.currentIndex() == 0 and self.FacultiesCB.currentIndex() == 0:
            self.setSpecialities()
        
    @QtCore.pyqtSlot(int)
    def UniversitiesCB_Change(self):
        print(self.UniversitiesCB.currentIndex())
        print(self.FacultiesCB.currentIndex())
        print(self.SpecialtiesCB.currentIndex())
        print(self.FirstSubjectCB.currentIndex())
        print(self.SecondSubjectCB.currentIndex())
        if self.UniversitiesCB.currentIndex() == 0:
            self.setUniversities()
            self.setFaculties()   
            self.setSpecialities() 
            self.setSubjects()
        else:
            container = []
            if not self.FacultiesCB.currentIndex():
                self.FacultiesCB.clear()
                self.FacultiesCB.addItem('----Выберите факультет-----')
                sql = """SELECT faculties.name
                        FROM universities, faculties, specialities
                        WHERE faculties.belong_to_university = universities.code
                        AND faculties.name = specialities.belong_to_faculty
                        AND specialities.belong_to_university = universities.code"""
                
                sql += "\nAND universities.code = (?)"
                container.append(self.UniversitiesCB.currentText().split(' ')[0])
                
                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])
                
                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())
                
                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name in self.cur:
                    self.FacultiesCB.addItem(name[0])
                container.clear()

            if not self.SpecialtiesCB.currentIndex():
                self.SpecialtiesCB.clear()
                self.SpecialtiesCB.addItem('----Выберите специальность------')
                sql = """SELECT specialities.name, specialities.code
                        FROM universities, faculties, specialities
                        WHERE specialities.belong_to_university = universities.code
                        AND specialities.belong_to_faculty = faculties.name
                        AND specialities.belong_to_university = faculties.belong_to_university"""

                sql += "\nAND universities.code = (?)"
                container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())

                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))

                for name, code in self.cur:
                    self.SpecialtiesCB.addItem('{0} - {1}'.format(code, name))
                container.clear()
            
            if not self.FirstSubjectCB.currentIndex():
                self.FirstSubjectCB.clear()
                self.FirstSubjectCB.addItem('----Выберите предмет-----')
                sql = """SELECT subjects.name
                         FROM universities, faculties, specialities, subjects
                         WHERE faculties.belong_to_university = universities.code
                         AND faculties.belong_to_university = specialities.belong_to_university
                         AND specialities.belong_to_university = universities.code
                         AND specialities.belong_to_faculty = faculties.name
                         AND subjects.name = specialities.require_subject_1"""
                
                sql += "\nAND universities.code = (?)"
                container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])
                
                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())
                
                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')
                
                self.cur.execute(sql, tuple(container))
                for name in self.cur:
                    self.FirstSubjectCB.addItem(name[0])
                container.clear()
            
            if not self.SecondSubjectCB.currentIndex():
                self.SecondSubjectCB.clear()
                self.SecondSubjectCB.addItem('----Выберите предмет-----')
                sql = """SELECT subjects.name
                         FROM universities, faculties, specialities, subjects
                         WHERE faculties.belong_to_university = universities.code
                         AND faculties.belong_to_university = specialities.belong_to_university
                         AND specialities.belong_to_university = universities.code
                         AND specialities.belong_to_faculty = faculties.name
                         AND subjects.name = specialities.require_subject_2"""
                
                sql += "\nAND universities.code = (?)"
                container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])
                
                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))
                for name in self.cur:
                    self.SecondSubjectCB.addItem(name[0])
                container.clear()
            del container

    @QtCore.pyqtSlot(int)
    def FacultiesCB_Change(self):
        print(self.UniversitiesCB.currentIndex())
        print(self.FacultiesCB.currentIndex())
        print(self.SpecialtiesCB.currentIndex())
        print(self.FirstSubjectCB.currentIndex())
        print(self.SecondSubjectCB.currentIndex())
        if self.FacultiesCB.currentIndex() == 0:
            self.setUniversities()
            self.setSpecialities()
            self.setFaculties()
            self.setSubjects()
        else:
            container = []
            if not self.UniversitiesCB.currentIndex():
                self.UniversitiesCB.clear()
                self.UniversitiesCB.addItem('----Выберите университет-----')
                sql = """SELECT universities.name, universities.code
                        FROM universities, faculties, specialities
                        WHERE universities.code = faculties.belong_to_university
                        AND faculties.name = specialities.belong_to_faculty
                        AND universities.code = specialities.belong_to_university
                        AND specialities.belong_to_university = faculties.belong_to_university"""
                
                sql += "\nAND faculties.name = (?)"
                container.append(self.FacultiesCB.currentText())

                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])
                
                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())

                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name, code in self.cur:
                    self.UniversitiesCB.addItem('{0} - {1}'.format(code, name))
                container.clear()

            if not self.SpecialtiesCB.currentIndex():
                self.SpecialtiesCB.clear()
                self.SpecialtiesCB.addItem('----Выберите специальность------')
                sql = """SELECT specialities.name, specialities.code
                        FROM universities, faculties, specialities
                        WHERE specialities.belong_to_university = universities.code
                        AND faculties.belong_to_university = universities.code
                        AND specialities.belong_to_faculty = faculties.name"""

                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                sql += "\nAND faculties.name = (?)"
                container.append(self.FacultiesCB.currentText())

                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())

                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name, code in self.cur:
                    self.SpecialtiesCB.addItem('{0} - {1}'.format(code, name))
                container.clear()

            if not self.FirstSubjectCB.currentIndex():
                self.FirstSubjectCB.clear()
                self.FirstSubjectCB.addItem('----Выберите предмет-----')
                sql = """SELECT subjects.name 
                        FROM universities, faculties, specialities, subjects
                        WHERE universities.code = faculties.belong_to_university
                        AND universities.code = specialities.belong_to_university
                        AND specialities.belong_to_faculty = faculties.name
                        AND specialities.belong_to_university = faculties.belong_to_university
                        AND subjects.name = specialities.require_subject_1"""

                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                sql += "\nAND faculties.name = (?)"
                container.append(self.FacultiesCB.currentText())

                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])
                
                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name in self.cur:
                    self.FirstSubjectCB.addItem(name[0])
                container.clear()

            if not self.SecondSubjectCB.currentIndex():
                self.SecondSubjectCB.clear()
                self.SecondSubjectCB.addItem('----Выберите предмет-----')
                sql = """SELECT subjects.name
                        FROM universities, faculties, specialities, subjects
                        WHERE universities.code = faculties.belong_to_university
                        AND universities.code = specialities.belong_to_university
                        AND specialities.belong_to_faculty = faculties.name
                        AND specialities.belong_to_university = faculties.belong_to_university
                        AND subjects.name = specialities.require_subject_2"""

                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                sql += "\nAND faculties.name = (?)"
                container.append(self.FacultiesCB.currentText())

                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])

                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())
                
                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name in self.cur:
                    self.SecondSubjectCB.addItem(name[0])
                container.clear()
            del container


    @QtCore.pyqtSlot(int)
    def SpecialtiesCB_Change(self):
        print(self.UniversitiesCB.currentIndex())
        print(self.FacultiesCB.currentIndex())
        print(self.SpecialtiesCB.currentIndex())
        print(self.FirstSubjectCB.currentIndex())
        print(self.SecondSubjectCB.currentIndex())
        if self.SpecialtiesCB.currentIndex() == 0:
            self.setFaculties()
            self.setUniversities()
            self.setSpecialities()
        else:
            container = []
            if not self.UniversitiesCB.currentIndex():
                self.UniversitiesCB.clear()
                self.UniversitiesCB.addItem('----Выберите университет-----')
                sql = """SELECT universities.name, universities.code
                        FROM universities, faculties, specialities
                        WHERE universities.code = faculties.belong_to_university
                        AND universities.code = specialities.belong_to_university
                        AND faculties.name = specialities.belong_to_faculty
                        AND faculties.belong_to_university = specialities.belong_to_university"""
                
                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                sql += "\nAND specialities.code = (?)"
                container.append(self.SpecialtiesCB.currentText().split(' ')[0])

                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())
                
                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name, code in self.cur:
                    self.UniversitiesCB.addItem('{0} - {1}'.format(code, name))
                container.clear()

            if not self.FacultiesCB.currentIndex():
                self.FacultiesCB.clear()
                self.FacultiesCB.addItem('----Выберите факультет-----')
                sql ="""SELECT faculties.name
                        FROM universities, faculties, specialities
                        WHERE universities.code = faculties.belong_to_university
                        AND universities.code = specialities.belong_to_university
                        AND specialities.belong_to_faculty = faculties.name
                        AND specialities.belong_to_university = faculties.belong_to_university"""
                
                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                sql += "\nAND specialities.code = (?)"
                container.append(self.SpecialtiesCB.currentText().split(' ')[0])

                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())

                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())
                
                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name in self.cur:
                    self.FacultiesCB.addItem(name[0])
                container.clear()
            
            if not self.FirstSubjectCB.currentIndex():
                self.FirstSubjectCB.clear()
                self.FirstSubjectCB.addItem('----Выберите предмет-----')
                sql = """SELECT subjects.name
                        FROM universities, faculties, specialities, subjects
                        WHERE universities.code = faculties.belong_to_university
                        AND universities.code = specialities.belong_to_university
                        AND specialities.belong_to_faculty = faculties.name
                        AND specialities.belong_to_university = faculties.belong_to_university
                        AND subjects.name = specialities.require_subject_1"""

                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                sql += "\nAND specialities.code = (?)"
                container.append(self.SpecialtiesCB.currentText().split(' ')[0])

                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name in self.cur:
                    self.FirstSubjectCB.addItem(name[0])
                container.clear()
            
            if not self.SecondSubjectCB.currentIndex():
                self.SecondSubjectCB.clear()
                self.SecondSubjectCB.addItem('----Выберите предмет-----')
                sql = """SELECT subjects.name
                        FROM universities, faculties, specialities, subjects
                        WHERE universities.code = faculties.belong_to_university
                        AND universities.code = specialities.belong_to_university
                        AND specialities.belong_to_faculty = faculties.name
                        AND specialities.belong_to_university = faculties.belong_to_university
                        AND subjects.name = specialities.require_subject_2"""
                
                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                sql += "\nAND specialities.code = (?)"
                container.append(self.SpecialtiesCB.currentText().split(' ')[0])

                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())
                
                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, container)
                for name in self.cur:
                    self.SecondSubjectCB.addItem(name[0])
                container.clear()
            del container 
    
    @QtCore.pyqtSlot(int)
    def FirstSubjectCB_Change(self):
        if self.FirstSubjectCB.currentIndex() == 0:
            self.setSpecialities()
            self.setFaculties()
            self.setUniversities()
            self.setSubjects()
        else:
            container = []
            if not self.UniversitiesCB.currentIndex():
                self.UniversitiesCB.clear()
                self.UniversitiesCB.addItem('----Выберите университет-----')
                sql ="""SELECT universities.name, universities.code
                        FROM universities, faculties, specialities
                        WHERE universities.code = faculties.belong_to_university
                        AND specialities.belong_to_university = universities.code
                        AND faculties.name = """

                if self.FacultiesCB.currentIndex():
                    sql += '(?)'
                    container.append(self.FacultiesCB.currentText())
                else:
                    sql += 'faculties.name'

                sql += "\nAND specialities.code = "
                if self.SpecialtiesCB.currentIndex():
                    sql += '(?)'
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])
                else:
                    sql += 'specialities.code'

                sql += "\nAND specialities.belong_to_faculty = "
                if self.FacultiesCB.currentIndex():
                    sql += '(?)'
                    container.append(self.FacultiesCB.currentText())
                else:
                    sql += 'faculties.name'
                
                sql += "\nAND specialities.require_subject_1 = (?)"
                container.append(self.FirstSubjectCB.currentText())

                sql += "\nAND specialities.require_subject_2 = "
                if self.SecondSubjectCB.currentIndex():
                    sql += '(?)'
                    container.append(self.SecondSubjectCB.currentText())
                else:
                    sql += 'specialities.require_subject_2'

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')
                
                self.cur.execute(sql, tuple(container))
                for name, code in self.cur:
                    self.UniversitiesCB.addItem('{0} - {1}'.format(code, name))
                container.clear()
            
            if not self.FacultiesCB.currentIndex():
                self.FacultiesCB.clear()
                self.FacultiesCB.addItem('----Выберите факультет-----')
                sql = """SELECT faculties.name
                        FROM universities, faculties, specialities
                        WHERE faculties.name = specialities.belong_to_faculty
                        AND specialities.belong_to_university = faculties.belong_to_university
                        AND specialities.belong_to_university = universities.code
                        AND faculties.belong_to_university = universities.code"""
                
                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])
                
                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])

                sql += "\nAND specialities.require_subject_1 = (?)"
                container.append(self.FirstSubjectCB.currentText())

                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))

                for name in self.cur:
                    self.FacultiesCB.addItem(name[0])

                container.clear()
            
            if not self.SpecialtiesCB.currentIndex():
                self.SpecialtiesCB.clear()
                self.SpecialtiesCB.addItem('----Выберите специальность------')
                sql = """SELECT specialities.name, specialities.code
                         FROM universities, faculties, specialities
                         WHERE specialities.belong_to_faculty = faculties.name
                         AND specialities.belong_to_university = faculties.belong_to_university
                         AND specialities.belong_to_university = universities.code
                         AND faculties.belong_to_university = universities.code""" 
                
                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                sql += "\nAND specialities.require_subject_1 = (?)"
                container.append(self.FirstSubjectCB.currentText())

                if self.SecondSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_2 = (?)"
                    container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))

                for name, code in self.cur:
                    self.SpecialtiesCB.addItem('{0} - {1}'.format(code, name))
                container.clear()

            if not self.SecondSubjectCB.currentIndex():
                self.SecondSubjectCB.clear()
                self.SecondSubjectCB.addItem('----Выберите предмет-----')
                sql = """SELECT subjects.name
                         FROM universities, faculties, specialities, subjects
                         WHERE faculties.belong_to_university = universities.code
                         AND faculties.belong_to_university = specialities.belong_to_university
                         AND specialities.belong_to_university = universities.code
                         AND specialities.belong_to_faculty = faculties.name
                         AND subjects.name = specialities.require_subject_2"""
                
                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])

                sql += "\nAND specialities.require_subject_1 = (?)"
                container.append(self.FirstSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))

                for name in self.cur:
                    self.SecondSubjectCB.addItem(name[0])
                container.clear()           
            del container

    @QtCore.pyqtSlot(int)
    def SecondSubjectCB_Change(self):
        if self.SecondSubjectCB.currentIndex() == 0:
            self.setSpecialities()
            self.setFaculties()
            self.setUniversities()
            self.setSubjects()
        else:
            container = []
            if not self.UniversitiesCB.currentIndex():
                self.UniversitiesCB.clear()
                self.UniversitiesCB.addItem('----Выберите университет-----')
                sql ="""SELECT universities.name, universities.code
                        FROM universities, faculties, specialities
                        WHERE universities.code = faculties.belong_to_university
                        AND specialities.belong_to_university = universities.code"""
                
                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())
                
                if self.SpecialtiesCB.currentIndex(): 
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])
                
                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())
                
                sql += "\nAND specialities.require_subject_2 = (?)"
                container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))
                for name, code in self.cur:
                    self.UniversitiesCB.addItem('{0} - {1}'.format(code, name))
                container.clear()

            if not self.FacultiesCB.currentIndex():
                self.FacultiesCB.clear()
                self.FacultiesCB.addItem('----Выберите факультет-----')
                sql = """SELECT faculties.name
                        FROM universities, faculties, specialities
                        WHERE faculties.name = specialities.belong_to_faculty
                        AND specialities.belong_to_university = faculties.belong_to_university
                        AND specialities.belong_to_university = universities.code
                        AND faculties.belong_to_university = universities.code"""
                
                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])
                
                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])
                
                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())

                sql += "\nAND specialities.require_subject_2 = (?)"
                container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))
                for name in self.cur:
                    self.FacultiesCB.addItem(name[0])
                container.clear()
            
            if not self.SpecialtiesCB.currentIndex():
                self.SpecialtiesCB.clear()
                self.SpecialtiesCB.addItem('----Выберите специальность------')
                sql = """SELECT specialities.name, specialities.code
                         FROM universities, faculties, specialities
                         WHERE specialities.belong_to_faculty = faculties.name
                         AND specialities.belong_to_university = faculties.belong_to_university
                         AND specialities.belong_to_university = universities.code
                         AND faculties.belong_to_university = universities.code""" 
                
                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                if self.FirstSubjectCB.currentIndex():
                    sql += "\nAND specialities.require_subject_1 = (?)"
                    container.append(self.FirstSubjectCB.currentText())

                sql += "\nAND specialities.require_subject_2 = (?)"
                container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))
                for name, code in self.cur:
                    self.SpecialtiesCB.addItem('{0} - {1}'.format(code, name))
                container.clear()

            if not self.FirstSubjectCB.currentIndex():
                self.FirstSubjectCB.clear()
                self.FirstSubjectCB.addItem('----Выберите предмет-----')
                sql = """SELECT subjects.name
                         FROM universities, faculties, specialities, subjects
                         WHERE faculties.belong_to_university = universities.code
                         AND faculties.belong_to_university = specialities.belong_to_university
                         AND specialities.belong_to_university = universities.code
                         AND specialities.belong_to_faculty = faculties.name
                         AND subjects.name = specialities.require_subject_1"""

                if self.UniversitiesCB.currentIndex():
                    sql += "\nAND universities.code = (?)"
                    container.append(self.UniversitiesCB.currentText().split(' ')[0])

                if self.FacultiesCB.currentIndex():
                    sql += "\nAND faculties.name = (?)"
                    container.append(self.FacultiesCB.currentText())

                if self.SpecialtiesCB.currentIndex():
                    sql += "\nAND specialities.code = (?)"
                    container.append(self.SpecialtiesCB.currentText().split(' ')[0])

                sql += "\nAND specialities.require_subject_2 = (?)"
                container.append(self.SecondSubjectCB.currentText())

                sql += "\nAND specialities.language_group = (?)"
                container.append('русская' if self.action.isChecked() else 'казахская')

                self.cur.execute(sql, tuple(container))
                for name in self.cur:
                    self.FirstSubjectCB.addItem(name[0])
                container.clear()
            del container

    @QtCore.pyqtSlot(bool)
    def actionChanged(self):
        self.action.setChecked(True)
        self.action_2.setChecked(False)
        self.changeSpecialities()

    @QtCore.pyqtSlot(bool)
    def action_2Changed(self):
        self.action_2.setChecked(True)
        self.action.setChecked(False)
        self.changeSpecialities()

    @QtCore.pyqtSlot()
    def search(self):
        '''
        Show new window to display an appropriate university, faculty, specialty and chance of getting grand.
        Input: nothing
        Return: nothing 
        '''
        print(not self.ScoreLE.text() or not self.ScoreLE.text().isdigit())
        print(not self.ScoreLE.text())
        print(not self.ScoreLE.text().isdigit())
        if not self.ScoreLE.text() or not self.ScoreLE.text().isdigit():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Не был коррекно введено количество баллов")
            return  
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
