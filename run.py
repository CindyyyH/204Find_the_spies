
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

players = ["Alice", "Bob", "Chris", "David", "Eric"]

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


# Call your variables whatever you want
# Basic Propositions for players
    alice = BasicPropositions("a")  
    bob = BasicPropositions("b")    
    chris = BasicPropositions("c")   
    david = BasicPropositions("d")   
    eric = BasicPropositions("e")   
    
    # Round being played
    Pi = FancyPropositions("Pi")
    
    # Task result (successful or not)
    Ki = FancyPropositions("Ki")
    
    # Suspicion of player being a spy
    Sa = FancyPropositions("Sa")
    Sb = FancyPropositions("Sb")
    Sc = FancyPropositions("Sc")
    Sd = FancyPropositions("Sd")
    Se = FancyPropositions("Se")
    
    # Player identified as a spy
    Da = FancyPropositions("Da")
    Db = FancyPropositions("Db")
    Dc = FancyPropositions("Dc")
    Dd = FancyPropositions("Dd")
    De = FancyPropositions("De")

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.








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
