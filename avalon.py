from good_agent import *
from evil_agent import *
from merlin_agent import *
from mlsolver.model import *
from mlsolver.formula import *
import random as rand
from copy import deepcopy


###Public announcement that agent 3 and agent 4 are evil and thus also not merlin
###A public anouncement like this can be made after both agents on a quest have played a fail card
# print(len(kripke_model.kripke_structure.worlds))
# formula = Or(Atom("e3"), Atom("e4"))
# kripke_model.kripke_structure = kripke_model.kripke_structure.solve(formula)
# print(len(kripke_model.kripke_structure.worlds))

def determine_party_leader(agents, round_number):
  #Check if first round, if so pick a random agent, otherwise pick the next agent
  first_round = False
  if round_number == 1:
    first_round = True

  for idx in range(len(agents)):
    if agents[idx].is_party_leader == True:
      if idx != 4:
        agents[idx].is_party_leader = False
        agents[idx + 1].is_party_leader = True
        party_leader_idx = idx + 1
        break
      else:
        agents[idx].is_party_leader = False
        agents[0].is_party_leader = True
        party_leader_idx = 0
        break
  if first_round == True:
    party_leader_idx = rand.randint(0, 4)
    agents[party_leader_idx].is_party_leader = True
  return party_leader_idx

def choose_quest_party(kripke_model, agents, good_agents, evil_agents, party_leader_idx, party_size):
  #Reset previous party
  for idx in range(len(agents)):
    agents[idx].is_in_quest_party = False

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
      agents[evil_agents[0]].is_in_quest_party = True
    elif len(knows_is_evil1) > len(knows_is_evil2):
      agents[evil_agents[1]].is_in_quest_party = True
    #Choose random evil agent
    else:
      agents[evil_agents[rand.randint(0,1)]].is_in_quest_party = True
    ###Fill rest of party with good agents 
    if party_size == 2:
      agents[good_agents[rand.randint(0,2)]].is_in_quest_party = True
    else:
      good_agents_for_quest = rand.sample(good_agents, 2)
      agents[good_agents_for_quest[0]].is_in_quest_party = True
      agents[good_agents_for_quest[1]].is_in_quest_party = True

  #Case where party leader is good
  else:
    knows_is_good = []
    knows_is_good.append(party_leader_idx)
    for good_agent in good_agents:
      if good_agent != party_leader_idx:
        #party leader knows a good agent is good and he himself is good
        formula = And(Box_a(str(party_leader_idx), Not(Atom('e' + str(good_agent)))), Not(Atom('e' + str(party_leader_idx))))
        nodes = kripke_model.kripke_structure.nodes_not_follow_formula(formula)
        if len(nodes) < len(kripke_model.worlds):
          knows_is_good.append(good_agent)
    sent_agents = 0
    #If party size is 2
    if party_size == 2:
      #Prune this list, based on people already sent (which are good) and evil agents
      agents_to_consider = [0, 1, 2, 3, 4]
      #Party leader knows of at least 2 good agents
      if len(knows_is_good) >= 2:
        agents_to_send = rand.sample(knows_is_good, 2)
        agents[agents_to_send[0]].is_in_quest_party = True
        agents[agents_to_send[1]].is_in_quest_party = True
        sent_agents = 2
      #Party leader knows only of himself, adds himself to quest team and removes himself from agents to consider further
      elif len(knows_is_good) == 1:
        agents[knows_is_good[0]].is_in_quest_party = True
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
        agents[agents_to_consider[rand.randint(0, len(agents_to_consider) - 1)]].is_in_quest_party = True

    #If party size is 3
    else:
      #Prune this list, based on people already sent (which are good) and evil agents
      agents_to_consider = [0, 1, 2, 3, 4]
      #Party leader knows of all 3 agents who is good
      if len(knows_is_good) == 3:
        agents_to_send = knows_is_good
        agents[agents_to_send[0]].is_in_quest_party = True
        agents[agents_to_send[1]].is_in_quest_party = True
        agents[agents_to_send[2]].is_in_quest_party = True
        sent_agents = 3

      #Party leader knows identity of 2 good agents, adds them to quest team and removes them from agents to consider further
      elif len(knows_is_good) == 2:
        agents_to_send = rand.sample(knows_is_good, 2)
        agents[agents_to_send[0]].is_in_quest_party = True
        agents[agents_to_send[1]].is_in_quest_party = True
        sent_agents = 2
      #Party leader knows only of himself, adds himself to quest team and removes himself from agents to consider further
      elif len(knows_is_good) == 1:
        agents_to_consider
        agents[knows_is_good[0]].is_in_quest_party = True
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
        agents[agents_to_consider[rand.randint(0, len(agents_to_consider) - 1)]].is_in_quest_party = True

      #If party is not full, 2 spots open 
      elif sent_agents == 1:
        #Remove agents that the party leader knows are evil from agents to consider sending on quest
        if party_leader_idx in knows_is_evil1:
          agents_to_consider.remove(evil_agents[0])
        if party_leader_idx in knows_is_evil2:
          agents_to_consider.remove(evil_agents[1])
        #Send a random agent on the quest from the party leaders list of considered agents
        random_agent = agents_to_consider[rand.randint(0, len(agents_to_consider) - 1)]
        agents[random_agent].is_in_quest_party = True
        #Remove the agent that was sent from the list of agents to consider
        agents_to_consider.remove(random_agent)
        #Send a random agent on the quest from the party leaders list of considered agents
        random_agent = agents_to_consider[rand.randint(0, len(agents_to_consider) - 1)]
        agents[random_agent].is_in_quest_party = True
        
