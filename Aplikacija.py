from Tkinter import *
import tkMessageBox
import ttk
import datetime
import math
import os.path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkFileDialog
from PIL import ImageTk, Image

global datum
datum = datetime.date.today ()

osobni_podaci_lista = []
lista_mjerenja = []
lista_fit_test = []

class Osobni_Podaci:

    def __init__ (self, spol, dob, visina, tezina):

        self.spol = spol
        self.dob = dob
        self.visina = visina
        self.tezina = tezina
        
    @staticmethod
    def spremi_osobne_podatke (spol, dob, visina, tezina, ekran):
                           
        if spol != "nije_odabrano":

            if dob.isdigit () and visina.isdigit () and tezina.isdigit ():
                
                ekran.destroy ()
        
                datoteka = open ("osobni.txt", "a")
        
                datoteka_r = open ("osobni.txt", "r")
        
                sadrzaj_datoteke = datoteka_r.readlines ()
                lista_redaka = []
                for i in range (0, len (sadrzaj_datoteke) / 5):
                    lista_redaka = []
                    for j in range (i * 5, (i * 5) + 5):
                        lista_redaka.append (sadrzaj_datoteke [j])
        
                datoteka.write ("\n" + spol)
                datoteka.write ("\n" + dob)
                datoteka.write ("\n" + visina)
                datoteka.write ("\n" + tezina)
                datoteka.write ("\n")
        
                datoteka.close ()
                
                tkMessageBox.showinfo ("Uspjeh!", "Unos uspjesno spremljen!")
                kalorijski_zahtjevi ()
            else:
                tkMessageBox.showerror ("Greska!", "Unijeli ste slova!")
                ekran.lift ()
        else:
            tkMessageBox.showerror ("Greska!", "Niste odabrali spol!")
            ekran.lift ()
            
    @staticmethod        
    def unos_osobnih_podataka ():

        if not os.path.exists ("osobni.txt"):

            open ("osobni.txt", "a")

        if os.stat ("osobni.txt").st_size == 0:
            
            unos_osobnih_podataka_ekran = Toplevel ()
            Label (unos_osobnih_podataka_ekran, text = "Spol:").grid (row = 0, column = 0)
            spol = StringVar ()
            spol.set ("nije_odabrano") # OMOGUCAVAMO POKRETANJE PROZORA U KOJEM NIJEDAN RADIO BUTTON NIJE ODABRAN
            musko_odabir = Radiobutton (unos_osobnih_podataka_ekran, text = "Musko", variable = spol, value = "Musko")
            musko_odabir.grid (row = 0, column = 1, sticky = "W")
            zensko_odabir = Radiobutton (unos_osobnih_podataka_ekran, text = "Zensko", variable = spol, value = "Zensko")
            zensko_odabir.grid (row = 0, column = 1, sticky = "E")
            Label (unos_osobnih_podataka_ekran, text = "Dob:").grid (row = 1, column = 0)
            dob_unos = Entry (unos_osobnih_podataka_ekran)
            dob_unos.grid (row = 1, column = 1)
            Label (unos_osobnih_podataka_ekran, text = "Visina:").grid (row = 2, column = 0)
            visina_unos = Entry (unos_osobnih_podataka_ekran)
            visina_unos.grid (row = 2, column = 1)
            Label (unos_osobnih_podataka_ekran, text = "Tezina:").grid (row = 3, column = 0)
            tezina_unos = Entry (unos_osobnih_podataka_ekran)
            tezina_unos.grid (row = 3, column = 1)
            Button (unos_osobnih_podataka_ekran, text = "SPREMI UNOS", command = lambda: \
                    Osobni_Podaci.spremi_osobne_podatke (spol.get (), dob_unos.get(), visina_unos.get(),\
                                          tezina_unos.get(), unos_osobnih_podataka_ekran)\
                    ).grid (row = 4, column = 0)
            Button (unos_osobnih_podataka_ekran, text = "ODUSTANI", command = \
                    unos_osobnih_podataka_ekran.destroy).grid (row = 4, column = 1)
        else:
            tkMessageBox.showerror ("Greska!", "Vec postoji unos osobnih podataka! Za unos novih osobnih podataka pokrenite restart programa pomocu menija Opcije, te ponovno pokrenite aplikaciju!")
       
    @staticmethod            
    def ispis_osobnih_podataka ():

        postoji = os.path.exists ("osobni.txt")
    
        if not postoji:
            tkMessageBox.showerror ("Greska!", "Nema unesenih osobnih podataka!")
        else:
            osobni_podaci_lista = []
            
            nazivi_stupaca = ("spol", "dob", "visina", "tezina")
            tablica = ttk.Treeview (columns = nazivi_stupaca, show = "headings")
        
            datoteka_r = open ("osobni.txt", "r")
        
            sadrzaj_datoteke = datoteka_r.readlines ()
        
            for i in range (0, len (sadrzaj_datoteke) / 5):
                lista_redaka = []
                for j in range (i * 5, (i * 5) + 5):
                    lista_redaka.append (sadrzaj_datoteke [j])
                    
                podaci = Osobni_Podaci (lista_redaka [1], lista_redaka [2], lista_redaka [3], \
                                        lista_redaka [4])
                osobni_podaci_lista.append (podaci)
            
            tablica.column ("spol", width = 250)
            tablica.heading ("spol", text = "Spol")
            tablica.column ("dob", width = 250)
            tablica.heading ("dob", text = "Dob")
            tablica.column ("visina", width = 250)
            tablica.heading ("visina", text = "Visina")
            tablica.column ("tezina", width = 250)
            tablica.heading ("tezina", text = "Tezina")
        
            tablica.grid (column = 0, row = 0)
        
            for podaci in osobni_podaci_lista:
                tablica.insert ("", 'end', values = (podaci.spol, podaci.dob, podaci.visina, \
                                                 podaci.tezina))

