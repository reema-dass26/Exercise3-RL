from typing import Dict, List, Tuple, Optional
import random
import numpy as np
from collections import deque


class Agent:
    def __init__(self) -> None:
        self.state_action_pairs_rewards: Dict[
            Tuple[int, int, Tuple[int, int], Tuple[int, int]],  # State
            Dict[
                int,  # Action
                List[int],  # Rewards
            ],
        ] = {}

        self.points_per_brick: int = 0
        self.points_per_tick: int = -1
        self.points_per_bump: int = 5000
        self.total_reward: int = 0

        self._tmp_bricks: Optional[int] = None

        self.last_speed: tuple[int, int] | None = None
        self.bounces: list[tuple[int, int]] = []
        self.last_entries= deque(maxlen=10)

    def policy(self, state) -> int:  # Returns action
        if state in self.state_action_pairs_rewards:
            actions = self.state_action_pairs_rewards[state]
            print(actions)
            epsilon = 0.1
            if actions:
                if 1000 * epsilon <= np.random.randint(1, 1000):
                    # if(actions not in  self.state_action_pairs_rewards[state]):
                    #     return random.choice([-1, 0, 1])
                    best_action = max(actions, key=lambda x: np.mean(actions[x]))
                    print("Greedy choice!")
                    return best_action
        print("Random choice!")
        return random.choice([-1, 0, 1])

    def remember_reward(self, state, action, reward):
        self.total_reward += reward

        if state not in self.state_action_pairs_rewards:
            self.state_action_pairs_rewards[state] = {}
        if action not in self.state_action_pairs_rewards[state]:
            self.state_action_pairs_rewards[state][action] = []
        self.state_action_pairs_rewards[state][action].append(reward)

    def update(self,state,action):
        self.last_entries.append((state,action))
    


    def get_score(self, paddle_bumps: int):
        return (
            + self.points_per_tick
            #+ paddle_bumps * self.points_per_bump
        )

    def remember_bounce(self, pos: tuple[int, int]):
        self.bounces.append(pos)

    def speed_change(self, speed: tuple[int, int]):
        if speed != self.last_speed:
            self.last_speed = speed
            return True
        return False


# State:
# (
#     xy_paddle [x]
#     speed_paddle [vx]
#     xy_ball [x, y]
#     speed_ball [vx, vy]
# )

# Actions:
# (
#     press_left
#     press_right
#     none
# )