def voting_on_quest_party(kripke_model, agents, good_agents, evil_agents):
  quest_party = []
  #Collect all agents that are in the quest party
  for idx in range(len(agents)):
    if agents[idx].is_in_quest_party:
      quest_party.append(idx)
  votes_in_favour = 0
  votes_against = 0
  #Voting
  for idx in range(len(agents)):
    #Party leader always for the team that he proposed
    if agents[idx].is_party_leader:
      votes_in_favour += 1
    else:
      #Agent voting is evil, no need to work with mlsolver as evil agents already know everyones role
      if idx in evil_agents:
        #Entire quest party filled with evil agents is too dangerous as neither can confidently fail a quest without possibly revealing both identities
        if evil_agents[0] in quest_party and evil_agents[1] in quest_party and len(quest_party) == 2:
          votes_against += 1
        #If an evil agent is in the quest party, vote in favour
        elif evil_agents[0] in quest_party or evil_agents[1] in quest_party:
          votes_in_favour += 1
        #Only good agents in quest party, vote against
        else:
          votes_against += 1
      #Agent voting is good
      else:
        agent_voted = False
        #Check knowledge of good agent to see if he knows an evil member is in quest party
        for agent in quest_party:
          #No need to check if good agent knows he is good
          if agent != idx:
            #Check if good agent knows of an agent if he is evil
            formula = And(Box_a(str(idx), Atom('e' + str(agent))), Not(Atom('e' + str(idx))))
            nodes = kripke_model.kripke_structure.nodes_not_follow_formula(formula)
            #If a good agent 
            if len(nodes) < len(kripke_model.worlds):
              votes_against += 1
              agent_voted = True
              break
        #Agent does not know if an evil agent is on the team
        if not agent_voted:
          votes_in_favour += 1
  print("votes in favour: " + str(votes_in_favour))
  print("votes against: " + str(votes_against))
  if votes_in_favour > votes_against:
    return True 
  else:
    return False

