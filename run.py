
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
import random
# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()



# Creating propositions that represent the state of a task for a particular player in a particular round
#K_i: True if task round ‘i’ succeeds, False if task round ‘i’ fails；
@proposition(E)
class TaskSuccess:
    def __init__(self, round_num):
        self.round_num = round_num
    
    def __repr__(self):
        return f"K_i{self.round_num}"

#M_ij: In task ‘i’, True if player ‘j’ votes to accept, False if player ‘j’ votes to reject.
@proposition(E)
class PlayerVote:
    def __init__(self, round_num, player_name):
        self.round_num = round_num
        self.player_name = player_name
    
    def __repr__(self):
        return f"M{self.round_num}{self.player_name}"

#R_ij: player ‘j’ attend task round ‘i’
@proposition(E)
class PlayerAttendance:
    def __init__(self, round_num, player_name):
        self.round_num = round_num
        self.player_name = player_name
    
    def __repr__(self):
        return f"R{self.round_num}{self.player_name}"

#G_j: True if player ‘j’ is good person, False if not 
@proposition(E)
class PlayerGoodness:
    def __init__(self, player_name):
        self.player_name = player_name

    def __repr__(self):
        return f"G{self.player_name}"
        
#Pi: round ‘i’ is playing.
@proposition(E)
class Current_round:
    def __init__(self, round_num):
        self.round_num = round_num

    def __repr__(self):
        return f"P{self.round_num}"

#Sj: Represents suspicion that a player with the name "name" is a spy.
@proposition(E)
class Suspicion:
    def __init__(self, player_name):
        self.player_name = player_name

    def __repr__(self):
        return f"S{self.player_name}"
    
#Dj: player ‘j’ has been identified as a spy.
@proposition(E)
class Spy:
    def __init__(self, player_name):
        self.player_name = player_name

    def __repr__(self):
        return f"D{self.player_name}"



# Step one: initializing
members = ['A', 'B', 'C', 'D', 'E']  
suspicions = 0  # 初始化怀疑次数
success_count = 0  # 任务成功次数
i_max = 18  # 总游戏轮次

roles = {'spies': set(random.sample(members, 2)), 'good': set()}  # 随机指定两名间谍，剩下为好人
for member in members:
    if member not in roles['spies']:
        roles['good'].add(member)


# 函数
def number_players(i)
    if i % 2 == 1:
        participants = random.sample(members, 3)      # 单数轮选三个
        return participants
    else:
        participants = random.sample(members, 2)      # 双数轮选两个
        return participants

def vote(participants):
    votes = {'success': True}
    for member in participants:
        if member in roles['spies']:
            # 间谍随机投票，有一定几率投反对票
            vote = random.choice([True, False])
            if not vote:
                votes['success'] = False
                break
    return votes['success']

def update_suspicions(participants, vote_result):
    if not vote_result:
        for member in participants:
            suspicions[member] += 1

def vote_out(round_number):
    if round_number in [6, 12]:
        # 找出怀疑次数最高的成员
        most_suspected = max(suspicions, key=suspicions.get)
        # 投票出局，无法参加接下来的6轮游戏
        for i in range(1, 7):
            if round_number + i <= rounds:
                members.remove(most_suspected)
        # print(f"Round {round_number}: Member {most_suspected} is voted out.")

# 主程序
for i in range(1, rounds + 1):      # i = 第几轮
    participants = assign_task(i)
    vote_result = vote(participants)
    update_suspicions(participants, vote_result)
    if vote_result:
        task_success_count += 1
    if round_number in [6, 12]:
        vote_out(round_number)




# # Build an example full theory for your setting and return it.
# #
# #  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
# #  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
# #  what the expectations are.
# player_name = ["Alice", "Bob", "Chris", "David", "Eric"]
# MAX_ROUNDS = 1000
# round_num = i

# def example_theory():
#     for i in range(1, MAX_ROUNDS + 1):
#         if i % 2 == 1:
#             indexes = random.sample(range(5), 3)
#             j1 = players[indexes[0]]
#             j2 = players[indexes[1]] 
#             j3 = players[indexes[2]]
#             E.add_constraint((R(round_num[i],player_name[j1]) & R(round_num[i],player_name[j2]) & R(round_num[i],player_name[j3]))
#         else:
#             indexes = random.sample(range(5), 2)
#             j4 = players[indexes[0]]
#             j5 = players[indexes[1]] 
#             E.add_constraint(R(round_num[i],player_name[j4]) & R(round_num[i],player_name[j5]))
    
#     # The success of the task requires the acceptance of all members participating in the task
#     E.add_constraint((Mij(j) & Mij(j) & Mij(j)) >> Ki(i))
#     E.add_constraint((Mij(j) & Mij(j)) >> Ki(i))
    
#     # Failure of the task means that there must be a spy among the members participating in the task
#     E.add_constraint(~Ki(i) >> (~Mij(j) | ~Mij(j) | ~Mij(j)))

#     # Good people can only vote for acceptance.
#     E.add_constraint(Gj(j) >> Mij(j))

#     # Spies can vote to accept or reject.
#     E.add_constraint((~Gj(j) >> Mij(j)) | (~Gj(j) >> ~Mij(j)))

#     # No one can participate in more than two tasks in a row
#     E.add_constraint(~(Ri(j) & Ri_plus_1(j=j, i_plus_1=i+1) & Ri_plus_2(j=j, i_plus_2=i+2)))

#     # The spy cannot vote “accept” two consecutive rounds of task
#     E.add_constraint(~Gj(j) >> ~(Mij(j) & Mi_plus_1j(j=j, i_plus_1=i+1)))

#     # If player ‘j’ has been identified as a spy, player j can not attend the following task.
#     E.add_constraint(~(Dj(j) & Pi_plus_1(i_plus_1=i+1)))

#     # If the task the player is on fails, they will be suspected
#     E.add_constraint((~Ki(i) & Ri(j)) >> Sj(j))

#     # Suspect identified as a good guy, no longer suspected after three consecutive successful tasks
#     E.add_constraint(Sj(j)& Ki(i) & Ki_plus_1(i+1) & Ki_plus_2(i+2) >> Gj(j)) 
    
#     # If the suspect is included in the voting in the next round, but the result of this round of voting is mission success, then this suspect will be temporarily cleared of suspicion
#     E.add_constraint((Ki_plus_1(i_plus_1=i+1) & Ri_plus_1(j=j, i_plus_1=i+1)) >> ~Sj(j))
    
    
    














if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
