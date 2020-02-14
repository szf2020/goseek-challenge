from typing import Any, Dict

import numpy as np

from tesse_gym.eval.agent import Agent


class StableBaselinesPPO(Agent):
    """ Stable Baselines PPO agent for GOSEEK submission. """

    def __init__(self, config: Dict[str, Any]) -> None:
        """ Initialize agent.

        Args:
            config (Dict[str, Any]): Agent configuration.
        """
        from stable_baselines import PPO2
        self.model = PPO2.load(config["weights"])
        self.state = None

        # Number of environments used to train model
        # to which stable-baselines input tensor size is fixed
        self.n_train_envs = self.model.initial_state.shape[0]

    def act(self, observation: np.ndarray) -> int:
        """ Act on an observation.

        args:
            observation (np.ndarray): observation.

        returns:
            int: an action in [0, 4) defined as follows
                - 0: forward 0.5m
                - 1: right 8 degrees
                - 2: left 8 degrees
                - 3: declare target
        """
        observation = np.repeat(observation[np.newaxis], self.n_train_envs, 0)
        actions, state = self.model.predict(
            observation, state=self.state, deterministic=False
        )
        self.state = state  # update model state
        return actions[0]

    def reset(self) -> None:
        """ Reset model state. """
        self.state = None


class RandomAgent(Agent):
    """ Agent that takes random actions. """

    def __init__(self, config: Dict[str, Any]) -> None:
        """ Initialize agent.

        Args:
            config (Dict[str, Any]): Agent configuration
        """

        self.action_space = np.arange(0, 4)

        # give probability for actions in `self.action_space`
        self.action_probability = np.array(config["action_probability"])
        self.action_probability /= self.action_probability.sum()

    def act(self, observation: np.ndarray) -> int:
        """ Take a uniformly random action.

        args:
            observation (np.ndarray): observation.

        returns:
            int: an action in [0, 4) defined as follows
                - 0: forward 0.5m
                - 1: right 8 degrees
                - 2: left 8 degrees
                - 3: declare target
        """
        return np.random.choice(self.action_space, p=self.action_probability)

    def reset(self) -> None:
        """ Nothing required on episode reset. """
        pass