def go_on_quest(kripke_model, agents, good_agents, evil_agents, party_size, round_number):
  quest_party = []
  #Collect all agents that are in the quest party
  for idx in range(len(agents)):
    if agents[idx].is_in_quest_party:
      quest_party.append(idx)

  pass_card = 0
  fail_card = 0
  for agent1 in quest_party:
    #Good agents always play pass card
    if agent1 in good_agents:
      pass_card += 1

    #Evil agent play fail card unless they reveal both identities to at least one agent on team good 
    else:
      if round_number == 5:
        fail_card += 1
      elif party_size == 2:
        #Evaluate what happens to the kripke structure if a public anouncement is made after this quest based on the evil agent playing the fail card
        formula = Or(Atom('e' + str(quest_party[0])), Atom('e' + str(quest_party[1])))
        copy_of_kripke_model = deepcopy(kripke_model)
        copy_of_kripke_model.kripke_structure.solve(formula)
        for agent2 in quest_party:
          if agent1 != agent2:
            #Does the good agent in quest party know the identity of both evil agents
            formula = And(And(Box_a(str(agent2), Atom('e' + str(evil_agents[0]))), Box_a(str(agent2), Atom('e' + str(evil_agents[0])))), Not(Atom('e' + str(agent2))))
            nodes_actual_model = kripke_model.kripke_structure.nodes_not_follow_formula(formula)
            nodes_copy_model = copy_of_kripke_model.kripke_structure.nodes_not_follow_formula(formula)
            if len(nodes_actual_model) < len(kripke_model.worlds):
              knows_in_actual_world = True
            else:
              knows_in_actual_world = False
            if len(nodes_copy_model) < len(copy_of_kripke_model.worlds):
              knows_in_copy_world = True
            else:
              knows_in_copy_world = False
        #Play pass card if fail card will result in both identities being revealed
        if not knows_in_actual_world and knows_in_copy_world:
          pass_card += 1
        else: 
          fail_card += 1

      elif party_size == 3:
        #Evaluate what happens to the kripke structure if a public anouncement is made after this quest based on the evil agent playing the fail card
        #If both evil agents are in quest party
        if evil_agents[0] in quest_party and evil_agents[1] in quest_party:
          #In this case only fail if the good agent already knows the identity of both evil players anyway.
          copy_of_quest_party = quest_party.copy()
          copy_of_quest_party.remove(evil_agents[0])
          copy_of_quest_party.remove(evil_agents[1])
          good_agent_in_party = copy_of_quest_party[0]
          formula = And(And(Box_a(str(good_agent_in_party), Atom('e' + str(evil_agents[0]))), Box_a(str(good_agent_in_party), Atom('e' + str(evil_agents[0])))), Not(Atom('e' + str(good_agent_in_party))))
          nodes = kripke_model.kripke_structure.nodes_not_follow_formula(formula)
          if len(nodes) < len(kripke_model.worlds):
            fail_card += 1
          else:
            pass_card += 1

        #If only one evil agent is in quest party
        else:
          formula = Or(Or(Atom('e' + str(quest_party[0])), Atom('e' + str(quest_party[1]))), Atom('e' + str(quest_party[2])))
          copy_of_kripke_model = deepcopy(kripke_model)
          copy_of_kripke_model.kripke_structure.solve(formula)
          played_pass_card = False
          for agent2 in quest_party:
            if agent1 != agent2:
              #Does the good agent in quest party know the identity of both evil agents
              formula = And(And(Box_a(str(agent2), Atom('e' + str(evil_agents[0]))), Box_a(str(agent2), Atom('e' + str(evil_agents[0])))), Not(Atom('e' + str(agent2))))
              nodes_actual_model = kripke_model.kripke_structure.nodes_not_follow_formula(formula)
              nodes_copy_model = copy_of_kripke_model.kripke_structure.nodes_not_follow_formula(formula)
              if len(nodes_actual_model) < len(kripke_model.worlds):
                knows_in_actual_world = True
              else:
                knows_in_actual_world = False
              if len(nodes_copy_model) < len(copy_of_kripke_model.worlds):
                knows_in_copy_world = True
              else:
                knows_in_copy_world = False
              #Play pass card if fail card will result in both identities being revealed
              if not knows_in_actual_world and knows_in_copy_world:
                pass_card += 1
                played_pass_card = True
                break
          if not played_pass_card: 
            fail_card += 1

  return pass_card, fail_card

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

# current_party_leader = determine_party_leader(agents)
# print(current_party_leader)
# # current_party_leader = 0
# choose_quest_party(kripke_model, agents, good_agents, evil_agents, current_party_leader, party_size = 2)

# for idx in range(len(agents)):
#   print("Agent " + str(idx) + " is evil: " + str(agents[idx].is_evil) +  " and on quest = " + str(agents[idx].is_in_quest_party))
# print(voting_on_quest_party(kripke_model, agents, good_agents, evil_agents))
# print(go_on_quest(kripke_model, agents, good_agents, evil_agents, party_size = 2, round_number = 1))

party_sizes = [2, 3, 2, 3, 3]
evil_wins = 0
good_wins = 0

for round_number in range(1, 6):
  party_size = party_sizes[round_number-1]
  current_party_leader = determine_party_leader(agents, round_number=round_number)
  print("pary leader: ", current_party_leader)
  choose_quest_party(kripke_model, agents, good_agents, evil_agents, current_party_leader, party_size = party_size)
  if voting_on_quest_party(kripke_model, agents, good_agents, evil_agents):
    num_pass, num_fail = go_on_quest(kripke_model, agents, good_agents, evil_agents, party_size = party_size, round_number = round_number)
    if num_fail > 0:
      evil_wins += 1
    else: 
      good_wins += 1

print("evil_wins", evil_wins)
print("good_wins", good_wins)




  







