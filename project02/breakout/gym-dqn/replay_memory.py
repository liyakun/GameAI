import numpy as np

class ReplayMemory():

    def __init__(self, n_actions):
        self.n_actions = n_actions
        self.empty()

        self.size = 0
        self.recent_a = []
        self.recent_t = []

        self.max_size = 1024*1024
        self.buffer_size = 1024
        self.zero_frames = 1
        self.non_term_prob = 1
        self.non_even_prob = 1
        self.num_entries = 0
        self.ins_index = 0
        self.state_dim = 84*84
        self.hist_len = 4
        self.hist_indices = [i for i in range(self.hist_len)]
        self.recent_mem_size = 4
        self.s_size = self.state_dim * self.hist_len
        self.recent_s = np.zeros((self.recent_mem_size, self.s_size))
        self.buf_a = np.zeros(self.buffer_size, dtype=np.long)
        self.buf_r = np.zeros(self.buffer_size)
        self.buf_term = np.zeros(self.buffer_size, dtype=np.int)
        self.buf_s = np.zeros((self.buffer_size, self.s_size))
        self.action_encodings = np.eye(self.n_actions)

        self.s = np.zeros((self.max_size, 7056))
        self.a = np.zeros(self.max_size)
        self.r = np.zeros(self.max_size)
        self.t = np.zeros(self.max_size)
        self.buf_ind = None

    def fill_buffer(self):
        assert(self.num_entries >= self.buffer_size)
        self.buf_ind = 0
        for buf_ind in range(self.buffer_size):   
            s,a,r,s2,term = self.sample_one()
            print(self.buf_s.shape)
            self.buf_s[buf_ind] = np.copy(s)
            self.buf_a[buf_ind] = a
            self.buf_r[buf_ind] = r
            self.buf_s2[buf_ind] = np.copy(s2)
            self.buf_term[buf_ind] = term

    #divide s/s2 by 255 here

    def sample_one(self, ):
        assert(self.num_entries > 1)
        valid = False
        while not valid:
            #start at 1 because of previous action
            index = np.random.randint(0, self.num_entries-self.recent_mem_size)
            if self.t[index+self.recent_mem_size - 1] == 0:
                valid = True
        return self.get(index)

    def sample(self, batch_size):
        assert(batch_size < self.buffer_size)
        if self.buf_ind is None or self.buf_ind + batch_size -1 > self.buffer_size:
            self.fill_buffer()

        i_fr = self.buf_ind
        i_to = i_fr + batch_size
        return self.buf_s[i_fr:i_to], self.buf_a[i_fr:i_to], self.buf_r[i_fr:i_to], self.buf_s2[i_fr:i_to], self.buf_term[i_fr:i_to]

    def concat_frames(self, index, use_recent=None):
    
        if use_recent is not None:
            s,t = self.recent_s, self.recent_t
        else:
            s,t = self.s, self.t

        #init array
        full_state = np.zeros((self.hist_len, s[0].shape[0]))
        zero_out = False
        episode_start = self.hist_len

        for i in range(self.hist_len - 2, -1, -1):
          if not zero_out:
            #check indices here lua uses 1 for first
            for j in range(index+self.hist_indices[i]-1, index+self.hist_indices[i+1]-2):
              if t[j] == 1:
                zero_out = True
                break

            if zero_out:
              fullstate[i] = np.zeros()
            else:
              episode_start = 0

        if self.zero_frames == 0:
          episode_start = 0

        for i in range(episode_start, self.hist_len):
          full_state[i] = np.copy(s[index+self.hist_indices[i]-1])
        return full_state

    def add(self, s, a, r, term):
        #increment untill full
        if self.num_entries < self.max_size:
          self.num_entries = self.num_entries + 1

        self.ins_index += 1

        if self.ins_index > self.max_size:
          self.ins_index = 1

        self.s[self.ins_index] = np.copy(s)
        self.a[self.ins_index] = a
        self.r[self.ins_index] = r
        if term:
          self.t[self.ins_index] = 1
        else:
          self.t[self.ins_index] = 0

    def concat_actions(self, index, use_recent):
        act_hist = torch.FloatTensor(self.hist_len, self.num_actions)
        if use_recent:
          a,t = self.recent_a, self.recent_c
        else:
          a, t = self.a, self.t

        zero_out = False
        episode_start = self.hist_len

        #check ranges
        for i in range(self.hist_len-1,-1,-1):
          if not zero_out:
            for j in range(index+self.hist_indices[i]-1, index+self.hist_indices[i+1]-2, -1):
              if t[j] == 1:
                zero_out = True
                break

          if zero_out:
            act_hist[i].zero()
          else:
            episode_start = i

        if self.zero_frames == 0:
          episode_start = 1

        for i in range(episode_start, self.hist_len):
          #one hot
          act_hist[i].copy(self.action_endcodings[a[index+self.hist_indices[i]-1]])

        return act_hist

    def empty(self):
        self.size = 0

    def reset(self):
        self.size = 0
        self.ins_ind = 0

    def get_recent(self):
        #Assumes that the most recent state has been added, but the action has not
        return self.concat_frames(1, True)

    def get(self, index):
        s = self.concat_frames(index)
        s2 = self.concat_frames(index+1)
        ar_index = index + self.recent_mem_size + 1
        return s, self.a[ar_index], self.r[ar_index], s2, self.t[ar_index+1]

    def add_recent_state(self, s, term):
        s = np.copy(s)

        if len(self.recent_s) == 0:
          for i in range(self.recent_mem_size):
            self.recent_s[i] = np.copy(s)
            self.recent_t.append(1)

        np.append(self.recent_s, s)
        if term:
          self.recent_t.append(1)
        else:
          self.recent_t.append(0)

        if len(self.recent_s) > self.recent_mem_size:
          np.delete(self.recent_s, -1)
          self.recent_t.pop(0)

    def add_recent_action(self, a):
        if len(self.recent_a) == 0:
          for i in range(self.recent_mem_size):
            self.recent_a.append(0)
        self.recent_a.append(a)

        #keep recentMemSize steps
        if len(self.recent_a) > self.recent_mem_size:
          #table.remove(self.recent_a, 1)
          pass
