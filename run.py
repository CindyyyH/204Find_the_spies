
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
    
#Vij:After round i, player j is voted on.
@proposition(E)
class Vote:
    def __init__(self, round_num, player_name):
        self.round_num = round_num
        self.player_name = player_name
    
    def __repr__(self):
        return f"V{self.round_num}{self.player_name}"





# Step one: initializing
members = ['A', 'B', 'C', 'D', 'E']  
suspicions = 0  
success_count = 0  
i_max = 18  # maximum round

roles = {'spies': set(random.sample(members, 2)), 'good': set()}  # randomly chooses two spies
for member in members:
    if member not in roles['spies']:
        roles['good'].add(member)


# 函数
def number_players(i)
    if i % 2 == 1:
        participants = random.sample(members, 3)      # 3 players in odd round
        return participants
    else:
        participants = random.sample(members, 2)      # 2 players in even round
        return participants

def vote(participants):
    votes = {'success': True}
    for member in participants:
        if member in roles['spies']:
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
        most_suspected = max(suspicions, key=suspicions.get)
        # players who get voted out cannot partcipate in next six rounds
        for i in range(1, 7):
            if round_number + i <= rounds:
                members.remove(most_suspected)
        # print(f"Round {round_number}: Member {most_suspected} is voted out.")

# Main
for i in range(1, rounds + 1):      # i = nth round
    participants = assign_task(i)
    vote_result = vote(participants)
    update_suspicions(participants, vote_result)
    if vote_result:
        task_success_count += 1
    if round_number in [6, 12]:
        vote_out(round_number)

# result
if task_success_count > 9:
    print("mission success, spies lose")
else:
    print("mission failure, spies win")

# Vote out two spies based on the number of suspicions.
sorted_suspicions = sorted(suspicions.items(), key=lambda item: item[1], reverse=True)
suspected_spies = sorted_suspicions[:2]
print("the most suspected member：", suspected_spies)

# check if the suspected members are really spies
actual_spies = roles['spies']
correctly_identified_spies = all(member in actual_spies for member, _ in suspected_spies)
if correctly_identified_spies:
    print("spy has been voted out")
else:
    print("someone was mistakenly identified as spies")





# Build an example full theory for your setting and return it.
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

player_name = ["Alice", "Bob", "Chris", "David", "Eric"]
MAX_ROUNDS = 18
round_num = i

def example_theory():
    for i in range(1, rounds + 1):
        if i % 2 == 1:
            indexes = random.sample(range(len(player_names)), 3)
            j1 = player_names[indexes[0]]
            j2 = player_names[indexes[1]]
            j3 = player_names[indexes[2]]
            E.add_constraint((PlayerAttendance(i, j1) & PlayerAttendance(i, j2) & PlayerAttendance(i, j3)))
        else:
            indexes = random.sample(range(len(player_names)), 2)
            j4 = player_names[indexes[0]]
            j5 = player_names[indexes[1]]
            E.add_constraint(PlayerAttendance(i, j4) & PlayerAttendance(i, j5))

        for j in player_names:
            # Good people can only vote for acceptance.
            E.add_constraint(G(j) >> M(j, i))
            # Spies can't vote in favor for two consecutive rounds
            E.add_constraint(~G(j) >> ~(M(j, i) & M(j, i - 1)))
            # Spies can vote to accept or reject.
            E.add_constraint((~G(j) >> M(j, i)) | (~G(j) >> ~M(j, i)))
            # No one can participate in more than two tasks in a row
            E.add_constraint(~(R(j, i) & R(j, i - 1) & R(j, i - 2)))
            # If the task the player is on fails, they will be suspected
            E.add_constraint((R(j, i) >> ~K(i)) >> S(j))
           
            # At the end of rounds 6 and 12, the voted member cannot participate in the next 6 rounds of the game
            if i == 6 or i == 12:
                E.add_constraint(~(R(j, i + 1) & R(j, i + 2) & R(j, i + 3) & R(j, i + 4) & R(j, i + 5) & R(j, i + 6)))
        # If the number of suspects is the same, one person will be randomly selected to vote.
        if i == 18:
            E.add_constraint(~(G(j) & G(j + 1)) >> (V(j, i) & V(j + 1, i)) >> F)

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
