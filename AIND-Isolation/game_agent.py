"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """
    THis function evaluates the player's position. If the player is 
    closer to the centre of the board, they have a higher probability of 
    winning. THis central position is evaluated against the opponent's
    central position. Ensuring we have a centrally position advantage.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    
    # Check if game is won
    if game.is_winner(player):
        return float("inf")

    # Check is game is lost
    elif game.is_loser(player):
        return float("-inf")

    # Identify the center x and y co-ordinates for the board
    w, h = game.width / 2., game.height / 2.

    # Identify the co-ordinates of both players
    y_player, x_player = game.get_player_location(player)
    opp_player, opp_player = game.get_player_location(player)

    player_distance = abs(y_player - h) + abs(x_player - w)
    opp_distance = abs(opp_player - h) + abs(opp_player - w)

    # return the score for difference of
    # the distance between the opponent and player's distance 
    # from the center

    return float(opp_distance - player_distance)/10



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_winner(player):
        return float("inf")
    elif game.is_loser(player):
        return float("-inf")

    # We have moves to play. How many more than our opponent?
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves*2)
    


def custom_score_3(game, player):
    """

    This heuristic incorporates both custom_score and custom_score_2 to
    form a superior heuristic. As a player human player may not always 
    use one strategy.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_winner(player):
        return float("inf")
    elif game.is_loser(player):
        return float("-inf")

    weighted_score = 0.1 * custom_score(game, player) + 0.5 * custom_score_2(game, player) + 0.4 * float(len(game.get_legal_moves(player)))

    # We have moves to play. How many more than our opponent?
    return float(weighted_score)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def max_value(self, game, depth):

        """
        Obtain the maximized value for a given state
            Parameters
            ----------
            game : isolation.Broad
                An instance of the Isolation game 'Board' class representing
                the current state
            
            depth : int
                Depth is an integer representing the maximum number of plies
                to search in the game tree before aborting

            Returns
            -------
            float
                the maximized value

        """

        # check for timeout
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Retrieve legal moves for active player
        legal_moves = game.get_legal_moves()

        # Check for game termination
        if not legal_moves:
            return game.utility(self)

        # Check for depth termination
        if depth <= 0:
            return self.score(game,self)

        score = float("-inf")
        for move in legal_moves:
            next_state = game.forecast_move(move)
            score = max(score, self.min_value(next_state, depth- 1))
        return score

    def min_value(self, game, depth):
        """
        Obtain the minimized value for a given state
            Parameters
            ----------
            game : isolation.Broad
                An instance of the Isolation game 'Board' class representing
                the current state
            
            depth : int
                Depth is an integer representing the maximum number of plies
                to search in the game tree before aborting

            Returns
            -------
            float
                the minimized value

        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Retrieve legal moves for active player
        legal_moves = game.get_legal_moves()

        # Check for game termination
        if not legal_moves:
            return game.utility(self)

        # Check for depth termination
        if depth <= 0:
            return self.score(game,self)

        score = float("inf")
        for move in legal_moves:
            next_state = game.forecast_move(move)
            score = min(score, self.max_value(next_state, depth-1))
        return score


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Retrieve legal moves for active player
        legal_moves = game.get_legal_moves()

        # Check for game termination
        if not legal_moves:
            return game.utility(self)

        # Check for depth termination
        if depth <= 0:
            return self.score(game,self)

        best_score = float("-inf")
        best_action = None
        score = None
        # implement mini-max algorithm
        for move in legal_moves:
            next_state = game.forecast_move(move)
            score = self.min_value(next_state, depth-1)
            if score > best_score:
                best_score, best_action = score, move

        return best_action

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        """
        find the best legal move using
        MinimaxPlayer.minimax() or AlphaBetaPlayer.alphabeta()
        """

        legal_moves = game.get_legal_moves()
        if legal_moves:

            # include variation in moves
            best_move = legal_moves[random.randint(0,(len(legal_moves)-1))]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            # Iterative deepening
            depth = 0
            while True:
                best_move = self.alphabeta(game, depth)
                if best_move == float("-inf") or best_move == float("inf"):
                    break
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed
            

        # Return the best move from the last completed search iteration
        return best_move


    def max_alphabeta(self, game, depth, alpha, beta):
        """
        Obtain the maximized value for a given state
            Parameters
            ----------
            game : isolation.Broad
                An instance of the Isolation game 'Board' class representing
                the current state
            
            depth : int
                Depth is an integer representing the maximum number of plies
                to search in the game tree before aborting

            alpha : float
                Limits the lower bound of the search on minimizing
                layers

            beta : float
                Limits the upper bound of the search on minimizing
                layers

            Returns
            -------
            float
                the maximized value

        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        # if not legal_moves:
        #     return game.utility(self)

        if depth == 0:
             return self.score(game, self)

        best_score = float("-inf")

        for move in legal_moves:
            next_state = game.forecast_move(move)
            score = self.min_alphabeta(next_state, depth - 1, alpha,beta)

            best_score = max(best_score, score)

            # Prune branches greater than beta
            if best_score >= beta:
                return best_score
            alpha = max(alpha, best_score)
                
        return best_score

    def min_alphabeta(self, game, depth, alpha, beta):
        """
        Obtain the minimized value for a given state
            Parameters
            ----------
            game : isolation.Broad
                An instance of the Isolation game 'Board' class representing
                the current state
            
            depth : int
                Depth is an integer representing the maximum number of plies
                to search in the game tree before aborting

            alpha : float
                Limits the lower bound of the search on minimizing
                layers

            beta : float
                Limits the upper bound of the search on minimizing
                layers

            Returns
            -------
            float
                the minimized value

        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

         # Check for game termination
        legal_moves = game.get_legal_moves()

        # if not legal_moves:
        #     return game.utility(self)

        if depth == 0:
            return self.score(game,self)

        best_score = float("inf")

        for move in legal_moves:
            next_state = game.forecast_move(move)
            score = self.max_alphabeta(next_state, depth - 1, alpha, beta)
            best_score = min(best_score, score)
            # Prune branches greater than alpha
            if best_score <= alpha:
                return best_score
            beta = min(beta, best_score)
                

        return best_score

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimising layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if not legal_moves:
            return game.utility(self)

        if depth == 0:
            return self.score(game,self)

        best_score = float('-inf')
        
        best_move = legal_moves[random.randint(0,len(legal_moves))-1]

        for move in legal_moves:
            next_state = game.forecast_move(move)
            score = self.min_alphabeta(next_state,depth-1, alpha, beta)
            if score >= best_score:
                best_score, best_move = score, move
            # prune if above beta
            if best_score >= beta:
                return best_move

            #update alpha when necessary
            alpha = max(alpha, best_score)

        return best_move
