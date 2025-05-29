# JupyterHub Profile Manager

This tool provides functionality to manage JupyterHub profiles and automate setup, including creating profiles, modifying them, exporting configurations, and setting up a JupyterHub systemd service.

## Features

- **Add Profile**: Add a new profile with specific configurations.
- **Change Profile**: Modify an existing profile.
- **Remove Profile**: Delete a profile.
- **Display Profiles**: List all profiles in the configuration.
- **Export Profiles**: Generate a `jupyterhub_config.py` file from the profiles.
- **Setup JupyterHub Service**: Install and configure JupyterHub to run as a systemd service.

## Requirements

Install the required packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```
### `requirements.txt`
- `jupyterhub`
- `jupyterlab`
- `wrapspawner`

### IMPORTANT NOTE
the target environemnt must also install jupyterhub and jupyterlab!

## Usage

### CLI Commands

The script provides a CLI for managing profiles and setting up the service:

#### Add a Profile
```bash
python3 jupyterhub_profile_formatter.py add <name> <shortname> <dir> [--env_path <path>] [--args <arg1> <arg2> ...]
```
Example:
```bash
python3 jupyterhub_profile_formatter.py add "Project 1" project1 /path/to/project1 --args --ServerApp.default_url=/lab
```

#### Change a Profile
```bash
python3 jupyterhub_profile_formatter.py change <shortname> [--name <new_name>] [--dir <new_dir>] [--env_path <new_env_path>] [--args <new_arg1> <new_arg2> ...]
```
Example:
```bash
python3 jupyterhub_profile_formatter.py change project1 --name "Updated Project 1"
```

#### Remove a Profile
```bash
python3 jupyterhub_profile_formatter.py remove <shortname>
```
Example:
```bash
python3 jupyterhub_profile_formatter.py remove project1
```

#### Display Profiles
```bash
python3 jupyterhub_profile_formatter.py display
```

#### Export Profiles to Configuration
```bash
python3 jupyterhub_profile_formatter.py export [--json_path <path>] [--config_path <path>]
```
Example:
```bash
python3 jupyterhub_profile_formatter.py export --json_path profiles.json --config_path jupyterhub_config.py
```

#### Setup JupyterHub Service
```bash
python3 jupyterhub_profile_formatter.py setup-service [--exec_start <path>]
```
Example:
```bash
python3 jupyterhub_profile_formatter.py setup-service
```

### Profiles JSON Structure
The `profiles.json` file should contain a list of profiles in the following format:

```json
[
  {
    "name": "Project 1",
    "shortname": "project1",
    "dir": "/path/to/project1",
    "env_path": "/path/to/project1/.venv",
    "args": ["--ServerApp.default_url=/lab"]
  },
  {
    "name": "Project 2",
    "shortname": "project2",
    "dir": "/path/to/project2",
    "args": []
  }
]
```

### Setting Up the Systemd Service
The systemd service is configured to:
- Use the `.venv` virtual environment in the current working directory by default.
- Run JupyterHub on startup.

Run:
```bash
python3 jupyterhub_profile_formatter.py setup-service
```
This creates a service file at `/etc/systemd/system/jupyterhub.service` and enables the service.

## License
This tool is licensed under the MIT License.


