from good_agent import *
from evil_agent import *
from merlin_agent import *
from mlsolver.model import *
from mlsolver.formula import *



num_agents = 5
kripke_model = Avalon(num_agents)
formula = And(Box_a(str(1), Atom("e3")), And(Not(Atom("e1")), Not(Atom("m1"))))
# print(formula)
# nodes = kripke_model.kripke_structure.nodes_not_follow_formula(formula)
# print(len(nodes))

formula = And(Atom("e3"), Atom("e4"))
kripke_model.kripke_structure = kripke_model.kripke_structure.solve(formula)
print(len(kripke_model.kripke_structure.worlds))