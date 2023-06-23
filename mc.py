from typing import Dict, List, Tuple, Optional
import random
import numpy as np


class Agent:
    def __init__(self) -> None:
        self.state_action_pairs_rewards: Dict[
            Tuple(int, int, Tuple[int, int], Tuple[int, int]),  # State
            Dict[
                int,  # Action
                List[int],  # Rewards
            ],
        ] = {}
        self.points_per_brick: int = 0
        self.points_per_tick: int = -1
        self.points_per_bump: int = 50000
        self.total_reward: int = -self.points_per_tick

        self._tmp_bricks: Optional[int] = None

    def policy(self, state) -> int:  # Returns action
        if state in self.state_action_pairs_rewards:
            actions = self.state_action_pairs_rewards[state]
            print(actions)
            epsilon=0.01
            if actions:
                if (1000*epsilon<=np.random.randint(1,1000)):
                    return random.choice([-1, 0, 1])
                best_action = max(actions, key=lambda x: np.mean(actions[x]))
                return best_action
        return random.choice([-1, 0, 1])

    def remember_reward(self, state, action, reward):
        self.total_reward += reward

        if state not in self.state_action_pairs_rewards:
            self.state_action_pairs_rewards[state] = {}
        if action not in self.state_action_pairs_rewards[state]:
            self.state_action_pairs_rewards[state][action] = []
        self.state_action_pairs_rewards[state][action].append(reward)

    def get_score(self, bricks, paddle_bumps: int):
        if self._tmp_bricks is None:
            self._tmp_bricks = len(bricks)
            return self.points_per_tick

        bricks_destroyed = self._tmp_bricks - len(bricks)
        self._tmp_bricks = len(bricks)
        return (
            bricks_destroyed * self.points_per_brick
            + self.points_per_tick
            + paddle_bumps * self.points_per_bump
        )


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
