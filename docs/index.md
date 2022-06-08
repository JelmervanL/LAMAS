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
