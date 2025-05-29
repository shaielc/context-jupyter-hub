import json


def dict_to_profile(profile_config):
    """
    Converts a dictionary into the correct ProfilesSpawner format.

    Args:
        profile_config (dict): A dictionary containing:
            - "name" (str): The display name for the profile.
            - "shortname" (str): The unique key for the profile.
            - "dir" (str): The working directory for the profile.
            - "env_path" (str, optional): Path to the virtual environment. Defaults to "<workdir>/.venv".
            - "args" (list, optional): Additional command-line arguments. Defaults to an empty list.

    Returns:
        tuple: A tuple formatted for ProfilesSpawner.
    """
    workdir = profile_config["dir"]
    env_path = profile_config.get("env_path", f"{workdir}/.venv")
    args = " ".join(profile_config.get("args", []))

    cmd = (
        f"source {env_path}/bin/activate && cd {workdir} && exec jupyterhub-singleuser {args}"
    )

    return (
        profile_config["name"],  # Display name
        profile_config["shortname"],  # Unique key
        profile_config.get('cls',"jupyterhub.spawner.LocalProcessSpawner"),  # Spawner class
        {'cmd': ['/bin/bash', '-c', cmd]}  # Spawner config dictionary
    )

# Read profiles from profiles.json
with open('profiles.json', 'r') as file:
    profiles_data = json.load(file)

jupyterhub_profiles = [dict_to_profile(profile) for profile in profiles_data]

if __name__ == "__main__":
  # Example usage:
  profile_config = {
      "name": "Project 1 Environment",
      "shortname": "project1",
      "dir": "/path/to/project1",
      "env_path": "/path/to/project1/venv",
      "args": ["--ServerApp.default_url=/lab"]
  }
  
  profile = dict_to_profile(profile_config)
  print(profile)

