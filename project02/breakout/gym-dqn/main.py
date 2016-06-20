import time as t
from agent import Agent
from environment import Environment

replay_mem_size = 1000000
train_start = 1231234341234 #TODO change
save_freq = 50000
eval_freq = 10000
eval_steps = 100000
train_steps  = 5000000
time_ctr = [0]
start_time = t.time()


if __name__ == '__main__':
  env = Environment()
  actions = env.env.action_space
  n_actions = actions.n
  done = False
  agent = Agent(n_actions)
  observation = env.reset()
  reward = 0

  for step in range(train_steps):
      step += 1
      #agend perceive here
      agent.perceive(reward, observation, done)
      action = actions.sample()
      #dump replay memory first
      if not done:
        observation, reward, done, info = env.step(action)
      else:
        observation = env.reset()
        reward = 0
        done = False

      env.render()

      if step % eval_freq == 0 and step > learn_start:

        #new game here
        total_reward = 0
        nrewards = 0
        nepisodes = 0
        episode_reward = 0
        for estep in range(eval_steps):
          agent.perceive(reward, observation, done)
          #persieve(reward, screen, terminal, True, 0.05)
          observation, reward, done, info = env.step(actions[action_index])
          episode_reward += reward
          if reward != 0:
            nrewards += 1

          if done:
            total_reward += episode_reward
            episode_reward = 0
            nepisodes += 1
            #nextRandomGame

        ind = len(reward_history)+1
        total_reward /= math.max(1, nepisodes)
        if len(reward_history) == 0 or total_reward > max(reward_history):
          agent.best_network = agent.network.clone()

        if agent.v_avg:
          v_history[ind] = agent.v_avg
          td_history[ind] = agent.tderr_avg
          qmax_history[ind] = agent.q_max

        reward_history = total_reward
        reward_counts[ind] = nrewards
        episode_counts[ind] = nepisodes


        eval_time = start_time - t.time()
        start_time += eval_time
        time_history[ind+1] = t.time() - start_time
        #check if time in lua in secs also
        time_histrory[ind+1] = t.time() - start_time
        learning_rate = eval_freq/time_dif




#TODO collect gabage
