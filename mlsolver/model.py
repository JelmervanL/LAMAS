""" Three wise men puzzle

Module contains data model for three wise men puzzle as Kripke strukture and agents announcements as modal logic
formulas
"""

from mlsolver.kripke import KripkeStructure, World
from mlsolver.formula import Atom, And, Not, Or, Box_a, Box_star


class WiseMenWithHat:
    """
    Class models the Kripke structure of the "Three wise men example.
    """

    knowledge_base = []

    def __init__(self):
        worlds = [
            World('RWW', {'1:R': True, '2:W': True, '3:W': True}),
            World('RRW', {'1:R': True, '2:R': True, '3:W': True}),
            World('RRR', {'1:R': True, '2:R': True, '3:R': True}),
            World('WRR', {'1:W': True, '2:R': True, '3:R': True}),

            World('WWR', {'1:W': True, '2:W': True, '3:R': True}),
            World('RWR', {'1:R': True, '2:W': True, '3:R': True}),
            World('WRW', {'1:W': True, '2:R': True, '3:W': True}),
            World('WWW', {'1:W': True, '2:W': True, '3:W': True}),
        ]

        relations = {
            '1': {('RWW', 'WWW'), ('RRW', 'WRW'), ('RWR', 'WWR'), ('WRR', 'RRR')},
            '2': {('RWR', 'RRR'), ('RWW', 'RRW'), ('WRR', 'WWR'), ('WWW', 'WRW')},
            '3': {('WWR', 'WWW'), ('RRR', 'RRW'), ('RWW', 'RWR'), ('WRW', 'WRR')}
        }

        relations.update(add_reflexive_edges(worlds, relations))
        relations.update(add_symmetric_edges(relations))

        self.ks = KripkeStructure(worlds, relations)

        # Wise man ONE does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('1', Atom('1:R'))), Not(Box_a('1', Not(Atom('1:R'))))))

        # This announcement implies that either second or third wise man wears a red hat.
        self.knowledge_base.append(Box_star(Or(Atom('2:R'), Atom('3:R'))))

        # Wise man TWO does not know whether he wears a red hat or not
        self.knowledge_base.append(And(Not(Box_a('2', Atom('2:R'))), Not(Box_a('2', Not(Atom('2:R'))))))

        # This announcement implies that third men has be the one, who wears a red hat
        self.knowledge_base.append(Box_a('3', Atom('3:R')))