class Mjerenje:

    def __init__ (self, r_br, datum, prsa, l_biceps, d_biceps, struk, bokovi, \
                  l_bedro, d_bedro, l_list, d_list, tezina):

        self.r_br = r_br
        self.datum = datum
        self.prsa = prsa
        self.l_biceps = l_biceps
        self.d_biceps = d_biceps
        self.struk = struk
        self.bokovi = bokovi
        self.l_bedro = l_bedro
        self.d_bedro = d_bedro
        self.l_list = l_list
        self.d_list = d_list
        self.tezina = tezina
    
    @staticmethod
    def spremi_mjerenje (r_br, datum, prsa, l_biceps, d_biceps, struk, bokovi, \
                     l_bedro, d_bedro, l_list, d_list, tezina, ekran):

        if prsa.isdigit () and l_biceps.isdigit () and d_biceps.isdigit () and struk.isdigit () \
           and bokovi.isdigit () and l_bedro.isdigit () and d_bedro.isdigit () and l_list.isdigit () \
           and d_list.isdigit () and tezina.isdigit ():
            
            ekran.destroy ()
    
            r_br = str (r_br)
    
            datum = datum.strftime ("%d.%m.%Y.")
    
            datoteka = open ("mjerenje.txt", "a")
    
            datoteka_r = open ("mjerenje.txt", "r")
    
            sadrzaj_datoteke = datoteka_r.readlines ()
    
            for i in range (0, len (sadrzaj_datoteke) / 13):
                lista_redaka = []
                for j in range (i * 13, (i * 13) + 13):
                    lista_redaka.append (sadrzaj_datoteke [j])
    
            datoteka.write ("\n" + r_br)
            datoteka.write ("\n" + datum)
            datoteka.write ("\n" + prsa)
            datoteka.write ("\n" + l_biceps)
            datoteka.write ("\n" + d_biceps)
            datoteka.write ("\n" + struk)
            datoteka.write ("\n" + bokovi)
            datoteka.write ("\n" + l_bedro)
            datoteka.write ("\n" + d_bedro)
            datoteka.write ("\n" + l_list)
            datoteka.write ("\n" + d_list)
            datoteka.write ("\n" + tezina)
            datoteka.write ("\n")
    
            datoteka.close ()

            Mjerenje.listanje_mjerenje ()            
            
            tkMessageBox.showinfo ("Uspjeh!", "Mjere uspjesno spremljene!")
        else:
            tkMessageBox.showerror ("Greska!", "Unijeli ste slova!")
            ekran.lift ()
    
    @staticmethod
    def unos_mjerenja ():

        def procedura ():

            unos_mjerenja_ekran = Toplevel ()
            datoteka_r = open ("mjerenje.txt", "r")
            sadrzaj_datoteke = datoteka_r.readlines ()
            global lista_redaka_mjerenje
            lista_redaka_mjerenje = []
            for i in range (0, len (sadrzaj_datoteke) / 13):
                for j in range (i * 13, (i * 13) + 13):
                    lista_redaka_mjerenje.append (sadrzaj_datoteke [j])
            if not lista_redaka_mjerenje:
                r_br = 0
            else:
                Mjerenje.listanje_mjerenje ()
                indeks = (pomnozi * 13) - 12
                r_br = lista_redaka_mjerenje [indeks]
                r_br = int (r_br)
            r_br += 1
            Label (unos_mjerenja_ekran, text = "Opseg prsa:").grid (row = 0, column = 0)
            opseg_prsa_unos = Entry (unos_mjerenja_ekran)
            opseg_prsa_unos.grid (row = 0, column = 1)
            Label (unos_mjerenja_ekran, text = "Lijevi biceps:").grid (row = 1, column = 0)
            l_biceps_unos = Entry (unos_mjerenja_ekran)
            l_biceps_unos.grid (row = 1, column = 1)
            Label (unos_mjerenja_ekran, text = "Desni biceps:").grid (row = 2, column = 0)
            d_biceps_unos = Entry (unos_mjerenja_ekran)
            d_biceps_unos.grid (row = 2, column = 1)
            Label (unos_mjerenja_ekran, text = "Opseg struka:").grid (row = 3, column = 0)
            struk_unos = Entry (unos_mjerenja_ekran)
            struk_unos.grid (row = 3, column = 1)
            Label (unos_mjerenja_ekran, text = "Opseg bokova:").grid (row = 4, column = 0)
            bokovi_unos = Entry (unos_mjerenja_ekran)
            bokovi_unos.grid (row = 4, column = 1)
            Label (unos_mjerenja_ekran, text = "Lijevo bedro:").grid (row = 5, column = 0)
            l_bedro_unos = Entry (unos_mjerenja_ekran)
            l_bedro_unos.grid (row = 5, column = 1)
            Label (unos_mjerenja_ekran, text = "Desno bedro:").grid (row = 6, column = 0)
            d_bedro_unos = Entry (unos_mjerenja_ekran)
            d_bedro_unos.grid (row = 6, column = 1)
            Label (unos_mjerenja_ekran, text = "Lijevi list:").grid (row = 7, column = 0)
            l_list_unos = Entry (unos_mjerenja_ekran)
            l_list_unos.grid (row = 7, column = 1)
            Label (unos_mjerenja_ekran, text = "Desni list:").grid (row = 8, column = 0)
            d_list_unos = Entry (unos_mjerenja_ekran)
            d_list_unos.grid (row = 8, column = 1)
            Label (unos_mjerenja_ekran, text = "Tezina:").grid (row = 9, column = 0)
            tezina_unos = Entry (unos_mjerenja_ekran)
            tezina_unos.grid (row = 9, column = 1)
            Button (unos_mjerenja_ekran, text = "SPREMI UNOS", command = lambda: \
                    Mjerenje.spremi_mjerenje (r_br, datum, opseg_prsa_unos.get(), l_biceps_unos.get(),\
                                     d_biceps_unos.get(), struk_unos.get(), bokovi_unos.get(),\
                                     l_bedro_unos.get(), d_bedro_unos.get(), \
                                     l_list_unos.get(), d_list_unos.get(), tezina_unos.get(),\
                                     unos_mjerenja_ekran)).grid (row = 10, column = 0)
            Button (unos_mjerenja_ekran, text = "ODUSTANI", command = \
                    unos_mjerenja_ekran.destroy).grid (row = 10, column = 1)
    
    
        postoji = os.path.exists ("mjerenje.txt")
        if not postoji:
            datoteka = open ("mjerenje.txt", "a")
            procedura ()
        else:
            procedura ()
    
    @staticmethod
    def ispis_mjerenja ():

        postoji = os.path.exists ("mjerenje.txt")
    
        if not postoji:
            tkMessageBox.showerror ("Greska!", "Nema unesenih podataka o mjerenju!")
        else:
            lista_mjerenja = []
        
            nazivi_stupaca = ("redni_broj_mjerenja", "datum_mjerenja", "prsa", "l_biceps", \
                              "d_biceps", "struk", "bokovi", "l_bedro", "d_bedro", "l_list", \
                              "d_list", "tezina")
            tablica = ttk.Treeview (columns = nazivi_stupaca, show = "headings")
        
            datoteka_r = open ("mjerenje.txt", "r")
        
            sadrzaj_datoteke = datoteka_r.readlines ()
        
            for i in range (0, len (sadrzaj_datoteke) / 13):
                lista_redaka = []
                for j in range (i * 13, (i * 13) + 13):
                    lista_redaka.append (sadrzaj_datoteke [j])
                
                mjerenje = Mjerenje (lista_redaka [1], lista_redaka [2], lista_redaka [3], \
                                     lista_redaka [4], lista_redaka [5], lista_redaka [6], \
                                     lista_redaka [7], lista_redaka [8], lista_redaka [9], \
                                     lista_redaka [10], lista_redaka [11], lista_redaka [12])
                lista_mjerenja.append (mjerenje)
            
            tablica.column ("redni_broj_mjerenja", width = 35)
            tablica.heading ("redni_broj_mjerenja", text = "R. Br.")
            tablica.column ("datum_mjerenja", width = 80)
            tablica.heading ("datum_mjerenja", text = "Datum")
            tablica.column ("prsa", width = 95)
            tablica.heading ("prsa", text = "Opseg prsa")
            tablica.column ("l_biceps", width = 95)
            tablica.heading ("l_biceps", text = "Lijevi biceps")
            tablica.column ("d_biceps", width = 95)
            tablica.heading ("d_biceps", text = "Desni biceps")
            tablica.column ("struk", width = 90)
            tablica.heading ("struk", text = "Opseg struka")
            tablica.column ("bokovi", width = 95)
            tablica.heading ("bokovi", text = "Opseg bokova")
            tablica.column ("l_bedro", width = 85)
            tablica.heading ("l_bedro", text = "Lijevo bedro")
            tablica.column ("d_bedro", width = 85)
            tablica.heading ("d_bedro", text = "Desno bedro")
            tablica.column ("l_list", width = 85)
            tablica.heading ("l_list", text = "Lijevi list")
            tablica.column ("d_list", width = 85)
            tablica.heading ("d_list", text = "Desni list")
            tablica.column ("tezina", width = 70)
            tablica.heading ("tezina", text = "Tezina")
        
            tablica.grid (column = 0, row = 0)
            
            for mjerenje in lista_mjerenja:
                tablica.insert ("", 'end', values = (mjerenje.r_br, mjerenje.datum, mjerenje.prsa, mjerenje.l_biceps, \
                                                 mjerenje.d_biceps, mjerenje.struk, mjerenje.bokovi, mjerenje.l_bedro, \
                                                 mjerenje.d_bedro, mjerenje.l_list, mjerenje.d_list, mjerenje.tezina))
    
    @staticmethod                                         
    def listanje_mjerenje ():
    
        lista_citanja_mjerenje = [line.strip () for line in open ("mjerenje.txt", "r")]
                
        global lista_r_br, lista_datuma, lista_prsa, lista_l_biceps, lista_d_biceps, lista_struk, \
        lista_bokovi, lista_l_bedro, lista_d_bedro, lista_l_list, lista_d_list, lista_tezina
                
        lista_r_br = lista_citanja_mjerenje [1::13]
        lista_r_br = map (int, lista_r_br)
        global pomnozi
        pomnozi = lista_r_br [-1]
        lista_r_br = [0] + lista_r_br
        del lista_r_br [-1]        
        lista_datuma = lista_citanja_mjerenje [2::13]
        lista_prsa = lista_citanja_mjerenje [3::13]
        lista_l_biceps = lista_citanja_mjerenje [4::13]
        lista_d_biceps = lista_citanja_mjerenje [5::13]
        lista_struk = lista_citanja_mjerenje [6::13]
        lista_bokovi = lista_citanja_mjerenje [7::13]
        lista_l_bedro = lista_citanja_mjerenje [8::13]
        lista_d_bedro = lista_citanja_mjerenje [9::13]
        lista_l_list = lista_citanja_mjerenje [10::13]
        lista_d_list = lista_citanja_mjerenje [11::13]
        lista_tezina = lista_citanja_mjerenje [12::13]
    
    @staticmethod
    def napredak_mjerenje ():

        postoji = os.path.exists ("mjerenje.txt")
    
        if not postoji:
            tkMessageBox.showerror ("Greska!", "Nema unesenih podataka o mjerenju!")
        else:
            Mjerenje.listanje_mjerenje ()
            if len (lista_datuma) == 1:
                tkMessageBox.showerror ("Greska!", "Nije moguc prikaz napretka za samo jedan unos!")
            else:
                graf = plt.figure ()
                osi = plt.subplot ()
                plt.xlabel ('Datum')
                plt.ylabel ('Mjera')
                plt.xticks (lista_r_br, lista_datuma)
                plt.plot (lista_r_br, lista_prsa)
                plt.plot (lista_r_br, lista_l_biceps)
                plt.plot (lista_r_br, lista_d_biceps)
                plt.plot (lista_r_br, lista_struk)
                plt.plot (lista_r_br, lista_bokovi)
                plt.plot (lista_r_br, lista_l_bedro)
                plt.plot (lista_r_br, lista_d_bedro)
                plt.plot (lista_r_br, lista_l_list, linestyle = "--")
                plt.plot (lista_r_br, lista_d_list, linestyle = "-.")
                plt.plot (lista_r_br, lista_tezina, linestyle = ":")
                
                box = osi.get_position ()
                osi.set_position ([box.x0, box.y0, box.width * 0.8, box.height]) # SMANJIVANJE GRAFA ZBOG LEGENDE
                
                legenda = plt.legend (["Prsa", "Lijevi biceps", "Desni biceps", "Struk", "Bokovi",\
                                "Lijevo bedro", "Desno bedro", "Lijevi list", "Desni list", "Tezina"], \
                                loc = 'center left', bbox_to_anchor = (1, 0.5))
                                
                for mjere in legenda.legendHandles:
                    mjere.set_linewidth (3) #POSTAVLJAMO DEBLJINU CRTE U LEGENDI              
                      
                graf_prozor = Tk ()
                graf_prozor.title ("Napredak mjerenja")
                graf_prozor.geometry ("1000x700")
                canvas = FigureCanvasTkAgg (graf, graf_prozor)
                canvas.show ()
                canvas.get_tk_widget ().pack (side = TOP, fill = BOTH, expand = 1)
                
                toolbar = NavigationToolbar2TkAgg (canvas, graf_prozor)
                toolbar.update ()
                canvas._tkcanvas.pack (side = TOP, fill = BOTH, expand = 1)
        
                Button (graf_prozor, text = "IZLAZ", command = \
                            graf_prozor.destroy).pack (side = BOTTOM)        
                
                plt.grid (True)

