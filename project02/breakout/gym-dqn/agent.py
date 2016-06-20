from replay_memory import ReplayMemory
from model import Model
import numpy as np

class Agent():

    def __init__(self, n_actions):
        self.n_actions = n_actions
        self.ep_start = 1
        self.ep = self.ep_start
        self.ep_end = self.ep
        self.ep_endt = 1000000
        self.max_reward = 1
        self.min_reward = 1
        self.valid_size = 500
        self.discount = 0.99
        self.update_freq = 1
        self.n_replay = 1
        self.learn_start = 2000 #50000
        self.hist_len = 1
        self.bestq = 0
        self.nonTermProb = 1
        self.buffer_size = 512
        self.num_steps = 0
        self.last_state = None
        self.last_action = None
        self.v_avg = 0
        self.tderr_avg = 0
        self.q_max = 1
        self.r_max = 1
        self.rescale_r = 1
        self.state_dim = 84*84
        self.replay_memory = ReplayMemory(n_actions)
        self.target_q_net = Model()

    def sample_validation_data(self):
        s,a,r,s2,term = self.replay_memory.sample(self.valid_size)
        self.valid_s = np.copy(s)
        self.valid_a = np.copy(a)
        self.valid_r = np.copy(r)
        self.valid_s2 = np.copy(s2)
        self.valid_term = np.copy(term)
    
    def preprocess(self, state):
        return state.copy().reshape(self.state_dim)     
    
    #FIX TESTING_EP. It should not be 1
    def perceive(self, reward, state, terminal, testing=False, testing_ep=1):
        state = self.preprocess(state)
        
        if self.max_reward:
          reward = min(reward, self.max_reward) #check paper

        if self.min_reward:
          reward = max(reward, self.min_reward)

        if self.rescale_r:
          self.r_max = max(self.r_max, reward)

        self.replay_memory.add_recent_state(state, terminal)
        current_full_state = self.replay_memory.get_recent()

        if not (self.last_state is None) and (not testing):
          self.replay_memory.add(self.last_state, self.last_action, reward, self.last_terminal)

        if self.num_steps == self.learn_start + 1 and not testing:
          self.sample_validation_data()

        curr_state = self.replay_memory.get_recent()

        action_index = 0
        if not terminal:
          action_index = self.e_greedy(curr_state)

        self.replay_memory.add_recent_action(action_index)

        if self.num_steps > self.learn_start and not testing and self_num_steps % self.update_freq == 0:
            self.q_learn_minibatch()

        if not testing:
          self.num_steps += 1

        self.last_state = np.copy(state)
        self.last_action = action_index
        self.last_terminal = terminal

        if not terminal:
          return action_index
        else:
          return -1

    def e_greedy(self, state):
        ep_test = (self.ep_end + max(0, (self.ep_start - self.ep_end)*(self.ep_endt - max(0, self.num_steps - self.learn_start))/self.ep_endt))
        if np.random.uniform(0,1) < ep_test:
          return np.random.randint(self.n_actions)
        else:
          return self.greedy(state)

    def greedy(self, state):
        q = self.network.forward(state)
        maxq = q[0]
        besta = [0]
        for a,v in enumerate(q):
          if v > maxq:
            besta = [a]
            maxq = v
          #can I compare float like that o_O. It's from google!
          elif v == maxq:
            besta.append(a)
        self.bestq = maxq
        self.last_action = random.choice(besta)
        return self.last_action


    def get_q_update(self):
        # delta = r + (1-terminal)*gamma*max_a Q(s2, a) - Q(s,a)

        term = term.clone().float().mul(-1).add(1)

        # max_a Q(s2,a)
        q2_max = target_q_net.forward(s2).float().max(2)

        #compute q2 = (1-terminal) * gamma * max_a Q(s2, a)
        q2  = q2_max * self.discount * term

        delta = r.clone()
        delta.add(q2)

        q_all = self.network.forward(s)
        q = np.zeros(q_all.shape[0])

        for i in range(0, q_all.shape(1)):
         q[i] = q_all[i][a[i]]
        delta.add(-1,q)

        targets = np.zeros(self.minibatch_size, self.n_actions, dtype=np.float)
        for i in range(math.min(self.minibatch_size, a.shape(1))):
         targets[i][a[i]] = delta[i]

        return targets, delta, q2_max

    def q_learn_minibatch(self):
        #w += alpha * (r + gamma max Q(s2, a2) - Q(s, a)) * dQ(s,a) / dw
        s, a, r, s2, term = self.replay_memory.sample(self.minibatch_size)

        targets, delta, q2_max = self.get_q_update(s, a, r, s2, term, update_qmax=True)

        self.dw.zero()
        self.network.backward(s, targets)

        self.dw.add(-self.wc, self.w)

        t = math.max(0, self.num_steps - self.learn_start)
        self.lr = (self.lr_start - self.lr_end) * (self.lr_endt - t)/self.le_endt+ self.lr_end
        self.lr = math.max(self.lr, self.lr_end)

        #use gradients
        self.g*0.95+0.05*self.dw
        tmp = self.dw * self.dw
        self.g2*0.95+0.05*tmp
        tmp*self.g*self.g
        tmp*=-1
        tmp += self.g2
        tmp += 0.01
        tmp = np.sqrt(tmp)

        #accumulate update
        self.w += np.divide(self.dw, tmp)*self.lr
