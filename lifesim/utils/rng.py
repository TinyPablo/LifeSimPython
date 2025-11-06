import random
import threading

import numpy as np


class RNG:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, seed: int | None = None):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init(seed)
        return cls._instance

    def _init(self, seed: int | None):
        self.seed = 0 if seed is None else seed
        self.random = random.Random(self.seed)
        self.np = np.random.default_rng(self.seed)
        
rng = RNG(0)