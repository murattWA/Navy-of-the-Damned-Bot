import random


class Ship():
    """Handles all game logic. both players get 2 boats. each boat is 1 unit wide due to discord api limits"""

    def __init__(self):
        pass

    # TODO add self.mode as a attribute to for game logic to know its playing as an ai
    
    def start_game(self, member: str):
        """creates new game against arg: member

        Args:
            member (str): set to p2 in game if member is == to bot name then p2 will be treated as ai. aka random guesser because its easier :D
        """

        self.member = member.lower()
        if self.member == "navyofthedamnedbot":
            # start game against ai
            pass
        else:
            # start game against member
            self.p1 = Board()
            self.p2 = Board()
        pass

    # TODO game logic will go in here as methods attack(), check_winner(), etc.
    
class Board():
    """Handles all board logic. dont use 'board' as instance name since thats used in the class. new_board() is called on init."""

    def __init__(self):
        self.new_board()

    def new_board(self):
        """IMPORTANT: when accessing or using x,y coord in self.board remember that its y first then x
        
        Sets: new board and ship positions
        
        Example:
        for cood (1,2) you would use self.board[2][1]
        """
        # player board and ships
        self.board = [[' ' for x in range(3)] for y in range(3)]
        self.ship1 = self.gen_cord()
        self.ship2 = self.gen_cord(self.ship1)
        self.board[self.ship1[1]][self.ship1[0]] = "X"
        self.board[self.ship2[1]][self.ship2[0]] = "X"

    def gen_cord(self, *exclude: list) -> list:
        """generates random list len=2 to be used as x,y coors for board piece placement.

        Inputs:
            list: unlimited list values. these lists will be ignored in generation logic

        Returns:
            list: returns a list that is unique compared to *exclude args
        """

        l = [random.randint(0, 2), random.randint(0, 2)]
        while l in exclude:
            l = [random.randint(0, 2), random.randint(0, 2)]
        return l