class Fit_Test:

    def __init__ (self, datum, switch_kicks, power_jacks, power_knees, power_jumps, \
                  globe_jumps, suicide_jumps, pushup_jacks, low_plank_oblique):

        self.datum = datum
        self.switch_kicks = switch_kicks
        self.power_jacks = power_jacks
        self.power_knees = power_knees
        self.power_jumps = power_jumps
        self.globe_jumps = globe_jumps
        self.suicide_jumps = suicide_jumps
        self.pushup_jacks = pushup_jacks
        self.low_plank_oblique = low_plank_oblique
    
    @staticmethod    
    def spremi_fit_test (datum, switch_kicks, power_jacks, power_knees, power_jumps, \
                     globe_jumps, suicide_jumps, pushup_jacks, low_plank_oblique, \
                     ekran):
    
        if switch_kicks.isdigit () and power_jacks.isdigit () and power_knees.isdigit () \
           and power_jumps.isdigit () and globe_jumps.isdigit () and suicide_jumps.isdigit ()\
           and pushup_jacks.isdigit () and low_plank_oblique.isdigit ():
    
            datum = datum.strftime ("%d.%m.%Y.")
    
            datoteka = open ("fit_test.txt", "a")
    
            datoteka_r = open ("fit_test.txt", "r")
    
            sadrzaj_datoteke = datoteka_r.readlines ()
    
            for i in range (0, len (sadrzaj_datoteke) / 10):
                lista_redaka = []
                for j in range (i * 10, (i * 10) + 10):
                    lista_redaka.append (sadrzaj_datoteke [j])
    
            datoteka.write ("\n" + datum)
            datoteka.write ("\n" + switch_kicks)
            datoteka.write ("\n" + power_jacks)
            datoteka.write ("\n" + power_knees)
            datoteka.write ("\n" + power_jumps)
            datoteka.write ("\n" + globe_jumps)
            datoteka.write ("\n" + suicide_jumps)
            datoteka.write ("\n" + pushup_jacks)
            datoteka.write ("\n" + low_plank_oblique)
            datoteka.write ("\n")
    
            datoteka.close ()
            
            Fit_Test.listanje_fit_test ()
            
            ekran.destroy ()
    
            tkMessageBox.showinfo ("Uspjeh!", "Rezultati Fit Testa uspjesno spremljeni!")
        else:
            tkMessageBox.showerror ("Greska!", "Unijeli ste slova!")
            ekran.lift ()
    
    @staticmethod    
    def unos_fit_testa ():
    
        unos_fit_testa_ekran = Tk ()
        Label (unos_fit_testa_ekran, text = "1. SWITCH KICKS:").grid (row = 0, column = 0)
        switch_kicks_unos = Entry (unos_fit_testa_ekran)
        switch_kicks_unos.grid (row = 0, column = 1)
        Label (unos_fit_testa_ekran, text = "2. POWER JACKS:").grid (row = 1, column = 0)
        power_jacks_unos = Entry (unos_fit_testa_ekran)
        power_jacks_unos.grid (row = 1, column = 1)
        Label (unos_fit_testa_ekran, text = "3. POWER KNEES:").grid (row = 2, column = 0)
        power_knees_unos = Entry (unos_fit_testa_ekran)
        power_knees_unos.grid (row = 2, column = 1)
        Label (unos_fit_testa_ekran, text = "4. POWER JUMPS:").grid (row = 3, column = 0)
        power_jumps_unos = Entry (unos_fit_testa_ekran)
        power_jumps_unos.grid (row = 3, column = 1)
        Label (unos_fit_testa_ekran, text = "5. GLOBE JUMPS:").grid (row = 4, column = 0)
        globe_jumps_unos = Entry (unos_fit_testa_ekran)
        globe_jumps_unos.grid (row = 4, column = 1)
        Label (unos_fit_testa_ekran, text = "6. SUICIDE JUMPS:").grid (row = 5, column = 0)
        suicide_jumps_unos = Entry (unos_fit_testa_ekran)
        suicide_jumps_unos.grid (row = 5, column = 1)
        Label (unos_fit_testa_ekran, text = "7. PUSH-UP JACKS:").grid (row = 6, column = 0)
        pushup_jacks_unos = Entry (unos_fit_testa_ekran)
        pushup_jacks_unos.grid (row = 6, column = 1)
        Label (unos_fit_testa_ekran, text = "8. LOW PLANK OBLIQUE:").grid (row = 7, column = 0)
        low_plank_oblique_unos = Entry (unos_fit_testa_ekran)
        low_plank_oblique_unos.grid (row = 7, column = 1)
        Button (unos_fit_testa_ekran, text = "SPREMI UNOS", command = lambda: \
                Fit_Test.spremi_fit_test (datum, switch_kicks_unos.get (), power_jacks_unos. get(), \
                                 power_knees_unos.get(), power_jumps_unos.get(), \
                                 globe_jumps_unos.get (), suicide_jumps_unos.get(), \
                                 pushup_jacks_unos. get(), \
                                 low_plank_oblique_unos.get(), unos_fit_testa_ekran))\
                                 .grid (row = 8, column = 0)
        Button (unos_fit_testa_ekran, text = "ODUSTANI", command = \
                unos_fit_testa_ekran.destroy).grid (row = 8, column = 1)
    
    @staticmethod
    def ispis_fit_testa ():
    
        postoji = os.path.exists ("fit_test.txt")
    
        if not postoji:
            tkMessageBox.showerror ("Greska!", "Nema unesenih podataka o Fit Testovima!")
        else:
            lista_fit_test = []
            
            nazivi_stupaca = ("datum", "switch_kicks", "power_jacks", "power_knees", "power_jumps", \
                              "globe_jumps", "sucide_jumps", "pushup_jacks", "low_plank_oblique")
            tablica = ttk.Treeview (columns = nazivi_stupaca, show = "headings")
        
            datoteka_r = open ("fit_test.txt", "r")
        
            sadrzaj_datoteke = datoteka_r.readlines ()
        
            for i in range (0, len (sadrzaj_datoteke) / 10):
                lista_redaka = []
                for j in range (i * 10, (i * 10) + 10):
                    lista_redaka.append (sadrzaj_datoteke [j])
                
                fit_test = Fit_Test (lista_redaka [1], lista_redaka [2], lista_redaka [3], \
                                     lista_redaka [4], lista_redaka [5], lista_redaka [6], \
                                     lista_redaka [7], lista_redaka [8], lista_redaka [9])
                lista_fit_test.append (fit_test)
            
            tablica.column ("datum", width = 111)
            tablica.heading ("datum", text = "Datum")
            tablica.column ("switch_kicks", width = 111)
            tablica.heading ("switch_kicks", text = "Switch kicks")
            tablica.column ("power_jacks", width = 111)
            tablica.heading ("power_jacks", text = "Power jacks")
            tablica.column ("power_knees", width = 111)
            tablica.heading ("power_knees", text = "Power knees")
            tablica.column ("power_jumps", width = 111)
            tablica.heading ("power_jumps", text = "Power jumps")
            tablica.column ("globe_jumps", width = 111)
            tablica.heading ("globe_jumps", text = "Globe jumps")
            tablica.column ("sucide_jumps", width = 111)
            tablica.heading ("sucide_jumps", text = "Suicide jumps")
            tablica.column ("pushup_jacks", width = 111)
            tablica.heading ("pushup_jacks", text = "Push-up jacks")
            tablica.column ("low_plank_oblique", width = 111)
            tablica.heading ("low_plank_oblique", text = "Low plank oblique")
        
            tablica.grid (column = 0, row = 0)
        
            for i in range (0, len(lista_fit_test)):
                fit_test = lista_fit_test [i]
                tablica.insert ("", 'end', values = (fit_test.datum, fit_test.switch_kicks, fit_test.power_jacks, \
                                                 fit_test.power_knees, fit_test.power_jumps, fit_test.globe_jumps, \
                                                 fit_test.suicide_jumps, fit_test.pushup_jacks, fit_test.low_plank_oblique))
    
    @staticmethod                                         
    def listanje_fit_test ():
    
        lista_citanja_fit_test = [line.strip () for line in open ("fit_test.txt", "r")]
                
        global lista_datuma_ft, lista_switch_kicks, lista_power_jacks, lista_power_knees, lista_power_jumps, \
        lista_globe_jumps, lista_suicide_jumps, lista_pushup_jacks, lista_low_plank_oblique, lista_ft
                       
        lista_datuma_ft = lista_citanja_fit_test [1::10]
        lista_switch_kicks = lista_citanja_fit_test [2::10]
        lista_power_jacks = lista_citanja_fit_test [3::10]
        lista_power_knees = lista_citanja_fit_test [4::10]
        lista_power_jumps = lista_citanja_fit_test [5::10]
        lista_globe_jumps = lista_citanja_fit_test [6::10]
        lista_suicide_jumps = lista_citanja_fit_test [7::10]
        lista_pushup_jacks = lista_citanja_fit_test [8::10]
        lista_low_plank_oblique = lista_citanja_fit_test [9::10]
        duljina_liste_ft = len (lista_datuma_ft) # ODREDUJEMO DULJINU LISTE
        lista_ft = list (range (duljina_liste_ft)) # STVARAMO LISTU BROJEVA DO BROJA DULJINE LISTE
        lista_ft = map (lambda x : x + 1, lista_ft) # POVECAVAMO BROJEVE U LISTI ZA 1 (POTREBNO ZA xticks U MATPLOTLIB MODULU)

    @staticmethod    
    def napredak_fit_test ():

        postoji = os.path.exists ("fit_test.txt")
    
        if not postoji:
            tkMessageBox.showerror("Greska!", "Nema unesenih podataka o Fit Testovima!")
        else:
            Fit_Test.listanje_fit_test ()
            if len (lista_datuma_ft) == 1:
                tkMessageBox.showerror("Greska!", "Nije moguc prikaz napretka za samo jedan unos!")
            else:
                graf = plt.figure ()
                osi = plt.subplot ()
                plt.xlabel ('Datum')
                plt.ylabel ('Broj ponavljanja')
                plt.xticks (lista_ft, lista_datuma_ft)
                graf_switch_kicks = plt.plot (lista_ft, lista_switch_kicks)
                graf_power_jacks = plt.plot (lista_ft, lista_power_jacks)
                graf_power_knees = plt.plot (lista_ft, lista_power_knees)
                graf_power_jumps = plt.plot (lista_ft, lista_power_jumps)
                graf_globe_jumps = plt.plot (lista_ft, lista_globe_jumps)
                graf_suicide_jumps = plt.plot (lista_ft, lista_suicide_jumps)
                graf_pushup_jacks = plt.plot (lista_ft, lista_pushup_jacks)
                graf_low_plank_oblique = plt.plot (lista_ft, lista_low_plank_oblique, linestyle = "--")
                
                box = osi.get_position ()
                osi.set_position ([box.x0, box.y0, box.width * 0.8, box.height]) # SMANJIVANJE GRAFA ZBOG LEGENDE
                
                legenda = plt.legend (["Switch kicks", "Power jacks", "Power knees", "Power jumps",\
                                "Globe jumps", "Suicide jumps", "Push-up jacks", "Low plank oblique"], \
                                loc = 'center left', bbox_to_anchor = (1, 0.5))
                                
                for mjere in legenda.legendHandles:
                    mjere.set_linewidth (3) #POSTAVLJAMO DEBLJINU CRTE U LEGENDI
                    
                graf_prozor = Tk ()
                graf_prozor.title ("Napredak fit testa")
                graf_prozor.geometry ("1000x700")
                canvas = FigureCanvasTkAgg (graf, graf_prozor)
                canvas.show ()
                canvas.get_tk_widget ().pack (side = TOP, fill = BOTH, expand = 1)
                
                toolbar = NavigationToolbar2TkAgg (canvas, graf_prozor)
                toolbar.update ()
                canvas._tkcanvas.pack (side = TOP, fill = BOTH, expand = 1)
        
                Button (graf_prozor, text = "IZLAZ", command = \
                            graf_prozor.destroy).pack (side = BOTTOM)   
                       
                plt.grid (True)

