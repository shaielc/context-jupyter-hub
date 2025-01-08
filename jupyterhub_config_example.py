# Add this to your jupyterhub_config.py file, make sure it's in the directory of this project.
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from wrapspawner import ProfilesSpawner
from jupyterhub_profiles import jupyterhub_profiles

c.JupyterHub.spawner_class = ProfilesSpawner
c.ProfilesSpawner.profiles = jupyterhub_profiles
c.Authenticator.allowed_users = {'user'}

