import scipy as sp
from .ZCache import zkey
import scipy.integrate as integrate
import scipy.stats as stats
import scipy.optimize as optimize
import numpy as np
import random
import math
from cachetools import cached, TTLCache, keys

class Greedy:
    def __init__(self, move_cost, index, opponent, debug=False, method='BFGS', guess=0):
        self.index = index
        self.move_cost = move_cost
        self.debug = debug
        self.method = method
        self.opponent = opponent
        self.guess = guess
        if self.guess == 0:
            self.guess = self.move_cost

    def first_move(self, l_bound):
        if self.opponent.strategy == 'periodic':
            return self.opponent.delta
        self.guess += self.move_cost
        move = random.uniform(l_bound, l_bound+self.guess)
        if self.debug:
            print("p1 random move:", move)
        return round(move,2)

    def move(self, time, tau):
        if self.debug:
            print("p1 move: ", time)
            print("tau: ", tau)
            print("k_1: ", self.move_cost)
        opp_cdf = self.opponent.cdf(tau)
        sign = -1 # minimum of negative benefit is maximum of positive benefit
        if self.opponent.strategy == 'uniform':
            if tau <= self.opponent.u:
                c = 1/self.opponent.u
            elif tau >= self.opponent.delta - self.opponent.u/2:
                c = 1/(self.opponent.delta + (self.opponent.u/2) - tau)
            else:
                raise NotImplementedError
            z = math.sqrt((self.opponent.delta - (self.opponent.u/2)-tau)**2 + 2*self.move_cost/c)
            return round(time + z)
        if self.opponent.strategy == 'normal':
            self.guess = 100
        if self.opponent.strategy == 'periodic' and tau > 2:
            self.guess = self.opponent.delta - tau
        L = optimize.minimize(self.local_benefit_wrapper,self.guess,args=(tau,opp_cdf,sign),options={"maxiter":20}, method = self.method)
        if self.debug:
            print("Chosen:", L.x[0], L.fun * sign)
            print("minimization succeeded:", L.success)
            print("minimization iterations:", L.nit)
            print("minimization message:", L.message)
        if L.fun * sign >= 0:
            mv = round(time + round(L.x[0],2),2)
            if self.debug:
                print("p1 move:", mv)
                print(mv)
            self.guess = L.x[0]
            if self.opponent.strategy == 'periodic':
                self.guess = self.opponent.delta
            return mv
        print("Greedy (p{}) dropped out after time={}.".format(self.index,time))
        return 'drop out'


    def local_benefit_wrapper(self, z, tau, opp_cdf, sign=1):
        return self.local_benefit(round(z[0],8),tau,opp_cdf,sign)

    # @cached(TTLCache(maxsize=100, ttl=300),key=zkey)
    @cached(TTLCache(maxsize=100, ttl=300))
    def local_benefit(self, z, tau, opp_cdf, sign=1):
        L_z = (1 / z) * (integrate.quad(self.first_term, 0, z, args=(tau, opp_cdf))[0]
                         + (z * integrate.quad(self.pdf, z, np.inf, args=(tau, opp_cdf))[0])
                         - self.move_cost)
        if self.debug:
            print("Attempt [z], [L(z)]:", z, L_z)
        return L_z * sign

    def first_term(self, x, tau, opp_cdf):
        return x * self.pdf(x, tau, opp_cdf)

    def pdf(self, x, tau, opp_cdf):
        if opp_cdf == 1:
           opp_cdf == .9999999
        return self.opponent.pdf(tau + x) / (1 - opp_cdf)
