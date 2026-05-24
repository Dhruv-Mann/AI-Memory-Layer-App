import math
from datetime import datetime, timedelta
from typing import Tuple

# FSRS-5 default weights
DEFAULT_W = [
    0.402, 0.887, 2.183, 10.902, # S0 for Again, Hard, Good, Easy
    4.93, 0.942, 0.865, 0.095, 1.477, # D0 & lapse
    0.059, 2.132, 0.053, 0.347, # D modifications
    0.114, 0.282, 1.953, 0.091  # S modifications
]

class FSRS:
    def __init__(self, weights: list = DEFAULT_W):
        self.w = weights
        
    def init_card(self, grade: int) -> Tuple[float, float, int]:
        """
        Initializes stability, difficulty, and interval for a new card.
        Grade: 1=Again, 2=Hard, 3=Good, 4=Easy.
        Returns: (stability, difficulty, interval_days)
        """
        # S0 = w[grade - 1]
        s = self.w[grade - 1]
        # D0 = w[4] - (grade - 3) * w[5]
        d = self.w[4] - (grade - 3) * self.w[5]
        d = max(1.0, min(10.0, d))
        
        # Calculate initial interval
        if grade == 1:
            interval = 0  # Relearning same day
        elif grade == 2:
            interval = 1
        elif grade == 3:
            interval = 3
        else: # Easy
            interval = 7
            
        return s, d, interval

    def next_interval(self, stability: float) -> int:
        """
        Calculates interval in days for a given stability.
        For a target recall rate of 90%:
        Interval = 9 * Stability
        """
        return max(1, round(9.0 * stability))

    def step(self, stability: float, difficulty: float, reps: int, lapses: int, grade: int, elapsed_days: int) -> Tuple[float, float, int]:
        """
        FSRS-5 state transition step. Updates card attributes and schedules next review.
        Returns: (new_stability, new_difficulty, interval_days)
        """
        # If the card is completely brand new (never reviewed, reps == 0)
        if reps == 0:
            return self.init_card(grade)
            
        # Calculate current Retrievability
        # R = (1 + elapsed_days / (9 * stability)) ** -0.5
        r = (1.0 + elapsed_days / (9.0 * stability)) ** -0.5
        
        # Update difficulty
        # D' = D - w[9] * (G - 3)
        if grade == 1:
            # Lapse (Again)
            new_d = difficulty + self.w[6]
        else:
            new_d = difficulty - self.w[9] * (grade - 3)
        new_d = max(1.0, min(10.0, new_d))
        
        # Update stability
        if grade == 1:
            # Lapse
            # S' = w[7] * D^(-w[8]) * S^(w[9]) * (1 - R)
            new_s = self.w[6] * (new_d ** -self.w[7]) * (stability ** self.w[8]) * (1.0 - r)
            new_s = max(0.1, new_s)
            interval = 0 # review today/again
        else:
            # Success
            # S' = S * (1 + exp(w[11]) * (11 - D') * S^(-w[12]) * (exp(w[13]*(1-R)) - 1))
            factor = math.exp(self.w[10]) * (11.0 - new_d) * (stability ** -self.w[11]) * (math.exp(self.w[12] * (1.0 - r)) - 1.0)
            new_s = stability * (1.0 + factor)
            new_s = max(0.1, new_s)
            interval = self.next_interval(new_s)
            
        return new_s, new_d, interval
