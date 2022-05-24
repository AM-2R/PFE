# %%
# Import of the pyomo module
from pyomo.environ import *
 
# Creation of a Concrete Model
model = ConcreteModel()

# %%
model.C = Set(initialize=range(7), doc='les Conducteur')
model.J = Set(initialize=range(8), doc='les jobs')
model.A = Set(initialize=range(25), doc='les arcs')

# %%
model.n = Param(initialize=8, doc='le nombre de jobs')
model.c = Param(initialize=6, doc='le nombre de conducteur')
model.m = Param(initialize=25, doc='les relations entre les arcs')
model.ex1 = Param(model.A,initialize=[0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,3,3,3,4,4,4,5,5,6], doc='extrémité 1')
model.ex2 = Param(model.A,initialize=[2,3,5,6,7,2,3,4,5,6,7,3,4,5,6,7,5,6,7,5,6,7,6,7,7], doc='extrémité 2')

# %%
model.x = Var(model.C, model.J,domain=Binary, doc='affectation conducteur')
model.v = Var(model.C,bounds=(0,None),domain=Integers, doc='les taches')
model.y = Var(bounds=(0,None),domain=Integers, doc='valeur de comparaison')

# %%
def Cotraint1(model,j):
  return sum(model.x[i,j] for i in model.C) == 1
model.C1 = Constraint(model.J, rule=Cotraint1, doc='verification daffectation')


def Contraint2(model,i,k):
  return ((model.x[i,model.ex1[k]]+model.x[i,model.ex2[k]])) <= 1  

model.C2 = Constraint (model.C,model.J, rule=Contraint2, doc='verification de non chevauchement ')

def Contraint3(model,i):
  return sum(model.x[i,j] for j in model.J)==model.v[i]

model.C3 = Constraint (model.C, rule=Contraint3, doc='une seul tache par conducteur')

def Contraint4(model,i):
  return (model.v[i]<=model.y)

model.C4 = Constraint (model.C, rule=Contraint4, doc='maximiser')

# %%
def objective_rule(model):
  return model.y
model.objective = Objective(rule=objective_rule, sense=minimize, doc='Define objective function')

# %%
def pyomo_postprocess(options=None, instance=None, results=None):
  model.x.display()

# %%
if __name__ == '__main__':
    # This emulates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory
    import pyomo.environ
    opt = SolverFactory("gurobi")
    results = opt.solve(model,tee=True)
    #sends results to stdout
    results.write()
    print("\nDisplaying Solution\n" + '-'*60)
    pyomo_postprocess(None, model, results)

# %%
model.v.display()
model.y.display()


