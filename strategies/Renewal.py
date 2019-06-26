from gym_flipit.envs.strategies import periodic,exponential,uniform

class Renewal:
    def __init__(self,strategy):
        self.dropped = False
        self.strategy = strategy
        params = strategy.split('-')
        if 'periodic' in strategy:
            self.renewal = periodic.Periodic()
            self.config = {'delta':int(params[-1])}
        elif 'exponential' in strategy:
            self.renewal = exponential.Exponential()
            self.config = {'lambd':float(params[-1])}
        elif 'uniform' in strategy:
            self.renewal = uniform.Uniform()
            self.config = {'d':int(params[-2]),'u':int(params[-1])}
        else:
            raise ValueError('{} is not a valid Renewal strategy'.format(strategy))

    def pre(self,tick,prev_observation,episode):
        if tick == 0:
            self.renewal.config(self.config)
            self.next_move = self.renewal.first_move()
            if self.next_move == 0:
                self.next_move == 1
        if self.next_move == tick:
            return 1
        return 0

    def post(self,tick,prev_observation,observation,reward,action):
        if action == 1:
            self.next_move = self.renewal.move(tick)
            if self.next_move == tick:
                self.next_move += 1