class Avalon:
    
    def __init__(self, num_agents = 5):

        self.kripke_worlds, self.worlds = self.generate_all_possible_worlds(num_agents)
        self.relations = self.generate_all_relations(num_agents, self.worlds)
        self.relations.update(add_reflexive_edges(self.kripke_worlds, self.relations))
        self.relations.update(add_symmetric_edges(self.relations))
        self.kripke_structure = KripkeStructure(self.kripke_worlds, self.relations)

    def role_of_agent(self, agent, evil1, evil2):
        if agent == evil1 or agent == evil2:
            return True
        return False

    def generate_all_possible_worlds(self, num_agents):
        all_worlds = []
        for evil1 in range(num_agents - 1):
          for evil2 in range(evil1 + 1, num_agents):
            world = ('e',(evil1, evil2))
            all_worlds.append(world)

        worlds = []
        for idx in range(len(all_worlds)):
            current_world = all_worlds[idx]
            e0 = e1 = e2 = e3 = e4  = False
            evil1 = current_world[1][0]
            evil2 = current_world[1][1]

            #Determine roles of agents in this world
            e0 = self.role_of_agent(0, evil1, evil2)
            e1 = self.role_of_agent(1, evil1, evil2)
            e2 = self.role_of_agent(2, evil1, evil2)
            e3 = self.role_of_agent(3, evil1, evil2)
            e4 = self.role_of_agent(4, evil1, evil2)
            worlds.append(World(str(idx), {'e0': e0, 'e1': e1, 'e2': e2, 'e3': e3, 'e4': e4}))
        return worlds, all_worlds

    def generate_all_relations(self, num_agents, worlds):
        #Create a dictionary with all relations of agents. Each item in the dictionary contains the relations of a single agent
        relations = {}
        for idx in range(num_agents):
            relations[str(idx)] = []

        #Get roles in first world
        for first_world_idx in range(len(worlds) - 1):
            first_world = worlds[first_world_idx]
            evil_in_first_world = (first_world[1][0], first_world[1][1])
            good_in_first_world = list(range(num_agents))
            good_in_first_world.remove(evil_in_first_world[0])
            good_in_first_world.remove(evil_in_first_world[1])
            #Get roles in second world
            for second_world_idx in range(first_world_idx + 1, len(worlds)):
                second_world = worlds[second_world_idx]
                evil_in_second_world = (second_world[1][0], second_world[1][1])
                good_in_second_world = list(range(num_agents))
                good_in_second_world.remove(evil_in_second_world[0])
                good_in_second_world.remove(evil_in_second_world[1])
                #Check if the same agents are evil in both worlds
                if evil_in_first_world[0] in evil_in_second_world and evil_in_first_world[1] in evil_in_second_world:
                    relations[str(evil_in_first_world[0])].append((str(first_world_idx), str(second_world_idx)))
                    relations[str(evil_in_first_world[1])].append((str(first_world_idx), str(second_world_idx)))
                #Create relations of the agents that are good
                for idx in range(len(good_in_first_world)):
                    if good_in_first_world[idx] in good_in_second_world:
                        relations[str(good_in_first_world[idx])].append((str(first_world_idx), str(second_world_idx)))
        #Convert to sets to have the structure needed for mlsolver and adding symmetric/reflexive edges
        for idx in range(len(relations)):
            relations[str(idx)] = set(relations[str(idx)])
        return relations   


    def create_merlin(self, agent):
        merlin_relations = []
        for idx in range(len(self.worlds)):
            merlin_relations.append((str(idx), str(idx)))
            self.relations[str(agent)] = set(merlin_relations)
        # for idx in range(5):
        #     print(self.relations[str(idx)])
        self.kripke_structure = KripkeStructure(self.kripke_worlds, self.relations)
        # print(self.relations[str(agent)])


    ### Below are the functions to generate worlds and relations with the inclusion of Merlin in the game ###    

    # def role_of_agent(self, agent, evil1, evil2, merlin):
    #     if agent == evil1 or agent == evil2:
    #         return True, False
    #     elif agent == merlin:
    #         return False, True
    #     return False, False    

    # def generate_all_possible_worlds(self, num_agents):
    #     all_worlds = []
    #     for evil1 in range(1, num_agents):
    #       for evil2 in range(evil1 + 1, num_agents + 1):
    #         for merlin in range(1, num_agents + 1):
    #           if merlin != evil1 and merlin != evil2:
    #             world = (('e',(evil1, evil2)),('m', merlin))
    #             all_worlds.append(world)

    #     worlds = []
    #     for idx in range(len(all_worlds)):
    #         current_world = all_worlds[idx]
    #         e1 = m1 = e2 = m2 = e3 = m3 = e4 = m4 = e5 = m5 = False
    #         evil1 = current_world[0][1][0]
    #         evil2 = current_world[0][1][1]
    #         merlin = current_world[1][1]

    #         #Determine roles of agents in this world
    #         e1, m1 = self.role_of_agent(1, evil1, evil2, merlin)
    #         e2, m2 = self.role_of_agent(2, evil1, evil2, merlin)
    #         e3, m3 = self.role_of_agent(3, evil1, evil2, merlin)
    #         e4, m4 = self.role_of_agent(4, evil1, evil2, merlin)
    #         e5, m5 = self.role_of_agent(5, evil1, evil2, merlin)
    #         # print(str(idx), {'e1': e1, 'm1': m1, 'e2': e2, 'm2': m2, 'e3': e3, 'm3': m3, 'e4': e4, 'm4': m4, 'e5': e5, 'm5': m5})
    #         worlds.append(World(str(idx), {'e1': e1, 'm1': m1, 'e2': e2, 'm2': m2, 'e3': e3, 'm3': m3, 'e4': e4, 'm4': m4, 'e5': e5, 'm5': m5}))
    #     return worlds, all_worlds
     

    # def generate_all_relations(self, num_agents, worlds):
    #     #Create a dictionary with all relations of agents. Each item in the dictionary contains the relations of a single agent
    #     relations = {}
    #     for idx in range(1, num_agents + 1):
    #         relations[str(idx)] = []

    #     #Get roles in first world
    #     for first_world_idx in range(len(worlds) - 1):
    #         first_world = worlds[first_world_idx]
    #         evil_in_first_world = (first_world[0][1][0], first_world[0][1][1])
    #         is_merlin_in_1 = first_world[1][1]
    #         good_in_first_world = list(range(1, num_agents + 1))
    #         good_in_first_world.remove(is_merlin_in_1)
    #         good_in_first_world.remove(evil_in_first_world[0])
    #         good_in_first_world.remove(evil_in_first_world[1])
    #         #Get roles in second world
    #         for second_world_idx in range(first_world_idx + 1, len(worlds)):
    #             second_world = worlds[second_world_idx]
    #             evil_in_second_world = (second_world[0][1][0], second_world[0][1][1])
    #             is_merlin_in_2 = second_world[1][1]
    #             good_in_second_world = list(range(1, num_agents + 1))
    #             good_in_second_world.remove(is_merlin_in_2)
    #             good_in_second_world.remove(evil_in_second_world[0])
    #             good_in_second_world.remove(evil_in_second_world[1])
    #             #Check if the same agents are evil in both worlds
    #             if evil_in_first_world[0] in evil_in_second_world and evil_in_first_world[1] in evil_in_second_world:
    #                 relations[str(evil_in_first_world[0])].append((str(first_world_idx), str(second_world_idx)))
    #                 relations[str(evil_in_first_world[1])].append((str(first_world_idx), str(second_world_idx)))
    #             #Create relations of the agents that are good
    #             for idx in range(len(good_in_first_world)):
    #                 if good_in_first_world[idx] in good_in_second_world:
    #                     relations[str(good_in_first_world[idx])].append((str(first_world_idx), str(second_world_idx)))
    #             #Merlin knows the true world so he has no relations other than reflexive
    #     #Convert to sets to have the structure needed for mlsolver and adding symmetric/reflexive edges
    #     for idx in range(len(relations)):
    #         relations[str(idx + 1)] = set(relations[str(idx + 1)])
    #     return relations        



def add_symmetric_edges(relations):
    """Routine adds symmetric edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for r in agents_relations:
            x, y = r[1], r[0]
            result_agents.add((x, y))
        result[agent] = result_agents
    return result


def add_reflexive_edges(worlds, relations):
    """Routine adds reflexive edges to Kripke frame
    """
    result = {}
    for agent, agents_relations in relations.items():
        result_agents = agents_relations.copy()
        for world in worlds:
            result_agents.add((world.name, world.name))
            result[agent] = result_agents
    return result


# if __name__ == "__main__":
#     avalon = Avalon()
#     print(len(avalon.kripke_worlds))
#     for idx in range(len(avalon.relations)):
#         print("Relations of agent:" + str(idx + 1))
#         print(avalon.relations[str(idx + 1)])

