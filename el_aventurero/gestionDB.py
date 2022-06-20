import sqlite3
import traceback

class GestionDB: 
    def abrir(self):
        conexion = sqlite3.connect("el_aventurero/game01.db")
        return conexion

    def executeFromFile(self, filename):
        con = self.abrir()
        cursor = con.cursor()
        fd = open(filename, "r")
        sqlFile = fd.read()
        fd.close()

        sqlCommands = sqlFile.split("#")

        for command in sqlCommands:
            try:
                cursor.execute(command)
                #print(command)
            except sqlite3.OperationalError:
                traceback.print_exc()
                #print("Command skipped")
        con.commit()
        con.close()

    def createDB(self):
        con = self.abrir()
        self.executeFromFile("el_aventurero/sql.sql")
        #print("comando ejecutado")
        con.commit()
        con.close()
    
    def partidaNueva(self, nombre):
        con = self.abrir()
        cursor = con.cursor()
        datos = [nombre,25,25,1,5,1,2,2,2,5,5,10,10,"el_aventurero/img/casco1.png","el_aventurero/img/armadura1.png","el_aventurero/img/arma1.png"]
        sql = "INSERT INTO data (nombre, stat_vida_max, stat_vida, stat_arm, stat_dmg, enemy_lvl, rotacion_arma, rotacion_casco, rotacion_armadura, aumento_dmg, aumento_casco, aumento_armadura, aumento_vida, img_casco, img_armadura, img_arma) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        cursor.execute(sql, datos)
        con.commit()
        con.close()
    
    def recogerNombres(self):
        con = self.abrir()
        cursor = con.cursor()
        sql = "SELECT nombre FROM data"
        cursor.execute(sql)
        return cursor.fetchall()
    
    def recogerDatos(self, nombre):
        con = self.abrir()
        cursor = con.cursor()
        sql = "SELECT * FROM data WHERE nombre=?"
        cursor.execute(sql, (nombre, ))
        return cursor.fetchall()
    
    def guardarPartida(self, datos):
        con = self.abrir()
        cursor = con.cursor()
        sql = "UPDATE data SET stat_vida_max=?, stat_vida=?, stat_arm=?, stat_dmg=?, enemy_lvl=?, rotacion_arma=?, rotacion_casco=?, rotacion_armadura=?, aumento_dmg=?, aumento_casco=?, aumento_armadura=?, aumento_vida=?, img_casco=?, img_armadura=?, img_arma=? WHERE nombre=?"
        cursor.execute(sql, datos)
        con.commit()
        con.close()

