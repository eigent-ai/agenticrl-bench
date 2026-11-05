import gymnasium
import gym_cardgame

print("Creating environment...")
env = gymnasium.make('CardGame-v0')

print("Resetting...")
obs, info = env.reset()
print(f"Initial observation: {obs}")

print("Stepping...")
for i in range(8):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    print(f"Step {i+1}: obs={obs}, reward={reward}, terminated={terminated}")

print("Done!")
