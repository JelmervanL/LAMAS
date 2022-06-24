

class Good_agent():

  def __init__(self, agent_name):
    self.name = str(agent_name + 1)
    self.idx = agent_name
    self.is_party_leader = False
    self.is_in_quest_party = False
    self.is_evil = False