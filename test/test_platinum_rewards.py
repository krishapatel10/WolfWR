import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transactions.platinum_rewards import issue_platinum_reward

if __name__ == "__main__":
    issue_platinum_reward(2024)
