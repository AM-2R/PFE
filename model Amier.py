# %%
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

# %%
#inputs
Mat = [[0, 1, 1, 1, 0, 0, 1, 0], [1, 0, 0, 0, 1, 1, 0, 0], [1, 0, 0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 1, 0, 1], [0, 1, 0, 0, 1, 0, 0, 1], [1, 0, 1, 1, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1, 1, 0]]
ex1=  [0, 0, 0, 0, 1, 1, 2, 3, 4, 4, 5, 6]
ex2=  [1, 2, 3, 6, 4, 5, 6, 6, 5, 7, 7, 7]
c=6
jobs = len(Mat)

print(jobs)

#model
model = pyo.ConcreteModel()


model.i = Set(initialize=range(c), doc='les conducteur')
model.j = Set(initialize=range(jobs), doc='les jobs')
model.x = pyo.Var( range(c), range(jobs), within = Binary)
x = model.x
model.v = pyo.Var(range(c), bounds=(0,None),within =Integers)
v = model.v
model.y = pyo.Var(bounds=(0,None),within =Integers)
y = model.y
#constraints
model.C1=pyo.ConstraintList()
for j in range(jobs):
    model.C1.add = pyo.Constraint(expr = sum (x[i,j] for i in range(c)) == 1)

def assign_rule(model, j):
  return sum(sum (model.x[i,j] for i in range(c))) == 1
model.C1 = Constraint(model.j, rule=assign_rule)

# model.C2=pyo.ConstraintList()
# for i in range(c):
#     for j in range(len(ex1)):
#         model.C2.add=pyo.Constraint(expr =(x[i,ex1[j]]+x[i,ex2[j]])<=1)

# model.C3=pyo.ConstraintList()
# for i in range(c):
#     model.C3.add = pyo.Constraint( expr =sum (x[i,j] for j in range(jobs))== v[i])

# model.C4=pyo.ConstraintList()
# for i in range(c):
#     model.C4.add = pyo.Constraint(expr =v[i]<=y)

#objFun
model.obj = pyo.Objective(expr =y,sense=maximize)

opt = SolverFactory('gurobi')
results = opt.solve(model,tee=True)
#opt.solve(model)

model.pprint()
