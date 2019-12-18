from strategies import Greedy

class GreedyWrapper:
    def __init__(self,p0,move_cost,debug=False):
        self.dropped = False
        self.strategy = 'greedy'
        self.move_cost = move_cost
        self.debug = debug
        self.strat = Greedy.Greedy(self.move_cost, 1, p0, debug, guess=10)
        self.next_move = self._first_move()

    def _first_move(self):
        return round(self.strat.first_move(0)) + 1

    def pre(self,tick,prev_observation,episode):
        action = 0
        if tick != 0 and tick == self.next_move and not self.dropped:
            action = 1
        return action

    def post(self,tick,prev_observation,observation,reward,action,true_action):
        if action == 0 and true_action == 0:
            return
        if tick == 0 or tick == observation-1 or observation < 0:
            self.next_move = self.strat.first_move(self.next_move)
        else:
            self.next_move = self.strat.move(tick,observation)
        if self.next_move == 'drop out':
            self.dropped == True
            self.next_move = -1
            return
        self.next_move = round(self.next_move)
        if self.next_move == tick:
            self.next_move += 1
