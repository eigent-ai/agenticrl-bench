import gym

gym.envs.register(
    id='CardGame-v0',
    entry_point='gym_cardgame.envs:CardGameEnvironment',
    max_episode_steps=52,
)
