# %%
from collections import deque
import numpy as np
import pandas as pd

import datetime as dt
from datetime import datetime, timedelta
import time
import math
from Functions import *
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pyomo.environ

# %% [markdown]
Data=''
# Imprting Data from excel File using pandas lib
def Operation01(link):
    global Data
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
    Nuit_par1=19
    Nuit_par2=8
    # Nuit_par1=input('Heraire de demarage de brigade')
    # Nuit_par1=int(Nuit_par1)
    # Nuit_par2=input('Heraire de demarage de brigade')
    # Nuit_par2=int(Nuit_par2)
    Brigade=[]
    for i in range (len(Data)):
        if (Time[i].hour >=0 and Time[i].hour< Nuit_par2) or (Time[i].hour >=Nuit_par1 and Time[i].hour<=23): 
            Brigade.append("Nuit")
        else:
            Brigade.append("Journee")
    Data['Brigade']=Brigade


print(Data)

Brigade=''
Date=''


def DateCheck(Dt):
    global Date
    Date=Dt
def BrigadeCheck(Br):
    global Brigade
    Brigade=Br

Selected_Data=[]
Ex=0
Value_Terminal=0
Adj=0
min_Conducteur=0
def Operations02():
    global Data
    global Selected_Data
    global Date
    global Brigade
    global Ex
    global Value_Terminal
    global Adj
    global min_Conducteur

    print(Date)
    print(Brigade)
    if Brigade=='Journee':
        Selected_Data=pd.Data.loc[(Data['Date'] == Date) & (Data['Brigade'] == Brigade) ]
    elif Brigade=='Nuit':
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
        Selected_Data = pd.Data.loc[Data['DATETIME'].isin(Selected)]

    print(Selected_Data)
    Graph_intervale=[]
    for i in Selected_Data["Graph_intervale"]:
        Graph_intervale.append(i)
    # Graph_intervale=Selected_Data["Graph_intervale"]
    Graph_intervale=np.array(Graph_intervale) #doing array to remove the indexes from the selections before , also sice we require a type list for our code to work 
    print(Graph_intervale)

    Graph01=Selected_Data.loc[Selected_Data['Terminal'] == 'T1']
    Graph01=np.array(Graph01["Graph_intervale"])
    Graph02=Selected_Data.loc[Selected_Data['Terminal'] == 'T2']
    Graph02=np.array(Graph02["Graph_intervale"])
    Graph03=Selected_Data.loc[Selected_Data['Terminal'] == 'T4']
    Graph03=np.array(Graph03["Graph_intervale"])

    # %%
            #print(listAdj[i])
        #print(listAdj[i])
    # print(M)
    Adj=listAdj(Graph_intervale)
    print(Adj)

    Adj01=listAdj(Graph01)
    Adj02=listAdj(Graph02)
    Adj03=listAdj(Graph03)

    # %%

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

    # C=Gloton(Adj)
    C1=Gloton(Adj01)
    C2=Gloton(Adj02)
    C3=Gloton(Adj03)

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
    

    min_Conducteur=(Minimum(C1)+Minimum(C2)+Minimum(C3))
    print(min_Conducteur)

Conducteur=0
def ConducteurCheck(C):
    global Conducteur
    Conducteur=C