def kalorijski_zahtjevi ():

    datoteka_r = open ("osobni.txt", "r")
    sadrzaj_datoteke = datoteka_r.readlines ()
    for i in range (0, len (sadrzaj_datoteke) / 5):
        lista_redaka = []
        for j in range (i * 5, (i * 5) + 5):
            lista_redaka.append (sadrzaj_datoteke [j])

    spol = lista_redaka [1]
    dob = int (lista_redaka [2])
    visina = int (lista_redaka [3])    
    tezina = int (lista_redaka [4])
    tezina_f = tezina * 2.20462262
    visina_in = visina * 0.393700787
    if spol == "Zensko":
        zahtjevi_f = (655 + (4.35 * tezina_f) + (4.7 * visina_in) - (4.7 * dob)) * 1.55
        zahtjevi = int (math.ceil (zahtjevi_f))
        poruka = "Vasi dnevni kalorijski zahtjevi iznose:", zahtjevi
        tkMessageBox.showinfo ("Kalorijski zahtjevi", poruka)
    else:
        zahtjevi_m = (66 + (6.23 * tezina_f) + (12.7 * visina_in) - (6.8 * dob)) * 1.55
        zahtjevi = int (math.ceil (zahtjevi_m))
        poruka = "Vasi dnevni kalorijski zahtjevi iznose:", zahtjevi
        tkMessageBox.showinfo ("Kalorijski zahtjevi", poruka)

