class PeriodicOptimal:
    def __init__(self,p0,move_cost,debug=False):
        self.dropped = False
        self.strategy = 'optimal-periodic'
        self.debug = debug
        self.delta = p0.delta
        self.next_move = self.delta
        if move_cost >= self.delta:
            self.dropped = True
            self.next_move = -1

    def pre(self,tick,prev_observation,episode):
        action = 0
        if tick != 0 and tick == self.next_move and not self.dropped:
            action = 1
        return action

    def post(self,tick,prev_observation,observation,reward,action):
        if action == 1:
            self.next_move = tick - observation + self.delta + 1
