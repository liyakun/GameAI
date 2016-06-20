import cv2
import gym
#add inheritance
class Environment:

    def __init__(self):
        self.env = gym.make('Breakout-v0')
        #make params
        self.width = 84
        self.height = 84

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        cv2.cvtColor(observation, cv2.COLOR_RGB2GRAY)/255
        observation = cv2.resize(cv2.cvtColor(observation, cv2.COLOR_RGB2GRAY)/255, (self.width, self.height))
        return observation, reward, done, info

    def reset(self):
        return cv2.resize(cv2.cvtColor(self.env.reset(), cv2.COLOR_RGB2GRAY)/255, (self.width, self.height))

    def render(self):
        return self.env.render()

    def new_game(self):
        return self.env.new_game()
