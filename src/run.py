# -*- coding: utf-8 -*-
#
# Written by Matthieu Sarkis, https://github.com/MatthieuSarkis
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import gym

from src.agents import Agent

class Run():
    
    def __init__(self, 
                 env: gym.Env,
                 agent: Agent,
                 n_episodes: int,
                 test_mode: bool,
                 
                 ) -> None:
        
        self.env = env
        self.agent = agent
        self.n_episodes = n_episodes
        self.test_mode = test_mode
        
        self.step = 0
        self.best_reward = float('-Inf')
        self.reward_history = []
        
    def run(self) -> None:
        pass