from ship import Ship

board = """```
      -------------------------      
    -/                         \-    
  -/          Your Ships         \-  
-/   +-------------------------+   \-
|    |       |         |       |    |
|    |   1   |    2    |   3   |    |
|    |       |         |       |    |
|    | ----------------------- |    |
|    |       |         |       |    |
|    |   4   |    5    |   6   |    |
|    |       |         |       |    |
|    | ----------------------- |    |
|    |       |         |       |    |
|    |   7   |    8    |   9   |    |
|    |       |         |       |    |
|    +-------------------------+    |
|                                   |
-------------------------------------
```"""

# this is how you would replace the numbers with ship locations
cords = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
i = iter(cords)

game_on = True
ship = Ship()
ship.start_game("mo")
hits = ship.p1.board
ship.p1.print_board(hits=False)

print(hits)
for row in hits:
    for spot in row:
        num = next(i)
        if spot == "X":
            board = board.replace(num, "X")
        else:
            board = board.replace(num, " ")
print(board)