def dodavanje_fotografija ():

    def pretrazi (ekran):

        lokacija_datoteke = tkFileDialog.askopenfilename (filetypes = (("Template files", "*.jpg"), ("All files", "*")))
        global slika
        slika = Image.open (lokacija_datoteke)
        slika = slika.resize ((308, 440), Image.ANTIALIAS)
        global fotografija
        fotografija = ImageTk.PhotoImage (slika)
        ekran.image = fotografija # POSTAVLJAMO SLIKU KAO ATRIBUT EKRANU
        pano = Label (ekran, image = fotografija)
        pano.grid (row = 0, columnspan = 3)
        ekran.lift ()

    def dodaj (ekran):

        if not "fotografija" in globals (): # PROVJERAVAMO DA LI JE ODABRANA KOJA FOTOGRAFIJA
            tkMessageBox.showerror ("Greska!", "Nije odabrana slika za dodavanje!")
            ekran.lift ()
        else:
            if not os.path.exists ("Slike"):
                os.makedirs ("Slike")
            ime_slike = datum.strftime ('%d-%m-%Y') + ".jpg"
            slika.save (os.path.join ("Slike", ime_slike))
            tkMessageBox.showinfo ("Uspjeh!", "Slika uspjesno spremljena!")
            ekran.destroy ()
        
    dodavanje_fotografija_ekran = Toplevel ()
    dodavanje_fotografija_ekran.title ("Dodavanje fotografija")
    Button (dodavanje_fotografija_ekran, text = "PRETRAZI", command = lambda: pretrazi (dodavanje_fotografija_ekran)).grid (row = 1, column = 0)
    Button (dodavanje_fotografija_ekran, text = "DODAJ", command = lambda: dodaj (dodavanje_fotografija_ekran)).grid (row = 1, column = 1)
    Button (dodavanje_fotografija_ekran, text = "IZLAZ", command = dodavanje_fotografija_ekran.destroy).grid (row = 1, column = 2)

