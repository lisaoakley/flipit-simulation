import gym
import gym_flipit
import numpy as np
import pprint
from experiments.strategies import GreedyWrapper,Q,Renewal,PeriodicOptimal

class Simulation:
    # debug (bool): print info during play
    # p1_strategy (str): agent strategy (q-table, greedy, optimal-periodic, renewal)
    # p1_config (dict): config values for agent (values depend on strategy)
    # p1_cost (non-negative int): move cost for p1
    # p0_strategy (str): renewal opponent strategy (periodic, exponential, normal, uniform)
    # p0_config (dict): parameters for renewal opponent's distribution
    # p0_cost (non-negative int): move cost for p0
    # duration (int): game duration in ticks
    # rew_type (string): name of reward type used in gym env (constant_minus_cost_norm, constant_minus_cost, LM_benefit, exponential, reciprocal, constant_reciprocal, constant, exp_cost, LM_avg)
    # rew_config (dict): parameters for chosen reward type
    # obs_type (string): name of observation scheme used in gym env (opp_LM,own_LM,composite)
    # run_id (any): identifier for given run (OPTIONAL)

    def run(self,debug,outfile,p1_strategy,p1_config,p1_cost,p0_strategy,p0_config,p0_cost,duration,rew_type,rew_config,obs_type,run_id=0):
        # set up environment and players
        env = gym.make('Flipit-v0')
        if rew_type == 'constant_minus_cost_norm'
            rew_config['val'] = p0_config['avg_mv']
        env.config(obs_type,rew_type,rew_config,p0_strategy,p0_config,duration,p0_cost,p1_cost)
        observation = env.reset()
        a = self.gen_attacker(p1_strategy,env,p1_config,p1_cost,debug)
        
        # print info
        if debug:
            print('---\nRun {}'.format(run_id))
            print('attacker config ({}):'.format(p1_strategy))
            print('attacker rew type:',rew_type)
            print('attacker cost:', p1_cost)
            pprint.pprint(p1_config)
            print('defender config ({}):'.format(p0_strategy))
            pprint.pprint(p0_config)

        # run simulation
        for tick in range(duration):
            prev_observation = observation
            action = a.pre(tick,prev_observation,i)
            observation, reward, done, info = env.step(action)
            a.post(tick,prev_observation,observation,reward,action,info['true_action'])
            if done:
                if debug:
                    print('\n---\n{}: episode {} completed.'.format(all_configs['run_id'],i))
                    print('Attacker: {}\nDefender:{}'.format(all_configs['p1_strategy'],all_configs['p0_strategy']))
                    print('Total p1 benefit: {}'.format(all_configs['p1_avg_benefit']))
                    print('Total p0 benefit: {}'.format(all_configs['p0_avg_benefit']))
                    print(env.player_moves[0])
                    print(env.player_moves[1])
                    print("\n\n\n")
                break

    def gen_attacker(self,s,env,p1_config,p1_cost,debug):
        if 'greedy' in s:
            return GreedyWrapper.GreedyWrapper(env.p0,p1_cost,debug=debug)
        elif 'q-table' in s:
            return Q.Q(env.action_space.n,p1_config,debug=debug)
        elif 'optimal-periodic' in s:
            return PeriodicOptimal.PeriodicOptimal(env.p0, p1_cost)
        elif 'renewal' in s:
            return Renewal.Renewal(s)
        else:
            raise NotImplementedError
