
from main import *
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pyomo.environ

import xlwt
from tempfile import TemporaryFile
from tkinter.filedialog import *
import xlwt
from xlwt.Workbook import *
from pandas import ExcelWriter
import xlsxwriter

print (Adj)
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


book = pd.ExcelWriter(f'Conducteur{Date}-{Brigade}.xlsx', engine='xlsxwriter')
Selected_Data.to_excel(book, sheet_name='recaputulation ')

for i in model.C:
    DATA=Selected_Data.loc[Selected_Data['Conducteur_ID'] == i]
    DATA.drop('Conducteur_ID', inplace=True, axis=1)
    DATA.to_excel(book, sheet_name='Conducteur '+str(i+1))

book.save()

filename = asksaveasfilename(initialfile=f'Conducteur{Date}-{Brigade}.xlsx', initialdir='/', title = 'Save File', filetypes=(('Excel File', '.xlsx'),('Text File','.txt'),('All Files','*.*'))) 