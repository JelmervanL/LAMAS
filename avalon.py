from good_agent import *
from evil_agent import *
from merlin_agent import *
from mlsolver.model import *
from mlsolver.formula import *
import random as rand


###Public announcement that agent 3 and agent 4 are evil and thus also not merlin
###A public anouncement like this can be made after both agents on a quest have played a fail card
# print(len(kripke_model.kripke_structure.worlds))
# formula = Or(Atom("e3"), Atom("e4"))
# kripke_model.kripke_structure = kripke_model.kripke_structure.solve(formula)
# print(len(kripke_model.kripke_structure.worlds))

def determine_party_leader(agents):
  #Check if first round, if so pick a random agent, otherwise pick the next agent
  first_round = True
  for idx in range(len(agents)):
    if agents[idx].is_party_leader == True:
      if idx != 4:
        agents[idx].is_party_leader = False
        agents[idx + 1].is_party_leader = True
        party_leader_idx = idx + 1
      else:
        agents[idx].is_party_leader = False
        agents[0].is_party_leader = True
        party_leader_idx = 0
  if first_round == True:
    party_leader_idx = rand.randint(0, 4)
    agents[party_leader_idx].is_party_leader = True
  return party_leader_idx

def choose_quest_party(kripke_model, agents, good_agents, evil_agents, party_leader_idx, party_size):
  #Reset previous party
  for idx in range(len(agents)):
    agents[idx].is_in_quest_pary = False

  #Determine the knowledge of good agents of evil agents
  knows_is_evil1 = []
  knows_is_evil2 = []
  for good_agent in good_agents:
    #good agent knows that an evil agent is evil, and he himself is not evil
    formula1 = And(Box_a(str(good_agent), Atom('e' + str(evil_agents[0]))), Not(Atom('e' + str(good_agent))))
    formula2 = And(Box_a(str(good_agent), Atom('e' + str(evil_agents[1]))), Not(Atom('e' + str(good_agent))))
    #Get nodes in current kripke structure where the previous formulas is not satisfiable
    nodes1 = kripke_model.kripke_structure.nodes_not_follow_formula(formula1)
    nodes2 = kripke_model.kripke_structure.nodes_not_follow_formula(formula2)
    #Check if good agent actually knows this
    if len(nodes1) < len(kripke_model.worlds):
      knows_is_evil1.append(good_agent)
    if len(nodes1) < len(kripke_model.worlds):
      knows_is_evil2.append(good_agent)
  #Case where party leader is evil
  if party_leader_idx in evil_agents:
    #Less good agents know evil1 is evil than evil2, so better to send evil1 on quest
    if len(knows_is_evil1) < len(knows_is_evil2):
      agents[evil_agents[0]].is_in_quest_pary = True
    elif len(knows_is_evil1) > len(knows_is_evil2):
      agents[evil_agents[1]].is_in_quest_pary = True
    #Choose random evil agent
    else:
      agents[evil_agents[rand.randint(0,1)]].is_in_quest_pary = True
    ###Fill rest of party with good agents 
    if party_size == 2:
      agents[good_agents[rand.randint(0,2)]].is_in_quest_pary = True
    else:
      good_agents_for_quest = rand.sample(good_agents, 2)
      agents[good_agents_for_quest[0]].is_in_quest_pary = True
      agents[good_agents_for_quest[1]].is_in_quest_pary = True

  #Case where party leader is good
  else:
    knows_is_good = []
    knows_is_good.append(party_leader_idx)
    for good_agent in good_agents:
      if good_agent != party_leader_idx:
        #party leader knows a good agent is good and he himself is good
        formula = And(Box_a(str(party_leader_idx), Not(Atom('e' + str(good_agent)))), Not(Atom('e' + str(party_leader_idx))))
        nodes = kripke_model.kripke_structure.nodes_not_follow_formula(formula)
        print(len(nodes))
        if len(nodes) < len(kripke_model.worlds):
          knows_is_good.append(good_agent)
    print(len(knows_is_good))
    sent_agents = 0
    #If party size is 2
    if party_size == 2:
      #Prune this list, based on people already sent (which are good) and evil agents
      agents_to_consider = [0, 1, 2, 3, 4]
      #Party leader knows of at least 2 good agents
      if len(knows_is_good) >= 2:
        agents_to_send = rand.sample(knows_is_good, 2)
        agents[agents_to_send[0]].is_in_quest_pary = True
        agents[agents_to_send[1]].is_in_quest_pary = True
        sent_agents = 2
      #Party leader knows only of himself, adds himself to quest team and removes himself from agents to consider further
      elif len(knows_is_good) == 1:
        agents[knows_is_good[0]].is_in_quest_pary = True
        agents_to_consider.remove(knows_is_good[0])
        sent_agents = 1

      #If party is not full
      if sent_agents == 1:
        #Remove agents that the party leader knows are evil from agents to consider sending on quest
        if party_leader_idx in knows_is_evil1:
          agents_to_consider.remove(evil_agents[0])
        if party_leader_idx in knows_is_evil2:
          agents_to_consider.remove(evil_agents[1])
        #Send a random agent on the quest from the party leaders list of considered agents
        agents[agents_to_consider[rand.randint(0, len(agents_to_consider) - 1)]].is_in_quest_pary = True

    #If party size is 3
    else:
      #Prune this list, based on people already sent (which are good) and evil agents
      agents_to_consider = [0, 1, 2, 3, 4]
      #Party leader knows of all 3 agents who is good
      if len(knows_is_good) == 3:
        agents_to_send = knows_is_good
        agents[agents_to_send[0]].is_in_quest_pary = True
        agents[agents_to_send[1]].is_in_quest_pary = True
        agents[agents_to_send[2]].is_in_quest_pary = True
        sent_agents = 3

      #Party leader knows identity of 2 good agents, adds them to quest team and removes them from agents to consider further
      elif len(knows_is_good) == 2:
        agents_to_send = rand.sample(knows_is_good, 2)
        agents[agents_to_send[0]].is_in_quest_pary = True
        agents[agents_to_send[1]].is_in_quest_pary = True
        sent_agents = 2
      #Party leader knows only of himself, adds himself to quest team and removes himself from agents to consider further
      elif len(knows_is_good) == 1:
        agents_to_consider
        agents[knows_is_good[0]].is_in_quest_pary = True
        agents_to_consider.remove(knows_is_good[0])
        sent_agents = 1

      #If party is not full, 1 spot open
      if sent_agents == 2:
        #Remove agents that the party leader knows are evil from agents to consider sending on quest
        if party_leader_idx in knows_is_evil1:
          agents_to_consider.remove(evil_agents[0])
        if party_leader_idx in knows_is_evil2:
          agents_to_consider.remove(evil_agents[1])
        #Send a random agent on the quest from the party leaders list of considered agents
        agents[agents_to_consider[rand.randint(0, len(agents_to_consider) - 1)]].is_in_quest_pary = True

      #If party is not full, 2 spots open 
      elif sent_agents == 1:
        #Remove agents that the party leader knows are evil from agents to consider sending on quest
        if party_leader_idx in knows_is_evil1:
          agents_to_consider.remove(evil_agents[0])
        if party_leader_idx in knows_is_evil2:
          agents_to_consider.remove(evil_agents[1])
        #Send a random agent on the quest from the party leaders list of considered agents
        random_agent = agents_to_consider[rand.randint(0, len(agents_to_consider) - 1)]
        agents[random_agent].is_in_quest_pary = True
        #Remove the agent that was sent from the list of agents to consider
        agents_to_consider.remove(random_agent)
        #Send a random agent on the quest from the party leaders list of considered agents
        random_agent = agents_to_consider[rand.randint(0, len(agents_to_consider) - 1)]
        agents[random_agent].is_in_quest_pary = True
        



def voting_on_quest_party():
  return

def go_on_quest():
  return

def update_knowledge():
  return



####MAIN####

num_agents = 5
kripke_model = Avalon(num_agents)
evil_agents = rand.sample(range(5), 2)
good_agents = []
agents = []
for idx in range(num_agents):
  if idx in evil_agents:
    agents.append(Evil_agent(idx))
  else:
    agents.append(Good_agent(idx))
    good_agents.append(idx)

current_party_leader = determine_party_leader(agents)
# print(current_party_leader + 1)
current_party_leader = 0
choose_quest_party(kripke_model, agents, good_agents, evil_agents, current_party_leader, party_size = 2)
print(good_agents)
print(evil_agents)
for idx in range(len(agents)):
  print("Agent " + str(idx + 1) + " is evil: " + str(agents[idx].is_evil) +  " and on quest = " + str(agents[idx].is_in_quest_pary))