def pregled_fotografija ():

    def dodaj_sliku (ekran, stupac):

        if not "fotka" in globals ():
            tkMessageBox.showerror ("Greska!", "Nije odabrana slika za prikazivanje!")
            ekran.lift ()
        else:
            ekran.image = fotka
            pano = Label (ekran, image = fotka)
            pano.grid (row = 0, column = stupac)
            Label (ekran, text = odabrana_slika [:-4]).grid (row = 1, column = stupac)

    def odabir (dog):
        
        global odabrana_slika
        odabrana_slika = str (listbox_slika.get (listbox_slika.curselection ()))
        lokacija_slike = "Slike/" + odabrana_slika
        global slikica
        slikica = Image.open (lokacija_slike)
        global fotka
        fotka = ImageTk.PhotoImage (slikica)
        
    import glob

    pregled_fotografija_ekran = Toplevel ()
    pregled_fotografija_ekran.title ("Pregled fotografija")
    pregled_fotografija_ekran.geometry ("1020x600")
    pregled_fotografija_ekran.resizable (0, 0)
    listbox_slika = Listbox (pregled_fotografija_ekran, width = 50, height = 35)
    listbox_slika.grid (columnspan = 3)
    listbox_slika.bind ('<<ListboxSelect>>', odabir)
    traka = Scrollbar (pregled_fotografija_ekran)
    traka.grid (row = 0, column = 3, sticky = E)
    listbox_slika.config (yscrollcommand = traka.set)
    traka.config (command = listbox_slika.yview)
    lista_imena = glob.glob ("Slike/*.jpg")
    lista_imena = [i [6:] for i in lista_imena] # BRISEMO PRVIH 6 ZNAKOVA IZ STRINGA U LISTI
    lista_imena.sort ()
    n = 1
    m = 0
    for i in lista_imena:
        listbox_slika.insert (n, lista_imena [m])
        n += 1
        m += 1
    Button (pregled_fotografija_ekran, text = "SLIKA 1", command = lambda: dodaj_sliku (pregled_fotografija_ekran, 4)).grid (row = 1, column = 0)
    Button (pregled_fotografija_ekran, text = "SLIKA 2", command = lambda: dodaj_sliku (pregled_fotografija_ekran, 5)).grid (row = 1, column = 1)
    Button (pregled_fotografija_ekran, text = "IZLAZ", command = pregled_fotografija_ekran.destroy).grid (row = 1, column = 2)
    naslov_slika_1 = Label (pregled_fotografija_ekran, text = "Slika 1", font= "-weight bold")
    naslov_slika_1.grid (row = 0, column = 4, padx = (200, 100), sticky = N)
    naslov_slika_2 = Label (pregled_fotografija_ekran, text = "Slika 2", font= "-weight bold")
    naslov_slika_2.grid (row = 0, column = 5, padx = (100, 150), sticky = N)
    okvir_slika_1 = Frame (pregled_fotografija_ekran, width = 308, height = 440, bg = "white", colormap = "new")
    okvir_slika_1.grid (row = 0, column = 4)
    okvir_slika_2 = Frame (pregled_fotografija_ekran, width = 308, height = 440, bg = "white", colormap = "new")
    okvir_slika_2.grid (row = 0, column = 5)
    
