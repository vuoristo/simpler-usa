import cv2
from gym.spaces.box import Box
import numpy as np
import gym
from gym import spaces
import logging
import time
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_env(env_id, client_id, remotes, **kwargs):
    spec = gym.spec(env_id)
    return create_atari_env(env_id)

def create_atari_env(env_id):
    env = gym.make(env_id)
    env = AtariRescale42x42(env)
    return env

def _process_frame42(frame):
    frame = frame[34:34+160, :160]
    # Resize by half, then down to 42x42 (essentially mipmapping). If we resize
    # directly we lose pixels that, when mapped to 42x42, aren't close enough
    # to the pixel boundary.
    frame = cv2.resize(frame, (80, 80))
    frame = cv2.resize(frame, (42, 42))
    frame = frame.mean(2)
    frame = frame.astype(np.float32)
    frame *= (1.0 / 255.0)
    frame = np.reshape(frame, [42, 42, 1])
    return frame

class AtariRescale42x42(gym.ObservationWrapper):
    def __init__(self, env=None):
        super(AtariRescale42x42, self).__init__(env)
        self.observation_space = Box(0.0, 1.0, [42, 42, 1])

    def _observation(self, observation):
        return _process_frame42(observation)
