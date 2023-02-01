import random

from ascii import ascii_board2


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


class Board():
    """Handles all board logic. dont use 'board' as instance name since thats used in the class. new_board() is called on init. note that self.board stores your boats and enemy missile location. whereas self.hits stores only where you've sent missiles to already."""

    def __init__(self):
        self.new_board()
        self.gen_ascii()

    def new_board(self):
        """IMPORTANT: when coding self.board remember that its y first then x, but when accessing self.board or update_board() its user-friendly x is first then y.
        
        Sets: new board & hits table and ship positions
        
        Example:
        for cord (1,2) you would use self.board[2][1]
        """
        # player board and ships
        self.board = [[' ' for x in range(3)] for y in range(3)]
        self.hits = [[' ' for x in range(3)] for y in range(3)]
        self.ship1 = self.gen_cord()
        self.ship2 = self.gen_cord(self.ship1)
        self.board[self.ship1[1]][self.ship1[0]] = "X"
        self.board[self.ship2[1]][self.ship2[0]] = "X"

    def update_board(self, symbol: str, hits: bool, *cords: list) -> bool:
        """Update self.board and self.hits(if hits is True) to a particular "symbol" at a particular "cord." 
        
        returns Bool hit if a ship was in any of the provided cords. You can update as many cords as you want in one function but all will be updated to only one symbol. likewise with the return only one return will be provided even if multiple ships were hit. for more granularity use separate functions for separate cords.

        Args:
            symbol (str): the symbol you would like to place at cord.
            hits (bool): set True if you would like to update self.hits
            *cord (list): the cords you would like to update to symbol

        Returns:
            bool: hit true or false if any ship was hit only if updating self.board. will still return false if updating self.hits. use the return for when updating self.hits to put a different marker if a ship was hit
        """

        hit = False
        for cord in cords:
            if hits:
                self.hits[cord[1]][cord[0]] = symbol
            else:
                if self.board[cord[1]][cord[0]] == "X":
                    hit = True
                    self.board[cord[1]][cord[0]] = symbol
                else:
                    self.board[cord[1]][cord[0]] = "*"
        self.gen_ascii()
        return hit

    def gen_cord(self, *exclude: list) -> list:
        """generates random list len=2 to be used as x,y coors for board piece placement. keep in mind you should store your exclusions in a list and pass that unpacked list.
        
        Example:
            exclusions = [[0,0],[0,1],[0,2]]
            gen_cord(*exclusions)
            it is important to use "*"

        Inputs:
            list: unlimited list values. these lists will be ignored in generation logic

        Returns:
            list: returns a list that is unique compared to *exclude args
        """
        l = [random.randint(0, 2), random.randint(0, 2)]
        while l in exclude:
            l = [random.randint(0, 2), random.randint(0, 2)]
        return l

    def check_winner(self) -> bool:
        """iterates over each row in self.board to check if "X" in row. if it finds "X" it breaks loops and returns False. if it reaches the end of self.board and doesnt find "X" then returns True

        Returns:
            bool: True = winner
        """

        for row in self.board:
            if "X" in row:
                return False
        return True

    def print_board(self, hits: bool = False):
        """Prints the game board if hits = (False by default) or hits board if hits = True row by row so it looks like an array. use this if your playing the game in cmd or something. or debuging like me :D
        """

        if hits:
            for row in self.hits:
                print(row)
        else:
            for row in self.board:
                print(row)

    def gen_ascii(self, board=None):
        """Generates a new ascii board using ascii_board which is accessable via self.ascii. this is run automatically on init and update_board().

        Args:
            board, optional: if not specified Defaults to None and will use current instance of self.board.
        """

        if board == None:
            board = self.board

        # cords are placeholders in the ascii image to be replaced
        cords = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        icords = iter(cords)
        self.ascii = ascii_board2

        for row in board:
            for spot in row:
                num = next(icords)
                if spot == "X":  # ship
                    self.ascii = self.ascii.replace(num, "X")
                elif spot == "/":  # sunken ship
                    self.ascii = self.ascii.replace(num, "@")
                elif spot == "*":  # miss
                    self.ascii = self.ascii.replace(num, "*")
                else:  #emply space
                    self.ascii = self.ascii.replace(num, " ")