def o_aplikaciji ():

    o_aplikaciji_ekran = Tk ()
    o_aplikaciji_ekran.title ("O aplikaciji")
    Label (o_aplikaciji_ekran, text = "Autor: Denis Miokovic").grid (row = 0)
    Label (o_aplikaciji_ekran, text = "Ustanova: Veleuciliste Velika Gorica").grid (row = 1)
    Label (o_aplikaciji_ekran, text = "Verzija: 1.00").grid (row = 2)
    Label (o_aplikaciji_ekran, text = "Datum izrade:").grid (row = 3)
    Button (o_aplikaciji_ekran, text = "IZLAZ", command = o_aplikaciji_ekran.destroy).grid (row = 4)

def restart_programa ():

    def restart (ekran):

        from shutil import rmtree

        if not os.path.exists ("osobni.txt") and not os.path.exists ("fit_test.txt") and \
           not os.path.exists ("mjerenje.txt") and not os.path.exists ("Slike"):
            tkMessageBox.showerror("Greska!", "Ne postoje podaci za brisanje!")
        else:
            if os.path.exists ("osobni.txt"):
                os.remove ("osobni.txt")
            if os.path.exists ("fit_test.txt"):
                os.remove ("fit_test.txt")
            if os.path.exists ("mjerenje.txt"):
                os.remove ("mjerenje.txt")
            if os.path.exists ("Slike"):
                rmtree ("Slike")
            tkMessageBox.showinfo ("Uspjeh!", "Podaci su uspjesno obrisani! Slijedi izlaz iz aplikacije!")
            ekran.destroy ()
            root.destroy ()
               
    restart_programa_ekran = Toplevel ()
    restart_programa_ekran.title ("Restart programa")
    Label (restart_programa_ekran, text = "Ukoliko pritisnete RESTART, brisu se svi dosad uneseni podaci").grid (row = 0, columnspan = 2)
    Label (restart_programa_ekran, text = "te slijedi izlaz iz programa.").grid (row = 1, columnspan = 2)
    Button (restart_programa_ekran, text = "RESTART", command = lambda: restart (restart_programa_ekran)).grid (row = 2, column = 0)
    Button (restart_programa_ekran, text = "ODUSTANI", command = restart_programa_ekran.destroy).grid (row = 2, column = 1)

