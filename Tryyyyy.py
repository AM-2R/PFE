# %%
from collections import deque
from matplotlib.pyplot import pause
import numpy as np
import pandas as pd

import datetime as dt
from datetime import datetime, timedelta
import time
import math

# %%
from ast import If
from cProfile import label
from fileinput import filename
from msilib.schema import RadioButton
import os
from tkinter import *
from tkinter import filedialog, Text, Image, ttk
from PIL import ImageTk, Image

# %%
root = Tk()
root.title('ACP')
root.iconbitmap('assets/luffy.ico')
root.geometry("1080x900")
root.configure(bg='white')

# %%
# text lowel
L1 = Label(root, background='white',
           font=('Segoe UI', 20, 'bold'),
           bg='white',
           fg='#707070',
           text="1. Importer des données")
L1.place(x=30, y=160)
L11 = Label(root, background='white',
            font=('Segoe UI', 12, ),
            bg='white',
            fg='#707070',
            text="Tous les fichiers doivent être des fichiers xlsx contenant les colonnes suivantes ( Terminal , Date , HPA, HPD )")
L11.place(x=30, y=200)

# %%
# open exel file
link = ''


async def open():

    root.filename = filedialog.askopenfilename(
        title="Selectionnez un ficher", filetypes=[("Fichier Exel", "*.xlsx")])
    global link
    await root.filename
    link = root.filename

# button image
img1 = Image.open("assets/import.png")
re = img1.resize((380, 80))
img1 = ImageTk.PhotoImage(re)

Button(root, image=img1, bd=0, bg='#ffffff',
       activebackground='#ffffff',
       command=open).place(x=30, y=235)



# %% [markdown]
# Imprting Data from excel File using pandas lib

# %%
Data = pd.read_excel(link)
Data.info

# %%
Data.head

# %%
Data.shape
Data= Data.astype({"Date": str}, errors='raise')

# %% [markdown]
# We needed to make the data col as string because pands automaticly detaxted dates , but it made it deficult for us to process 

# %%
Data.info()
print(Data['Date'])


# %%

Time=[]
for i in range (len(Data)):
    if pd.notna(Data['HPA'][i]) : #Convert heure prevu d'accostage and adding to her the exact date
        Time.append(str(Data["Date"][i])+" "+str(Data['HPA'][i]))
    elif pd.notna(Data['HPD'][i]) :#Convert heure prevu d'essacostage and adding to her the exact date
        Time.append(str(Data["Date"][i])+" "+str(Data['HPD'][i]))
    else:
        Time.append(float('nan'))

print(Time)
Data['DATETIME']=Time #creating a new col in the table with the datetime for the operation .
print(Data)

# %%
print(len (Data['Terminal']))

# %%
# TimeGap1=input('Give a Time GAP Terminal 1 equal or bigger to 2  :') #input gap time based on the need and calculation 
# TimeGap1=int(TimeGap1)

# TimeGap2=input('Give a Time GAP Terminal 2 equal or bigger to 2  :') #input gap time based on the need and calculation 
# TimeGap2=int(TimeGap2)
# TimeGap4=input('Give a Time GAP Terminal Ouest equal or bigger to 2  :') #input gap time based on the need and calculation 
# TimeGap4=int(TimeGap4)

TimeGap1=4
TimeGap2=4
TimeGap4=6
def Trans_to_min(x):
    D=x.day*24*60
    min = x.minute
    H = x.hour *60
    return int(D+min+H)
# this fenction transfer the date time into a number , we transfered the date into munites also , because in the night shift , the 00:00 comes after 23:00 , so we needed another variable to tell us that the day changed

Graph_intervale=[]

