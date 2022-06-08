# Modelling Avalon

Authors: Anne-Jan Mein, Imme Huitema and Jelmer van Lune

## Description of Avalon

In the boardgame Avalon, two teams are playing against each other. These
teams are: “Loyal servants of Arthur” (Good) and “Minions of Mordred” (Evil).
Team Good wins by completing three out of five quests, team Evil by making
sure three out of five quests fail or by eliminating a special character called
“Merlin” after thee quests have successfully been completed.
When playing with five players, the teams are split into three players on team
Good (one of which is a special character called “Merlin”) and two on team Evil
(one of which is a special character called ”Assassin”). At the start of the game
everyone closes their eyes, and the players of team Evil reveal themselves to
each other. Then everyone closes their eyes, and Merlin opens his eyes while
the players of team Evil reveal themselves to Merlin without opening their eyes.
This results in the players of team Evil knowing who is on team Good and who
is on Team Evil without (most of) team Good knowing anything about other
players than themselves. The only exception is Merlin, who also knows who is
on team Good and Evil, but no one knows who Merlin is.
Every round a party leader is assigned. The first leader is random, the
following leaders are chosen as right side neighbour of the previous leader. The
leader can choose who goes on a quest. These players then have a choice to
play a “Pass” or a “Fail” card. A quest is only completed if everyone that went
on said quest played the Pass card, otherwise the quest fails. Players on team
Good must always play a Pass card, while players on team Evil can choose.
After a quest is completed a new party leader is assigned. The quest party size
can vary depending on quest number, which is determined as follows:

**Quest Number**  | **Party Size**
-------------     | -------------
1                 | 2
2                 | 3
3                 | 2
4                 | 3
5                 | 3

Players can vote on the team compositions of the quest teams proposed by
the party leader. If the majority approves the players go on the quest, if five
party propositions are rejected in a row the quest is failed automatically and a
new round begins.
After team Good has completed three quests, team Evil gets one more chance
at victory. If they manage to determine who Merlin is, who might have revealed
himself by sharing his knowledge too blatantly, they can assassinate him and
win the game. The Assassin character has the final say who gets assassinated.


## Knowledge in Avalon

- **Initial Knowledge**
  The logic in this game uses two propositional atoms: *e<sub> i </sub>* and *m<sub> i </sub>*. *e<sub> i </sub>* entails:
  Agent *i* is Evil. *m<sub> i </sub>* entails agent *i* is Merlin

  Consider a game where agents 1 and 2 are Good, agent 3 and 4 are Evil
  and agent 5 is Merlin. The initial knowledge of each agent is given by:

  - **Team Good**
    An agent on team Good knows that they are not Evil themselves.
    *K<sub> 1 </sub>* ¬*e<sub> 1 </sub>* ∧ K<sub> 2 </sub> ¬*e<sub> 2 </sub>*

  - **Team Evil**
    An agent on team Evil knows for every agent whether they are Good
    or Evil, and considers it possible that any agent on team Good is
    Merlin.  
    *K<sub> 3 </sub>* (*e<sub> 3 </sub>* ∧ *e<sub> 4 </sub>* ∧ ¬*e<sub> 1 </sub>* ∧ ¬*e<sub> 2 </sub>* ∧ ¬*e<sub> 5 </sub>* ∧ (*m<sub> 1 </sub>* ∨ *m<sub> 2 </sub>* ∨ *m<sub> 5 </sub>*)) ∧  
    *K<sub> 4 </sub>* (*e<sub> 4 </sub>* ∧ *e<sub> 3 </sub>* ∧ ¬*e<sub> 1 </sub>* ∧ ¬*e<sub> 2 </sub>* ∧ ¬*e<sub> 5 </sub>* ∧ (*m<sub> 1 </sub>* ∨ *m<sub> 2 </sub>* ∨ *m<sub> 5 </sub>*))  
  - **Merlin**
    Merlin knows for every agent whether they are Good or Evil  
    *K<sub> 5 </sub>* (¬*e<sub> 1 </sub>* ∧ ¬*e<sub> 2 </sub>* ∧ *e<sub> 3 </sub>* ∧ *e<sub> 4 </sub>* ∧ ¬*e<sub> 5 </sub>*)  

  In order to keep the model complexity low, only the Evil players care
  about Merlin. Merlin simply acts like any other Good player, except he
  starts the game with full knowledge about other agents roles. Therefore,
  knowledge about who Merlin is is only modeled from the perspective of
  agents from team Evil.


- **Determine Quest Leader**
  At the beginning of the game a random order is created which determines
  who will be the quest leader. The first quest leader will be the first person
  in this list, the next quest leader the one after etc. etc.