global root
root = Tk ()
root.title ("Glavni izbornik")
root.geometry ("1000x600")
root.resizable (0, 0)
glavni_meni = Menu (root)

osobni_podaci_meni = Menu (glavni_meni, tearoff = 0)
mjerenje_meni = Menu (glavni_meni, tearoff = 0)
fit_test_meni = Menu (glavni_meni, tearoff = 0)
napredak_meni = Menu (glavni_meni, tearoff = 0)
fotografije_meni = Menu (glavni_meni, tearoff = 0)
opcije_meni = Menu (glavni_meni, tearoff = 0)

glavni_meni.add_cascade (label = "Osobni podaci", menu = osobni_podaci_meni)
osobni_podaci_meni.add_command (label = "Unos osobnih podataka", command = Osobni_Podaci.unos_osobnih_podataka)
osobni_podaci_meni.add_command (label = "Ispis osobnih podataka", command = Osobni_Podaci.ispis_osobnih_podataka)

glavni_meni.add_cascade (label = "Mjerenje", menu = mjerenje_meni)
mjerenje_meni.add_command (label = "Unos mjerenja", command = Mjerenje.unos_mjerenja)
mjerenje_meni.add_command (label = "Ispis mjerenja", command = Mjerenje.ispis_mjerenja)

glavni_meni.add_cascade (label = "Fit Test", menu = fit_test_meni)
fit_test_meni.add_command (label = "Unos Fit Testa", command = Fit_Test.unos_fit_testa)
fit_test_meni.add_command (label = "Ispis Fit Testa", command = Fit_Test.ispis_fit_testa)

glavni_meni.add_cascade (label = "Napredak", menu = napredak_meni)
napredak_meni.add_command (label = "Mjerenje", command = Mjerenje.napredak_mjerenje)
napredak_meni.add_command (label = "Fit Test", command = Fit_Test.napredak_fit_test)

glavni_meni.add_cascade (label = "Fotografije", menu = fotografije_meni)
fotografije_meni.add_command (label = "Dodavanje fotografije", command = dodavanje_fotografija)
fotografije_meni.add_command (label = "Pregled fotografija", command = pregled_fotografija)

glavni_meni.add_cascade (label = "Opcije", menu = opcije_meni)
opcije_meni.add_command (label = "Kalorijski zahtjevi", command = kalorijski_zahtjevi)
opcije_meni.add_command (label = "O aplikaciji", command = o_aplikaciji)
opcije_meni.add_command (label = "Restart programa", command = restart_programa)

glavni_meni.add_cascade (label = "Izlaz", command = root.destroy)

root.config (menu = glavni_meni)

root.mainloop ()

"""
TEZE: IMPLEMENTIRATI FUNKCIONALNOST DODAVANJA FOTOGRAFIJA ZA USPOREDBU PRIJE I POSLIJE
      IMPLEMENTIRATI FUNKCIONALNOST PRACENJA NAPRETKA UZ POMOC GRAFA KORISTECI MATPLOTLIB MODUL ----------------------- RIJESENO!!!!
"""


"""
http://www.tutorialspoint.com/python/tk_radiobutton.htm - 19.02.
http://effbot.org/tkinterbook/radiobutton.htm#Tkinter.Radiobutton.select-method - 19.02.
http://stackoverflow.com/questions/27435600/determine-which-radiobutton-has-been-selected - 19.02.
https://docs.python.org/3.2/library/datetime.html - 21.02.
http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python - 21.02.
http://stackoverflow.com/questions/4518641/how-to-round-off-a-floating-number-in-python - 24.02.
http://zetcode.com/gui/tkinter/dialogs/ - 24.02.
http://stackoverflow.com/questions/13897679/tkinter-reminder-messagebox-show-up - 24.02.
http://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window - 02.03.
http://stackoverflow.com/questions/19944712/browse-for-file-path-in-python - 06.03.
http://matplotlib.org/users/legend_guide.html 01.08.
"""
