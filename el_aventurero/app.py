from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from PIL import Image, ImageTk
from random import randint
from sqlite3 import IntegrityError
import traceback

from gestionDB import GestionDB

class AplicacionJuego():

    def __init__(self):
        self.main = Tk()
        self.main.title("El aventurero")

        self.gestor = GestionDB()
        self.gestor.createDB()

        self.TITULO = "EL AVENTURERO"
        self.PAD = 15

        #datos cogidos de la base de datos
        self.nombreJugador = StringVar()
        self.vidaMaxPj = 0
        self.vidaPj = 0
        self.armPj = 0
        self.dmgPj = 0
        self.nivelEnemigo = 0
        self.imgCascoPj = StringVar()
        self.imgArmaduraPj = StringVar()
        self.imgArmaPj = StringVar()

        #datos calculados con el nivel del enemigo
        self.vidaEnemigoMax = 10
        self.vidaEnemigo = 10
        self.armaduraEnemigo = 1
        self.dmgEnemigo = 5

        #rotaciones de objetos
        self.rotacionArma = 2
        self.rotacionArmadura = 2
        self.rotacionCasco = 2

        #rotaciones máximas de los objetos (dependiendo de la cantidad de imagénes que haya)
        self.MAX_ROTATION_ARMA = 4
        self.MAX_ROTATION_CASCO = 4
        self.MAX_ROTATION_ARMADURA = 4
        
        #aumentos de stat
        self.aumento_danno = 5
        self.aumento_casco = 5
        self.aumento_armadura = 10
        self.aumento_vida = 10

        #opciones juego
        self.PIEDRA = "piedra"
        self.PAPEL = "papel"
        self.TIJERA = "tijera"
        self.primerTurno = True
        self.EMPATE = "Empate"
        self.GANADOR = "Ganador"
        self.PERDEDOR = "Perdedor"

        self.AMARILLO = "#FFFF00"
        self.VERDE = "#00FF00"
        self.ROJO = "#FF0000"
        self.AZUL = "#0000FF"

        self.cargaVetana()
        self.main.mainloop()
    
    def cargaVetana(self):
        self.lbTitulo = Label(self.main, text=self.TITULO)
        self.lbTitulo.pack(side="top", padx=self.PAD, pady=30)

        self.lbNueva = Label(self.main, text="Partida nueva\nIntroduce el nombre")
        self.lbNueva.pack(padx=self.PAD)
        self.nombre = StringVar()
        self.entryNombre = Entry(self.main, textvariable=self.nombre)
        self.entryNombre.pack(padx=self.PAD)
        self.btnNueva = Button(self.main, text="Partida Nueva", command=self.nueva)
        self.btnNueva.pack(padx=self.PAD, pady=self.PAD)

        self.lbcb = Label(self.main, text="Selecciona la partida")
        self.lbcb.pack(padx=self.PAD)
        self.cbPartidas = ttk.Combobox(self.main, values=self.gestor.recogerNombres())
        self.cbPartidas.pack(padx=self.PAD)

        self.btnJugar = Button(self.main, text="Jugar", command=self.jugar)
        self.btnJugar.pack(padx=self.PAD, pady=self.PAD)
    
    def jugar(self):
        #cargar los datos de la partida con el nombre del combobox
        if self.cbPartidas.get()!="":
            self.nombreJugador = self.cbPartidas.get()  
            self.crearVentanaJuego()
        else:
            messagebox.showwarning("Error", "Selecciona una partida.")

    def nueva(self):
        name = self.nombre.get()
        try:
            if(name!=""):
                if(messagebox.askyesno("Confirmación", "¿Quieres que el nombre sea ["+name+"] ?")):
                    self.gestor.partidaNueva(name)
                    
                    self.nombreJugador.set(name)
                    self.nombre.set("")
                    #abrir la ventana de juego
                    self.crearVentanaJuego()
            else:
                messagebox.showwarning("Campo vacío", "Provafor, intoduce un nombre.")
        except IntegrityError:
            messagebox.showwarning("Nombre ya cogido", "El nombre seleccionado ya está cogido.")
            traceback.print_exc()
        except Exception:
            messagebox.showerror("Error", "Ha ocurrido un error, pruebe de nuevo.")
            traceback.print_exc()
    
    def crearVentanaJuego(self):
        self.ventana = Toplevel()
        self.canvas = Canvas(self.ventana, bg=self.ROJO)

        #nombrePJ
        self.lbJugador = Label(self.canvas, text=self.nombreJugador)
        self.lbJugador.grid(row=0, column=3, columnspan=3)

        #vidaPj
        imgVidaPj = ImageTk.PhotoImage(Image.open("el_aventurero/img/vidaPj.png"))
        self.lbVidaPj = Label(self.canvas, text=self.vidaPj, image=imgVidaPj, compound="center")
        self.lbVidaPj.image = imgVidaPj #por algún motivo, esta línea es esencial, aunque parece que está mal.
        self.lbVidaPj.configure(image=imgVidaPj)
        self.lbVidaPj.grid(row=0, column=0)
        
        #armaduraPj
        imgArmaduraPj = ImageTk.PhotoImage(Image.open("el_aventurero/img/armaduraPj.png"))
        self.lbArmPj = Label(self.canvas, text=self.armPj, image=imgArmaduraPj, compound="center")
        self.lbArmPj.image = imgArmaduraPj
        self.lbArmPj.configure(image=imgArmaduraPj)
        self.lbArmPj.grid(row=0, column=1)

        #dmgPj
        imgDmgPj = ImageTk.PhotoImage(Image.open("el_aventurero/img/dmgPj.png"))
        self.lbDmgPj = Label(self.canvas, text=self.dmgPj, compound="center")
        self.lbDmgPj.image = imgDmgPj
        self.lbDmgPj.configure(image=imgDmgPj)
        self.lbDmgPj.grid(row=0, column=2)

        #imgPj
        imgPj = ImageTk.PhotoImage(Image.open("el_aventurero/img/pj.png"))
        self.lbPj = Label(self.canvas)
        self.lbPj.image = imgPj
        self.lbPj.configure(image=imgPj)
        self.lbPj.grid(row=1, column=1, columnspan=2, rowspan= 3)

        #imgCascoPj
        imgCascoPj = ImageTk.PhotoImage(Image.open("el_aventurero/img/casco1.png"))
        self.lbCascoPj = Label(self.canvas)
        self.lbCascoPj.image = imgCascoPj
        self.lbCascoPj.configure(image=imgCascoPj)
        self.lbCascoPj.grid(row=1, column=0)

        #imgArmaduraPj
        imgArmaduraPj = ImageTk.PhotoImage(Image.open("el_aventurero/img/armadura1.png"))
        self.lbArmaduraPj = Label(self.canvas)
        self.lbArmaduraPj.image = imgArmaduraPj
        self.lbArmaduraPj.configure(image=imgArmaduraPj)
        self.lbArmaduraPj.grid(row=2, column=0)

        #imgArmaPj
        imgArmaPj = ImageTk.PhotoImage(Image.open("el_aventurero/img/arma1.png"))
        self.lbArmaPj = Label(self.canvas)
        self.lbArmaPj.image = imgArmaPj
        self.lbArmaPj.configure(image=imgArmaPj)
        self.lbArmaPj.grid(row=3, column=0)

        #btnGuardar
        self.btnGuardar = Button(self.canvas, text="Guardar y salir", command=self.guardar)
        self.btnGuardar.grid(row=0,column=6)

        #notebook
        self.notebook = ttk.Notebook(self.canvas)
        self.tab1 = Label(self.notebook)
        self.notebook.add(self.tab1, text="Enemigo")
        self.tab2 = Label(self.notebook)
        self.notebook.add(self.tab2, text="Arma")
        self.tab3 = Label(self.notebook)
        self.notebook.add(self.tab3, text="Armadura")
        self.tab4 = Label(self.notebook)
        self.notebook.add(self.tab4, text="Poción de Vida")
        
        #pestaña enemigo
        #vidaEnemigo
        imgVidaEnemigo = ImageTk.PhotoImage(Image.open("el_aventurero/img/vidaEnemigo.png"))
        self.lbVidaEnemigo = Label(self.tab1, text=self.vidaEnemigo, compound="center")
        self.lbVidaEnemigo.image = imgVidaEnemigo
        self.lbVidaEnemigo.configure(image=imgVidaEnemigo)
        self.lbVidaEnemigo.grid(row=0, column=0)
        #armaduraEnemigo
        imgArmaduraEnemigo = ImageTk.PhotoImage(Image.open("el_aventurero/img/armaduraEnemigo.png"))
        self.lbArmaduraEnemigo = Label(self.tab1, text=self.armaduraEnemigo, compound="center")
        self.lbArmaduraEnemigo.image = imgArmaduraEnemigo
        self.lbArmaduraEnemigo.configure(image=imgArmaduraEnemigo)
        self.lbArmaduraEnemigo.grid(row=0, column=1)
        #dmgEnemigo
        imgDmgEnemigo = ImageTk.PhotoImage(Image.open("el_aventurero/img/dmgEnemigo.png"))
        self.lbDmgEnemigo = Label(self.tab1, text=self.dmgEnemigo, compound="center")
        self.lbDmgEnemigo.image = imgDmgEnemigo
        self.lbDmgEnemigo.configure(image=imgDmgEnemigo)
        self.lbDmgEnemigo.grid(row=0, column=2)
        #img enemigo
        imgEnemigo = ImageTk.PhotoImage(Image.open("el_aventurero/img/enemigo1.png"))
        self.lbEnemigo = Label(self.tab1)
        self.lbEnemigo.image = imgEnemigo
        self.lbEnemigo.configure(image=imgEnemigo)
        self.lbEnemigo.grid(row=1, column=0, rowspan=3, columnspan=3)
        #btn combate
        self.btnCombate = Button(self.tab1, text="Combate", command=self.crearVentanaPartida)
        self.btnCombate.grid(row=2, column=4)

        #pestaña arma
        self.lbaram = Label(self.tab2)
        self.lbaram.pack()

        self.btnCogerArma = Button(self.tab2, text="Coger arma", command=self.cogerArma)
        self.btnCogerArma.pack()

        #pestaña armadura
        self.lbarmadura = Label(self.tab3)
        self.lbarmadura.pack()

        self.btnCogerArmadura = Button(self.tab3, text="Coger pieza de armadura", command=self.cogerArmadura)
        self.btnCogerArmadura.pack()

        #pestaña poción
        self.lbpocion = Label(self.tab4)
        self.imgPocion = ImageTk.PhotoImage(Image.open("el_aventurero/img/pocion.png"))
        self.lbpocion.image = self.imgPocion
        self.lbpocion.configure(image=self.imgPocion)
        self.lbpocion.pack()

        self.btnPocion = Button(self.tab4, text="Beber poción de vida", command=self.cogerPocion)
        self.btnPocion.pack()
        

        self.notebook.grid(row=1, column=4, columnspan=3, rowspan= 3)
        self.canvas.pack()

        self.cargarDatos()
        self.actualizarImagenes()
    
    def cargarDatos(self):
        datos = self.gestor.recogerDatos(str(self.nombreJugador))
        print(datos)
        for d in datos:
            self.nombreJugador = d[0]
            self.vidaMaxPj = d[1]
            self.vidaPj = d[2]
            self.armPj = d[3]
            self.dmgPj = d[4]
            self.nivelEnemigo = d[5]
            self.rotacionArma = d[6]
            self.rotacionCasco = d[7]
            self.rotacionArmadura = d[8]
            self.aumento_danno = d[9]
            self.aumento_casco = d[10]
            self.aumento_armadura = d[11]
            self.aumento_vida = d[12]
            self.imgCascoPj = d[13]
            self.imgArmaduraPj = d[14]
            self.imgArmaPj = d[15]

        self.calcularStatsEnemigo()
    
    def calcularSecundario(self):
        num = randint(1, 100)
        resul = 0
        if(num<60):
            resul = 1 #enemigo
        elif(num>60 and num<75):
            resul = 2 #arma
        elif(num>75 and num<90):
            resul = 3 #armadura
        else:
            resul = 4 #poción de vida
        return resul
            
    def siguienteRotacion(self):
        num = self.calcularSecundario()
        if num==1:
            #enemigo
            stats = self.calcularStatsEnemigo()
            self.lbVidaEnemigo.configure(text=stats[0])
            self.lbArmaduraEnemigo.configure(text=stats[1])
            self.lbDmgEnemigo.configure(text=stats[2])
            self.nivelEnemigo+=1
            
            self.notebook.select(0)
        elif num==2:
            #arma
            if self.rotacionArma<=self.MAX_ROTATION_ARMA:
                self.imgArma = ImageTk.PhotoImage(Image.open("el_aventurero/img/arma"+str(self.rotacionArma)+".png"))
                self.lbaram.image = self.imgArma
                self.lbaram.configure(image=self.imgArma)
            else:
                self.imgArma = ImageTk.PhotoImage(Image.open("el_aventurero/img/arma4.png"))
                self.lbaram.image = self.imgArma
                self.lbaram.configure(image=self.imgArma)
            
            self.btnCogerArma["state"] = ACTIVE
            self.notebook.select(1)
        elif num==3:
            #armadura
            self.numArmadura = randint(1, 100)
            if self.numArmadura<50:
                #casco
                if self.rotacionCasco<=self.MAX_ROTATION_CASCO:    
                    self.imgCasco = ImageTk.PhotoImage(Image.open("el_aventurero/img/casco"+str(self.rotacionCasco)+".png"))
                    self.lbarmadura.image = self.imgCasco
                    self.lbarmadura.configure(image = self.imgCasco)
                else:
                    self.imgCasco = ImageTk.PhotoImage(Image.open("el_aventurero/img/casco4.png"))
                    self.lbarmadura.image = self.imgCasco
                    self.lbarmadura.configure(image = self.imgCasco)
            elif self.numArmadura>50:
                #armadura
                if self.rotacionArmadura<=self.MAX_ROTATION_ARMADURA:
                    self.imgArmadura = ImageTk.PhotoImage(Image.open("el_aventurero/img/armadura"+str(self.rotacionArmadura)+".png"))
                    self.lbarmadura.image = self.imgArmadura
                    self.lbarmadura.configure(image=self.imgArmadura)
                else:
                    self.imgArmadura = ImageTk.PhotoImage(Image.open("el_aventurero/img/armadura4.png"))
                    self.lbarmadura.image = self.imgArmadura
                    self.lbarmadura.configure(image=self.imgArmadura)

            self.btnCogerArmadura["state"] = ACTIVE
            self.notebook.select(2)
        elif num==4:
            #poción de vida
            self.notebook.select(3)
    
    def calcularStatsEnemigo(self):
        self.vidaEnemigoMax = self.nivelEnemigo * 3
        self.vidaEnemigo = self.vidaEnemigoMax
        self.armaduraEnemigo = self.nivelEnemigo * 2
        self.dmgEnemigo = self.nivelEnemigo * 2
        stats = [self.vidaEnemigoMax, self.armaduraEnemigo, self.dmgEnemigo]
        return stats

    def cogerArma(self):
        self.lbArmaPj.image = self.imgArma
        self.lbArmaPj.configure(image=self.imgArma)
        self.dmgPj += self.aumento_danno
        self.aumento_danno += 5
        if self.rotacionArma <= self.MAX_ROTATION_ARMA:
            self.imgArmaPj = "el_aventurero/img/arma"+str(self.rotacionArma)+".png"
            self.rotacionArma += 1
        self.lbDmgPj.configure(text=str(self.dmgPj))
        self.btnCogerArma["state"] = DISABLED
        self.siguienteRotacion()

    def cogerArmadura(self):
        if (self.numArmadura<50):
            #casco
            self.lbCascoPj.image = self.imgCasco
            self.lbCascoPj.configure(image=self.imgCasco)
            self.armPj += self.aumento_casco
            self.aumento_casco += 5
            if self.rotacionCasco <= self.MAX_ROTATION_CASCO:
                self.imgCascoPj = "el_aventurero/img/casco"+str(self.rotacionCasco)+".png"
                self.rotacionCasco += 1
        else:
            #armadura
            self.lbArmaduraPj.image = self.imgArmadura
            self.lbArmaduraPj.configure(image=self.imgArmadura)           
            self.armPj += self.aumento_armadura
            self.aumento_armadura += 10
            if self.rotacionArmadura <= self.MAX_ROTATION_ARMADURA:
                self.imgArmaduraPj = "el_aventurero/img/armadura"+str(self.rotacionArmadura)+".png"
                self.rotacionArmadura += 1
        
        self.lbArmPj.configure(text=str(self.armPj))
        self.btnCogerArmadura["state"] = DISABLED
        self.siguienteRotacion()
    
    def cogerPocion(self):
        self.vidaMaxPj += self.aumento_vida
        self.aumento_vida += 11
        self.vidaPj = self.vidaMaxPj
        self.lbVidaPj.configure(text=str(self.vidaPj))
        self.siguienteRotacion()
    
    def guardar(self):
        datos = [
            self.vidaMaxPj, 
            self.vidaPj,
            self.armPj,
            self.dmgPj,
            self.nivelEnemigo,
            self.rotacionArma,
            self.rotacionCasco,
            self.rotacionArmadura,
            self.aumento_danno,
            self.aumento_casco,
            self.aumento_armadura,
            self.aumento_armadura,
            self.imgCascoPj,
            self.imgArmaduraPj,
            self.imgArmaPj,
            self.nombreJugador
        ]
        print(datos)
        self.gestor.guardarPartida(datos)

    def actualizarImagenes(self):
        imgCasco = ImageTk.PhotoImage(Image.open(self.imgCascoPj))
        self.lbCascoPj.image = imgCasco
        self.lbCascoPj.configure(image=imgCasco)

        imgArmadura = ImageTk.PhotoImage(Image.open(self.imgArmaduraPj))
        self.lbArmaduraPj.image = imgArmadura
        self.lbArmaduraPj.configure(image=imgArmadura)
        
        imgArma = ImageTk.PhotoImage(Image.open(self.imgArmaPj))
        self.lbArmaPj.image = imgArma
        self.lbArmaPj.configure(image=imgArma)
    
    def crearVentanaPartida(self):
        self.juego = Toplevel()
        self.canvasJuego = Canvas(self.juego, bg=self.AZUL)

        self.juego.protocol("WM_DELETE_WINDOW", self.cerrandoJuego)

        #vida pj
        self.lbNombrePjJuego = Label(self.canvasJuego, text=self.nombreJugador)
        self.lbNombrePjJuego.grid(row=0, column=0, columnspan=2)

        self.progressBarVidaPj = ttk.Progressbar(self.canvasJuego, length=200)
        self.progressBarVidaPj.grid(row=1, column=0)

        #label vida pj
        self.vidaPjText = StringVar()
        self.lbVidaPjJuego = Label(self.canvasJuego, text=self.vidaPjText)
        self.lbVidaPjJuego.grid(row=2, column=0)

        #armadura pj
        self.armaduraTempPj = self.armPj
        self.progressBarArmaduraPj = ttk.Progressbar(self.canvasJuego, length=200)
        self.progressBarArmaduraPj.grid(row=3, column=0)

        #label armadura pj
        self.armPjText = StringVar()
        self.lbArmaduraPjJuego = Label(self.canvasJuego, text=self.armPjText)
        self.lbArmaduraPjJuego.grid(row=4, column=0)

        #vida enemigo
        lbnombreenemigo = Label(self.canvasJuego, text="Enemigo").grid(row=0, column=1)
        self.progressBarVidaEnemgio = ttk.Progressbar(self.canvasJuego, length=200)
        self.progressBarVidaEnemgio.grid(row=1, column=1)

        #label vida enemigo
        self.vidaEnemigoText = StringVar()
        self.lbVidaEnemigoJuego = Label(self.canvasJuego, text=self.vidaEnemigoText)
        self.lbVidaEnemigoJuego.grid(row=2, column=1)

        #armadura enemigo
        self.armaduraTempEnemigo = self.armaduraEnemigo
        self.progressBarArmaduraEnemigo = ttk.Progressbar(self.canvasJuego, length=200)
        self.progressBarArmaduraEnemigo.grid(row=3, column=1)

        #label armadura enemigo
        self.armaduraEnemigoText = StringVar()
        self.lbArmaduraEnemigoJuego = Label(self.canvasJuego, text=self.armaduraEnemigoText)
        self.lbArmaduraEnemigoJuego.grid(row=4, column=1)

        #opciones de juego (ppt)
        self.canvasOpciones = Canvas(self.canvasJuego)
        self.canvasOpciones.grid(row=5, column=0, columnspan=2, padx=self.PAD, pady=self.PAD)

        self.opcion = StringVar()

        imgPiedra = ImageTk.PhotoImage(Image.open("el_aventurero/img/piedra.png"))
        self.btnPiedra = Button(self.canvasOpciones, image = imgPiedra, command=self.accionPiedra)
        self.btnPiedra.image = imgPiedra
        self.btnPiedra.configure(image=imgPiedra)
        self.btnPiedra.grid(row=0, column=0)

        imgPapel = ImageTk.PhotoImage(Image.open("el_aventurero/img/papel.png"))
        self.btnPapel = Button(self.canvasOpciones, image = imgPapel, command=self.accionPapel)
        self.btnPapel.image = imgPapel
        self.btnPapel.configure(image=imgPapel)
        self.btnPapel.grid(row=0, column=1)

        imgTijera = ImageTk.PhotoImage(Image.open("el_aventurero/img/tijera.png"))
        self.btnTijera = Button(self.canvasOpciones, image = imgTijera, command=self.accionTijera)
        self.btnTijera.image = imgTijera
        self.btnTijera.configure(image=imgTijera)
        self.btnTijera.grid(row=0, column=2)

        #resultados
        columns = ("resultado", "pj", "enemigo")
        self.treeResultados = ttk.Treeview(self.canvasJuego, columns=columns, show="headings")
        self.treeResultados.heading("resultado", text="Resultado")
        self.treeResultados.heading("pj", text=self.nombreJugador)
        self.treeResultados.heading("enemigo", text="Enemigo")

        self.treeResultados.tag_configure(self.EMPATE, background=self.AMARILLO)
        self.treeResultados.tag_configure(self.GANADOR, background=self.VERDE)
        self.treeResultados.tag_configure(self.PERDEDOR, background=self.ROJO)

        self.treeResultados.grid(row=6, column=0, columnspan=2, padx=self.PAD, pady=self.PAD)

        self.canvasJuego.grid(row=0, column=0)
        self.actualizarBarras()
    
    def actualizarBarras(self):
        #vida
        self.progressBarVidaPj["value"] = self.numToPercentage(self.vidaPj, self.vidaMaxPj)
        self.progressBarVidaEnemgio["value"] = self.numToPercentage(self.vidaEnemigo, self.vidaEnemigoMax)

        self.vidaPjText = "[ "+str(self.vidaPj)+" / "+str(self.vidaMaxPj)+" ]"
        self.vidaEnemigoText = "[ "+str(self.vidaEnemigo)+" / "+str(self.vidaEnemigoMax)+" ]"

        self.lbVidaPjJuego.configure(text=self.vidaPjText)
        self.lbVidaEnemigoJuego.configure(text=self.vidaEnemigoText)

        #armadura
        self.progressBarArmaduraPj["value"] = self.numToPercentage(self.armaduraTempPj, self.armPj)
        self.progressBarArmaduraEnemigo["value"] = self.numToPercentage(self.armaduraTempEnemigo, self.armaduraEnemigo)

        self.armPjText = "[ "+str(self.armaduraTempPj)+" / "+str(self.armPj)+" ]"
        self.armaduraEnemigoText = "[ "+str(self.armaduraTempEnemigo)+" / "+str(self.armaduraEnemigo)+" ]"

        self.lbArmaduraPjJuego.configure(text=self.armPjText)
        self.lbArmaduraEnemigoJuego.configure(text=self.armaduraEnemigoText)

    def numToPercentage(self, num, max):
        return int(num*100/max)
    
    def accionPiedra(self):
        self.opcionAnterior = self.opcion
        self.opcion = self.PIEDRA
        self.btnPiedra["state"]=DISABLED
        self.btnPapel["state"]=DISABLED
        self.btnTijera["state"]=DISABLED
        self.calcularJuego()
    
    def accionPapel(self):
        self.opcionAnterior = self.opcion
        self.opcion = self.PAPEL
        self.btnPiedra["state"]=DISABLED
        self.btnPapel["state"]=DISABLED
        self.btnTijera["state"]=DISABLED
        self.calcularJuego()
    
    def accionTijera(self):
        self.opcionAnterior = self.opcion
        self.opcion = self.TIJERA
        self.btnPiedra["state"]=DISABLED
        self.btnPapel["state"]=DISABLED
        self.btnTijera["state"]=DISABLED
        self.calcularJuego()
    
    def calcularJuego(self):
        self.opcionEnemigo = self.calcularOpcionEnemigo()
        self.primerTurno = False

        if self.opcion == self.opcionEnemigo:
        #empate
            self.treeResultados.insert("", 0, values=(self.EMPATE, self.opcion, self.opcionEnemigo), tags=(self.EMPATE, ))
        elif self.opcion == self.PIEDRA and self.opcionEnemigo == self.TIJERA or self.opcion == self.PAPEL and self.opcionEnemigo == self.PIEDRA or self.opcion == self.TIJERA and self.opcionEnemigo == self.PAPEL:
        #gana pj
            self.treeResultados.insert("", 0, values=(self.GANADOR, self.opcion, self.opcionEnemigo), tags=(self.GANADOR, ))
            if self.armaduraTempEnemigo > 0:
                self.armaduraTempEnemigo -= self.dmgPj
            else:
                self.vidaEnemigo -= self.dmgPj
            
        elif self.opcion == self.PIEDRA and self.opcionEnemigo == self.PAPEL or self.opcion == self.PAPEL and self.opcionEnemigo == self.TIJERA or self.opcion == self.TIJERA and self.opcionEnemigo == self.PIEDRA:
        #gana enemigo
            self.treeResultados.insert("", 0, values=(self.PERDEDOR, self.opcion, self.opcionEnemigo), tags=(self.PERDEDOR, ))
            if self.armaduraTempPj > 0:
                self.armaduraTempPj -= self.dmgEnemigo
            else:
                self.vidaPj -= self.dmgEnemigo
            
        self.actualizarBarras()
        self.btnPiedra["state"]=ACTIVE
        self.btnPapel["state"]=ACTIVE
        self.btnTijera["state"]=ACTIVE

        if(self.vidaEnemigo<=0):
            #enemigo muerto
            self.cerrandoJuego()
    
    def calcularOpcionEnemigo(self):
        """if self.primerTurno:
            num = randint(1, 99)
            if num<33:
                return self.PIEDRA
            elif 33<num<66:
                return self.PAPEL
            elif num>66:
                return self.TIJERA
        else:
            self.opcionEnemigo = self.opcionAnterior"""
        
        num = randint(1, 99)
        if num<33:
            return self.PIEDRA
        elif 33<num<66:
            return self.PAPEL
        elif num>66:
            return self.TIJERA

    def cerrandoJuego(self):
        #messagebox.showinfo("Cerrando", "Se ha cerrando la ventana de juego")
        self.actualizarVidaJuego()
        self.siguienteRotacion()
        self.juego.destroy()

    def actualizarVidaJuego(self):
        self.lbVidaPj.configure(text=str(self.vidaPj))
        self.armPj = self.armaduraTempPj
        self.lbArmPj.configure(text=str(self.armPj))
    
app = AplicacionJuego()