- **Choose Quest Team**
  The team selection for the quest is determined by the Quest leader. The
  choice of the quest leader depends on whether the quest leader is a member
  of team Good, team Evil or Merlin.
  - **Team Good**
    The team selection for the quest is determined by the Quest leader. The
    choice of the quest leader depends on whether the quest leader is a member
    of team Good, team Evil or Merlin.
    They will then try to fill up the rest of team with agents about whom
    they do not know whether or not they are Evil. If no such agents
    exist, they will fill up the team with agents about whom they know
    they are Evil.

  - **Team Evil**
    When the quest leader belongs to team Evil they do not want to send
    a member of team Evil on the quest that has been revealed as Evil to
    any of the team Good members, because these team Good members
    will then vote against the quest. In other words, if the quest leader
    knows that any of the team Good members knows the identity of
    one of the members of team Evil, they will not choose that team
    Evil member to go on the quest. If this happens the quest leader will
    choose the other member of team Evil that has not yet been revealed.
    The remaining spots for the quest are then randomly chosen from the
    Good members. The quest leader will always choose one Evil member
    for the quest, even if both Evil members have been revealed to the
    Good members. This Evil member will then be chosen randomly.
    This is done because the Evil members do not want to send a team
    that consists of only Good members.

    In short, a quest leader from team Evil will choose the Evil agent
    whose identity is known to the least amount of Good agents.

  - **Merlin**
    When the quest leader is the Merlin it behaves the same as a team
    Good member. Because Merlin knows the identity of all agents, Mer-
    lin will only choose players randomly out of the group of team Good
    to send on a quest.


- **Voting on Quest Team**
  When a team is proposed by the quest leader, each agent in the game
  votes whether they want that chosen team to go on the quest or not. How
  each agent votes depends on whether they belong to team Good, team
  Evil or Merlin.

  - **Team Good**
    A member of team Good will always disagree if they know that a
    member of team Evil is on the quest team. Otherwise they will agree
    with the proposed quest team.

  - **Team Evil**
    Members of team Evil want to be on the quest team, so they will
    always agree if one member of team Evil is in the proposed quest
    team. Otherwise they will disagree with the proposed quest team.

  - **Merlin**
    Merlin will use the same logic as a regular member of team Good,
    but will sometimes ”bluff” and vote against this belief. This means
    Merlin will agree with a team proposition that consists of a member
    of team Evil. This is done as an attempt to stay hidden, giving the
    members of team Evil false information about his own knowledge.

- **Pass or Fail Quest**
  Whether an agents chooses a pass or fail card when sent on a quest depends
  on whether the agents belongs to team Good or team Evil.
  - **Team Good**
    A member of team Good will always play the pass card when chosen
    on the quest.

  - **Team Evil**
    A team Evil member will wants to play a fail card to fail the quest.
    However, a member of team Evil will take into consideration that
    playing a fail card can result in the identity of both Evil members
    being discovered by a team Good member. If this can happen, they
    will choose a pass card instead of using a fail card, to hide the identities of team Evil.
  - **Merlin**
    For Merlin the behavior is the same as team Good. This means
    Merlin will always play the pass card when chosen on the quest.

- **Updating Knowledge Based On Public Announcements And Reasoning**
  The general voting of individual agents on team makeup is not considered
  a public announcement in our model, for simplification reasons.  

  The proposed quest team of the quest leader is also not considered a public
  announcement about the knowledge of the quest leader in our model.
  These restrictions are chosen to keep the model from growing too large.
  - **Team Good**
    The knowledge of members of team Good will be updated based on
    a public announcement that is a result of the quest passing/failing.
    If, for example, agent 1 and 2 are sent on a quest which fails with
    one fail card. This results in the following public announcement for
    everyone: [*e<sub> 1 </sub> ∨ e <sub> 1 </sub>*].  

    If agent 1 is on team Good, *K* <sub> 1 </sub> ¬*e* <sub> 1 </sub> therefore after this public announcement *K* <sub> 1 </sub> *e* <sub> 2 </sub>. 
    If a quest fails with all fail cards then the following announcement will be made:    
    [*e<sub> 1 </sub> ∧ e <sub> 1 </sub>*].  
    The same logic can be applied for quest were the quest team consists of three agents.
  - **Team Evil**
    The knowledge of team Evil is reasoned based on the voting of team good members 
    on quest team propositions. If an agent votes on a
    quest team that consists of at least one member of team Evil, then
    the members of team Evil will not consider that agent to be Merlin
    anymore. Furthermore, when a member of team Good was chosen to
    go on a quest together with a member of team Evil, and that Evil
    played the fail card, both team Evil members now know that the
    Good member knows that the Evil member that went on the quest
    is Evil.

  - **Merlin**
    Merlins knowledge is not updated, as this agent already knows
    everyone’s role/allegiance.