for i in Data.index:
    if Data['Terminal'][i]=='T1':
        try:
            Graph_intervale.append([])
            Time[i] = dt.datetime.strptime(str(Time[i]), '%Y-%d-%m %H:%M:%S')
            min= Time[i]- dt.timedelta(minutes=TimeGap1//2)
            Graph_intervale[i].append(Trans_to_min(min))
            max= Time[i]+ dt.timedelta(minutes=TimeGap1//2)
            Graph_intervale[i].append(Trans_to_min(max))
        except:
            Time[i] = dt.datetime.strptime(str(Time[i]), '%d-%m-%Y %H:%M:%S')
            min= Time[i]- dt.timedelta(minutes=TimeGap1//2)
            Graph_intervale[i].append(Trans_to_min(min))
            max= Time[i]+ dt.timedelta(minutes=TimeGap1//2)
            Graph_intervale[i].append(Trans_to_min(max))
    elif Data['Terminal'][i]=='T2':
        try:
            Graph_intervale.append([])
            Time[i] = dt.datetime.strptime(str(Time[i]), '%Y-%d-%m %H:%M:%S')
            min= Time[i]- dt.timedelta(minutes=TimeGap2//2)
            Graph_intervale[i].append(Trans_to_min(min))
            max= Time[i]+ dt.timedelta(minutes=TimeGap2//2)
            Graph_intervale[i].append(Trans_to_min(max))
        except:
            Time[i] = dt.datetime.strptime(str(Time[i]), '%d-%m-%Y %H:%M:%S')
            min= Time[i]- dt.timedelta(minutes=TimeGap2//2)
            Graph_intervale[i].append(Trans_to_min(min))
            max= Time[i]+ dt.timedelta(minutes=TimeGap2//2)
            Graph_intervale[i].append(Trans_to_min(max))

    else:
        try:
            Graph_intervale.append([])
            Time[i] = dt.datetime.strptime(str(Time[i]), '%Y-%d-%m %H:%M:%S')
            min= Time[i]- dt.timedelta(minutes=TimeGap4//2)
            Graph_intervale[i].append(Trans_to_min(min))
            max= Time[i]+ dt.timedelta(minutes=TimeGap4//2)
            Graph_intervale[i].append(Trans_to_min(max))
        except:
            Time[i] = dt.datetime.strptime(str(Time[i]), '%d-%m-%Y %H:%M:%S')
            min= Time[i]- dt.timedelta(minutes=TimeGap4//2)
            Graph_intervale[i].append(Trans_to_min(min))
            max= Time[i]+ dt.timedelta(minutes=TimeGap4//2)
            Graph_intervale[i].append(Trans_to_min(max)) 
print((Graph_intervale))
Data['Graph_intervale']=Graph_intervale


# %% [markdown]
# we transftered into munites every variables for us to create an interval of time .

# %%
# Nuit_par1=19
# Nuit_par2=8
Nuit_par1=input('Heraire de demarage de brigade')
Nuit_par1=int(Nuit_par1)
Nuit_par2=input('Heraire de demarage de brigade')
Nuit_par2=int(Nuit_par2)
Brigade=[]
for i in range (len(Data)):
    if (Time[i].hour >=0 and Time[i].hour< Nuit_par2) or (Time[i].hour >=Nuit_par1 and Time[i].hour<=23): 
        Brigade.append("Nuit")
    else:
        Brigade.append("Journee")
Data['Brigade']=Brigade
print(Data)

# %%
#Select Brigate


# %%

# text zawej
L2 = Label(root, background='white',
           font=('Segoe UI', 20, 'bold'),
           bg='white',
           fg='#707070',
           text="2. Choisissez votre date")
L2.place(x=30, y=320)
L21 = Label(root, background='white',
            font=('Segoe UI', 12),
            bg='white',
            fg='#707070',
            text="la date doit être au format Annee-Mois-Jour, et incluse dans le fichier xlsx que vous avez importé avant .")
L21.place(x=30, y=360)

# input yakho
# hna hover


def click(event):
    input1.config(state=NORMAL)
    input1.delete(0, END)

# hna save input

Date=''
def ab3at():
    global Date
    sad = achfa.get()
    Date =sad


achfa = StringVar()
input1 = Entry(root, highlightthickness=1,
               width=30,
               textvariable=achfa,
               font=('Segoe UI', 25))

input1.place(x=30, y=400)
input1.insert(0, 'Ecrire votre date ici')
input1.config(highlightbackground="#707070",
              state=DISABLED,
              font=('Segoe UI', 25),
              highlightcolor='#707070')

input1.bind("<Button-1>", click)
# button image
img2 = Image.open("assets/valider.png")
re = img2.resize((200, 50))
img2 = ImageTk.PhotoImage(re)

Button(root, image=img2, bd=0, bg="#707070",
       activebackground='#ffffff',
       highlightthickness=1,
       command=ab3at).place(x=575, y=400)


# text talet
L2 = Label(root, background='white',
           font=('Segoe UI', 20, 'bold'),
           bg='white',
           fg='#707070',
           text="3. Choisissez votre Brigade")
L2.place(x=30, y=460)
L21 = Label(root, background='white',
            font=('Segoe UI', 12),
            bg='white',
            fg='#707070',
            text="vous pouvez toujours aller au paramettre pour vérifier l'heure de début de la brigade de nuit et la changer")
L21.place(x=30, y=500)
# radio button
v1 = IntVar()

Brigade=''
def nuit():
    global Brigade
    Brigade ='nuit'


def jour():
    global Brigade
    Brigade ='journee'


r1 = Radiobutton(root, text='Journee',
                 variable=v1,
                 font=('Segoe UI', 16, 'bold'),
                 bg='white',
                 fg='#707070',
                 value=1,
                 command=jour)
r1.place(x=100, y=530)

r2 = Radiobutton(root, text='Nuit',
                 variable=v1,
                 font=('Segoe UI', 16, 'bold'),
                 bg='white',
                 fg='#707070',
                 value=2,
                 command=nuit)
r2.place(x=300, y=530)

# %%



if Brigade=='Journee':
    Selected_Data=Data.loc[(Data['Date'] == Date) & (Data['Brigade'] == Brigade) ]
if Brigade=='Nuit':
    Time01 = dt.datetime.strptime(str(Date)+" 19:00:00", '%Y-%m-%d %H:%M:%S')
    Time02 = dt.datetime.strptime(str(Date)+" 08:00:00", '%Y-%m-%d %H:%M:%S')

    Time01=Trans_to_min(Time01)
    Time02=Trans_to_min(Time02) + 24*60
    print(Time01)
    print(Time02)
    Selected=[]
    for i in range(len(Data)):
        Time = dt.datetime.strptime(Data['DATETIME'][i], '%Y-%m-%d %H:%M:%S')
        Time=Trans_to_min(Time)
        if Time >= Time01 and Time < Time02 :
            Selected.append(Data['DATETIME'][i])
    Selected_Data = Data.loc[Data['DATETIME'].isin(Selected)]

print(Selected_Data)


# %% [markdown]
# Slection of the brigade based on the need , the pd.loc will filter based on the condition ,but the indexes will stay the same.

# %%
Graph_intervale=Selected_Data["Graph_intervale"]
Graph_intervale=np.array(Graph_intervale) #doing array to remove the indexes from the selections before , also sice we require a type list for our code to work 
print(Graph_intervale)

Graph01=Selected_Data.loc[Selected_Data['Terminal'] == 'T1']
Graph01=np.array(Graph01["Graph_intervale"])
Graph02=Selected_Data.loc[Selected_Data['Terminal'] == 'T2']
Graph02=np.array(Graph02["Graph_intervale"])
Graph03=Selected_Data.loc[Selected_Data['Terminal'] == 'T4']
Graph03=np.array(Graph03["Graph_intervale"])

# %%
def Verify_in_interval(M1,M2):
    if M1[0]<=M2[0] and M1[1]>=M2[0]:
        return True
    elif M1[0]<=M2[1] and M1[1]>=M2[1]:
        return True
    else: 
        return False 
def   listAdj(M):
    listAdj=[]
    for i in range(len(M)):
        listAdj.append([])
        for j in [x for x in range(len(M)) if x != i]:
            if Verify_in_interval(M[i],M[j]) or Verify_in_interval(M[j],M[i]) :
                listAdj[i].append(j)
            else:
                pass
    return listAdj
            #print(listAdj[i])
    #print(listAdj[i])
# print(M)
Adj=listAdj(Graph_intervale)
print(Adj)

Adj01=listAdj(Graph01)
Adj02=listAdj(Graph02)
Adj03=listAdj(Graph03)

# %%
def matriceAdj(Adj):
    Mat=[]
    for i in range( len(Adj)):
        Mat.append([])
        for j in range( len(Adj)):
            Mat[i].append(0)
            for k in range(len(Adj[i])):
                if j==Adj[i][k]:
                    Mat[i][j]=1
    return Mat

# %%
def arret(M):
    ex=[[],[]]
    for i in range (len(M)-1):
        for j in range(i+1,len(M)):
            if M[i][j]==1:
                ex[0].append(i)
                ex[1].append(j)
    return ex
#Create a list of start and end of each arret in our graph

# %%
Mat=matriceAdj(Adj)
Mat= np.array(Mat)
print (Mat)

# %%
Ex=arret(Mat)
print("ex1= ",Ex[0])
print("ex2= ",Ex[1])


print(len(Ex[0]))

# %%
def Gloton(Adj):
    n=len(Adj)
    NC=dict()
    C=[0 for k in range(n)]
    for i in range(n):
        NC[i]=[]
    def  rajouter(k,NC):
        if ((k in NC)==True):
            return NC
        else:
            NC.append(k)
            return NC
    i=0
    while i<=n-1:
        exist=True
        k=0
        while (exist==True):
            exist=k in NC[i]
            if (exist==True):
                k+=1
        C[i]=k    
        for j in range(len(Adj[i])):
            voisin=Adj[i][j]
            NC[voisin]=rajouter(k,NC[voisin])
        i+=1
    return C
# C=Gloton(Adj)
C1=Gloton(Adj01)
C2=Gloton(Adj02)
C3=Gloton(Adj03)
def Minimum(C):
    min_Conducteur=0
    for i in C:
        if min_Conducteur<=i:
            min_Conducteur=i
    if len(C)> 0:
        min_Conducteur+=1
    return min_Conducteur

min_Conducteur=(Minimum(C1)+Minimum(C2)+Minimum(C3))
print(min_Conducteur)
Conducteur=0
# text raba3
L4 = Label(root, background='white',
           font=('Segoe UI', 20, 'bold'),
           bg='white',
           fg='#707070',
           text="4. Choisissez le nombre de conducteur")
L4.place(x=30, y=570)
L41 = Label(root, background='white',
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#707070',
            text="Le nombre minimum possible est : {min_Conducteur}")
L41.place(x=30, y=610)

# input yakho
# hna hover


# def ss(event2):
#     input2.config(state=NORMAL)
#     input2.delete(0, 'end')
#     input2.unbind(0, '<FocusIn>')

# hna save input


def ab3at2():
    global Conducteur
    sad1 = achfa2.get()
    Conducteur=sad1


achfa2 = IntVar()

input2 = Entry(highlightthickness=1,
               width=30,
               textvariable=achfa2,
               font=('Segoe UI', 25))

input2.place(x=30, y=640)


input2.config(highlightbackground="#707070",
              #   state=DISABLED,
              font=('Segoe UI', 25),
              highlightcolor='#707070')

# input2.insert(0, 'Ecrire le nombre de conducteur ici')
# input1.bind('<FocusIn>', ss)
# button image
img3 = Image.open("assets/valider.png")
re = img3.resize((200, 50))
img3 = ImageTk.PhotoImage(re)

Button(root, image=img3, bd=0, bg="#707070",
       activebackground='#ffffff',
       highlightthickness=1,
       command=ab3at2).place(x=575, y=640)

# text raba3
L4 = Label(root, background='white',
           font=('Segoe UI', 12),
           bg='white',
           fg='#707070',
           text="Ecrire un chiffre supérieur ou egale à : {min_Conducteur}")
L4.place(x=30, y=700)
# button submit
img4 = Image.open("assets/submit.png")
re = img4.resize((700, 90))
img4 = ImageTk.PhotoImage(re)

Button(root, image=img4, bd=0, bg='#ffffff',
       activebackground='#ffffff',
       command=open).place(x=30, y=740)





# %%
Slected_Terminal=np.array(Selected_Data['Terminal'])

Value_Terminal=[]
for i in range(len(Slected_Terminal)):
    if Slected_Terminal[i]=='T1':
        Value_Terminal.append(1)
    elif Slected_Terminal[i]=='T2':
        Value_Terminal.append(2)
    else:
        Value_Terminal.append(4)

print(Value_Terminal)
    

# %%
# %%
# Import of the pyomo module
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pyomo.environ

# Creation of a Concrete Model
model = ConcreteModel()

# %%
model.C = Set(initialize=range(Conducteur), doc='les Conducteur')
model.J = Set(initialize=range(len(Adj)), doc='les jobs')
model.A = Set(initialize=range(len(Ex[0])), doc='les arcs')
model.t = Set (initialize=[1,2,4], doc='Terminal')
# %%
model.n = Param(initialize=len(Adj), doc='le nombre de jobs')
model.c = Param(initialize=Conducteur, doc='le nombre de conducteur')
model.m = Param(initialize=len(Ex[1]), doc='les relations entre les arcs')
model.ex1 = Param(model.A,initialize=Ex[0], doc='extrémité 1')
model.ex2 = Param(model.A,initialize=Ex[1], doc='extrémité 2')
model.T = Param(model.J,initialize=Value_Terminal, doc='les Terminal Affecté')
# %%
model.x = Var(model.C, model.J,domain=Binary, doc='affectation conducteur')
model.alpha = Var(model.C, model.t,domain=Binary, doc='affectation conducteur au terminal')
model.v = Var(model.C,bounds=(0,None),domain=Integers, doc='les taches')
model.y = Var(model.t,bounds=(0,None),domain=Integers, doc='valeur de comparaison')

# %%
def Cotraint1(model,j):
  return sum(model.x[i,j] for i in model.C) == 1
model.C1 = Constraint(model.J, rule=Cotraint1, doc='verification daffectation')


def Contraint2(model,i,k):
  return ((model.x[i,model.ex1[k]]+model.x[i,model.ex2[k]])) <= 1  

model.C2 = Constraint (model.C,model.A, rule=Contraint2, doc='verification de non chevauchement ')

def Contraint3(model,i):
  return sum(model.alpha[i,k] for k in model.t) == 1
model.C5 = Constraint(model.C, rule=Contraint3, doc='verification daffectation de terminal')

def Contraint4(model,i,j):
  return (model.alpha[i,model.T[j]] >= model.x[i,j] )
model.C6 = Constraint(model.C,model.J, rule=Contraint4, doc='verification daffectation au t')


def Contraint5(model,i):
  return sum(model.x[i,j] for j in model.J)==model.v[i]

model.C3 = Constraint (model.C, rule=Contraint5, doc='une seul tache par conducteur')

def Contraint6(model,i,k):
  return (model.alpha[i,k]*model.v[i]<=model.y[k])

model.C4 = Constraint (model.C,model.t, rule=Contraint6, doc='maximiser')

# %%

# %%
def objective_rule(model):
  return sum(model.y[k] for k in model.t)
model.objective = Objective(rule=objective_rule, sense=minimize, doc='Define objective function')



# %%
def pyomo_postprocess(options=None, instance=None, results=None):
  model.x.display()
# %%


opt = SolverFactory("gurobi")
results = opt.solve(model,tee=True)
#sends results to stdout
results.write()
print("\nDisplaying Solution\n" + '-'*60)
pyomo_postprocess(None, model, results)
# %%




# %%
model.v.display()
#verfy how much each driver is working per day

# %%
model.y.display()

# %%
x=model.x
Group_co=[]
Conducteur_ID=[0]*len(Adj)
for i in model.C:
    Group_co.append([])
    for j in model.J:
        if x[i,j].value == 1:
            Group_co[i].append(j)
            Conducteur_ID[j]=i

print(Group_co)
print(Conducteur_ID)

# %%
Selected_Data['Conducteur_ID']=Conducteur_ID
Selected_Data.drop('DATETIME', inplace=True, axis=1)
Selected_Data.drop('Graph_intervale', inplace=True, axis=1)

Selected_Data.head

# %%

import xlwt
from tempfile import TemporaryFile

import xlwt
from xlwt.Workbook import *
from pandas import ExcelWriter
import xlsxwriter
book = pd.ExcelWriter('Conducteur'+str(Date)+'-'+str(Brigade)+'.xlsx', engine='xlsxwriter')
Selected_Data.to_excel(book, sheet_name='recaputulation ')

for i in model.C:
    DATA=Selected_Data.loc[Selected_Data['Conducteur_ID'] == i]
    DATA.drop('Conducteur_ID', inplace=True, axis=1)
    DATA.to_excel(book, sheet_name='Conducteur '+str(i+1))

book.save()

root.mainloop()



