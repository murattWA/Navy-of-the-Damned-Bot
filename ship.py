import random


class Ship():
    """Handles all game logic. both players get 2 boats. each boat is 1 unit wide due to discord api limits"""

    def __init__(self):
        pass

    def start_game(self, member: str):
        self.member = member.lower()
        if self.member == "navyofthedamnedbot":
            # start game against ai
            pass
        else:
            # start game against member
            self.brd = Board()
        pass


# Board class could be made better and more universal by using a for loop but i feel this is easier to understand at a glance
class Board():
    """Handles all board logic. dont use 'board' as instance name since thats used in the class. new_board() is called on init."""

    def __init__(self):
        self.new_board()

    def new_board(self):
        """IMPORTANT: when accessing or using x,y coord in self.board remember that its y first then x
        
        Returns: new boards and ship positions for both players
        
        Example:
        for cood (1,2) you would use self.board[2][1]
        """
        # player 1 board and ships
        self.boardp1 = [[' ' for x in range(3)] for y in range(3)]
        self.p1ship1 = self.gen_cord()
        self.p1ship2 = self.gen_cord(self.p1ship1)
        self.boardp1[self.p1ship1[1]][self.p1ship1[0]] = "X"
        self.boardp1[self.p1ship2[1]][self.p1ship2[0]] = "X"

        # player 2 board and ships
        self.boardp2 = [[' ' for x in range(3)] for y in range(3)]
        self.p2ship1 = self.gen_cord()
        self.p2ship2 = self.gen_cord(self.p2ship1)
        self.boardp2[self.p2ship1[1]][self.p2ship1[0]] = "X"
        self.boardp2[self.p2ship2[1]][self.p2ship2[0]] = "X"

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


ship = Ship()
ship.start_game("Mo")
print(ship.member)
print(ship.brd.boardp1)
# for row in brd.boardp1:
#     print(row)
# print("-------")
# for row in brd.boardp2:
#     print(row)
