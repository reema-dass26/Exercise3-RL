from typing import Dict, List, Tuple, Optional, Type
import random
import numpy as np
import pygame
import matplotlib


class Agent:
    def __init__(self) -> None:
        self.state_action_pairs_rewards: Dict[
            Tuple[int, int, Tuple[int, int], Tuple[int, int]],  # State
            Dict[
                int,  # Action
                List[int],  # Rewards
            ],
        ] = {}
        self.points_per_brick: int = 40
        self.points_per_tick: int = -0.1
        self.points_per_bump: int = 50
        self.total_reward: int = -self.points_per_tick
        self.lost_count: int = -1
        self.same_position_points: int = 200
        self.offset_change_points: int = 50

        self._tmp_bricks: Optional[int] = None
        self._last_x_offset: int = None

        self.last_speed: tuple[int, int] | None = None
        self.bounces: list[tuple[int, int]] = []
        self.paddle_bounces: list[int] = []

    # def policy(self, state) -> int:  # Returns action
    #     if state in self.state_action_pairs_rewards:
    #         actions = self.state_action_pairs_rewards[state]
    #         print(actions)
    #         epsilon = 0.01
    #         if actions:
    #             if 1000 * epsilon <= np.random.randint(1, 1000):
    #                 best_action = max(actions, key=lambda x: np.mean(actions[x]))
    #                 return best_action
    # #     return random.choice([-1, 0, 1])
    
    def policy(self, state):
        if state in self.state_action_pairs_rewards:
            actions = self.state_action_pairs_rewards[state]
            epsilon = 0.5
            if actions:
                if random.random() > epsilon:
                    best_action = max(actions, key=lambda x: np.mean(actions[x]))
                    return best_action
        return random.choice([-1, 0, 1])



    # def policy(self, state) -> int:
    #     if state in self.state_action_pairs_rewards:
    #         actions = self.state_action_pairs_rewards[state]
    #         if actions:
    #             best_action = max(actions, key=lambda x: np.mean(actions[x]))
    #             return best_action
    #     return random.choice([-1, 0, 1])

    def remember_reward(self, state, action, reward):
        self.total_reward += reward

        if state not in self.state_action_pairs_rewards:
            self.state_action_pairs_rewards[state] = {}
        if action not in self.state_action_pairs_rewards[state]:
            self.state_action_pairs_rewards[state][action] = []
        self.state_action_pairs_rewards[state][action].append(reward)

    def get_score(self, bricks, paddle_bumps: int,lost_count:int, x_offset: int, paddle_width: int):
        if self._tmp_bricks is None or self._last_x_offset is None:
            self._tmp_bricks = len(bricks)
            self._last_x_offset = x_offset
            return self.points_per_tick

        offset_reward: int = 0
        
        same_x_position = abs(x_offset) < (paddle_width // 2) + 1
        x_offset_change = abs(self._last_x_offset) - abs(x_offset)
        

        print(x_offset_change)

        if same_x_position:
            offset_reward += self.same_position_points
        else:
            offset_reward += self.offset_change_points * x_offset_change

        bricks_destroyed = self._tmp_bricks - len(bricks)
        self._last_x_offset = x_offset
        self._tmp_bricks = len(bricks)
        return (
            # bricks_destroyed * self.points_per_brick
            # + self.points_per_tick
            # + paddle_bumps * self.points_per_bump
            # + lost_count * self.lost_count
            # + 
            offset_reward
        )

    def reset_graph(self):
        self.bounces = []
        self.last_speed = None
        self.paddle_bounces = []

    def remember_bounce(self, pos: tuple[int, int], paddle_bounce: bool):
        self.bounces.append(pos)
        if paddle_bounce:
            self.paddle_bounces.append(len(self.bounces) - 1)

    def speed_change(self, speed: tuple[int, int]):
        if speed != self.last_speed:
            self.last_speed = speed
            return True
        return False

    def render_bounces(self, canvas: pygame.SurfaceType, scale_factor: int):
        cmap = matplotlib.cm.get_cmap("viridis")
        n_paddle_bounces: int = len(self.paddle_bounces)
        color_index: float = 0.0
        color: tuple[int, int, int, int] = tuple(
            (int(c * 255) for c in cmap(color_index))
        )  # type: ignore

        print(f"Bounces: {len(self.bounces)}")
        print(f"Paddle bounces: {len(self.paddle_bounces)}")

        canvas.fill((255, 255, 255))

        for x in range(canvas.get_width()):
            for y in range(canvas.get_height()):
                if not x % scale_factor and not y % scale_factor:
                    canvas.set_at((x, y), (0,0,0))


        for index, bounce in enumerate(self.bounces):
            if not index:
                continue

            # if index in self.paddle_bounces:
            #     color_index += 1 / n_paddle_bounces
            #     print(color_index)
            #     color = tuple((int(c * 255) for c in cmap(color_index)))  # type: ignore

            color_index += 1 / len(self.bounces)
            color = tuple((int(c * 255) for c in cmap(color_index)))  # type: ignore

            print(color_index)

            prev_bounce: tuple[int, int] = self.bounces[index - 1]
            start_pos: tuple[int, int] = (
                prev_bounce[0] * scale_factor + scale_factor // 2,  # X center
                prev_bounce[1] * scale_factor + scale_factor // 2,  # Y center
            )
            end_pos: tuple[int, int] = (
                bounce[0] * scale_factor + scale_factor // 2,  # X center
                bounce[1] * scale_factor + scale_factor // 2,  # Y center
            )
            pygame.draw.aaline(
                canvas,
                color,
                start_pos,
                end_pos,
            )
        pygame.image.save(canvas, "trace.png")


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
