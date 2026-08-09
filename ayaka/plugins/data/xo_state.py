class XOGame:
    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
        (0, 4, 8), (2, 4, 6),              # diagonals
    ]

    def __init__(self):
        self.active = False
        self.player_x: int | None = None
        self.player_o: int | None = None
        self.board: list[str] = [" "] * 9
        self.turn: int | None = None

    def start(self, x_id: int, o_id: int) -> None:
        self.active = True
        self.player_x = x_id
        self.player_o = o_id
        self.board = [" "] * 9
        self.turn = x_id  # X always moves first

    def reset(self) -> None:
        self.__init__()

    def symbol_for(self, user_id: int) -> str | None:
        if user_id == self.player_x:
            return "X"
        if user_id == self.player_o:
            return "O"
        return None

    def opponent_of(self, user_id: int) -> int | None:
        if user_id == self.player_x:
            return self.player_o
        if user_id == self.player_o:
            return self.player_x
        return None

    def play(self, user_id: int, cell: int) -> bool:
        """Place this player's mark in `cell` (0-8). Returns False if it's
        not their turn or the cell is taken — caller should treat that as
        a no-op, not an error."""
        if user_id != self.turn:
            return False
        if not (0 <= cell <= 8) or self.board[cell] != " ":
            return False

        self.board[cell] = self.symbol_for(user_id)
        self.turn = self.opponent_of(user_id)
        return True

    def winner(self) -> str | None:
        """Returns 'X', 'O', or None if no winner yet."""
        for a, b, c in self.WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_draw(self) -> bool:
        return " " not in self.board and self.winner() is None

    def is_over(self) -> bool:
        return self.winner() is not None or self.is_draw()


XO_GAME = XOGame()
