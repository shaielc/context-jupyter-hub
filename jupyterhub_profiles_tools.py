#!/usr/bin/env python3

import json
import os
import subprocess
import argparse

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
        'jupyterhub.spawner.LocalProcessSpawner',  # Spawner class
        {'cmd': ['/bin/bash', '-c', cmd]}  # Spawner config dictionary
    )

def load_profiles(file_path='profiles.json'):
    """Loads profiles from the specified JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_profiles(profiles, file_path='profiles.json'):
    """Saves profiles to the specified JSON file."""
    with open(file_path, 'w') as file:
        json.dump(profiles, file, indent=4)

def add_profile(profile_config):
    profiles = load_profiles()
    profiles.append(profile_config)
    save_profiles(profiles)
    print(f"Profile '{profile_config['name']}' added successfully.")

def change_profile(shortname, updated_config):
    profiles = load_profiles()
    for i, profile in enumerate(profiles):
        if profile['shortname'] == shortname:
            profiles[i] = {**profile, **updated_config}
            save_profiles(profiles)
            print(f"Profile '{shortname}' updated successfully.")
            return
    print(f"Profile with shortname '{shortname}' not found.")

def remove_profile(shortname):
    profiles = load_profiles()
    profiles = [profile for profile in profiles if profile['shortname'] != shortname]
    save_profiles(profiles)
    print(f"Profile '{shortname}' removed successfully.")

def display_profiles():
    profiles = load_profiles()
    for profile in profiles:
        print(json.dumps(profile, indent=4))

def ensure_jupyterhub_installed(env_path):
    activate_script = os.path.join(env_path, 'bin', 'activate')
    subprocess.run(
        f"source {activate_script} && pip install jupyterhub", 
        shell=True, 
        check=True
    )
    print(f"JupyterHub installed in virtual environment: {env_path}")

def setup_jupyterhub_service(exec_start=None):
    """
    Sets up a systemd service for JupyterHub to run on startup.

    Args:
        exec_start (str, optional): Custom ExecStart path. If not provided, defaults to <current_dir>/.venv/bin/jupyterhub.
    """
    working_dir = os.getcwd()
    env_path = os.path.join(working_dir, '.venv')
    if exec_start is None:
        exec_start = f"{env_path}/bin/jupyterhub"

    service_content = f"""
    [Unit]
    Description=JupyterHub
    After=network.target

    [Service]
    Type=simple
    User={os.getenv('USER')}
    WorkingDirectory={working_dir}
    ExecStart=/bin/bash -c 'source {env_path}/bin/activate && {exec_start}'
    Restart=always

    [Install]
    WantedBy=multi-user.target
    """

    service_path = "/etc/systemd/system/jupyterhub.service"
    with open(service_path, 'w') as service_file:
        service_file.write(service_content)
    subprocess.run(['systemctl', 'daemon-reload'], check=True)
    subprocess.run(['systemctl', 'enable', 'jupyterhub'], check=True)
    subprocess.run(['systemctl', 'start', 'jupyterhub'], check=True)
    print("JupyterHub service installed and started successfully.")

def export_profiles_to_config(json_path='profiles.json', config_path='jupyterhub_config.py'):
    """
    Exports profiles from a JSON file to a JupyterHub configuration file.

    Args:
        json_path (str): Path to the JSON file containing profiles.
        config_path (str): Path to the JupyterHub configuration file to write.
    """
    profiles = load_profiles(json_path)
    formatted_profiles = [dict_to_profile(profile) for profile in profiles]
    return formatted_profiles

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage JupyterHub profiles and service setup.")

    subparsers = parser.add_subparsers(dest="command")

    # Add profile command
    add_parser = subparsers.add_parser("add", help="Add a new profile.")
    add_parser.add_argument("name", help="Name of the profile.")
    add_parser.add_argument("shortname", help="Shortname of the profile.")
    add_parser.add_argument("dir", help="Working directory of the profile.")
    add_parser.add_argument("--env_path", help="Path to the virtual environment.", default=None)
    add_parser.add_argument("--args", nargs="*", help="Additional arguments for the server.", default=[])

    # Change profile command
    change_parser = subparsers.add_parser("change", help="Change an existing profile.")
    change_parser.add_argument("shortname", help="Shortname of the profile to change.")
    change_parser.add_argument("--name", help="New name of the profile.")
    change_parser.add_argument("--dir", help="New working directory of the profile.")
    change_parser.add_argument("--env_path", help="New path to the virtual environment.")
    change_parser.add_argument("--args", nargs="*", help="New additional arguments for the server.", default=None)

    # Remove profile command
    remove_parser = subparsers.add_parser("remove", help="Remove a profile.")
    remove_parser.add_argument("shortname", help="Shortname of the profile to remove.")

    # Display profiles command
    display_parser = subparsers.add_parser("display", help="Display all profiles.")

    # Setup service command
    service_parser = subparsers.add_parser("setup-service", help="Setup JupyterHub systemd service.")
    service_parser.add_argument("--exec_start", help="Custom ExecStart path.", default=None)

    # Export profiles command
    export_parser = subparsers.add_parser("export", help="Export profiles to JupyterHub configuration.")
    export_parser.add_argument("--json_path", help="Path to the JSON file with profiles.", default="profiles.json")
    export_parser.add_argument("--config_path", help="Path to the JupyterHub configuration file.", default="jupyterhub_config.py")

    args = parser.parse_args()

    if args.command == "add":
        profile_config = {
            "name": args.name,
            "shortname": args.shortname,
            "dir": args.dir,
            "env_path": args.env_path if args.env_path else f"{args.dir}/.venv",
            "args": args.args
        }
        add_profile(profile_config)

    elif args.command == "change":
        updated_config = {}
        if args.name:
            updated_config["name"] = args.name
        if args.dir:
            updated_config["dir"] = args.dir
        if args.env_path:
            updated_config["env_path"] = args.env_path
        if args.args is not None:
            updated_config["args"] = args.args
        change_profile(args.shortname, updated_config)

    elif args.command == "remove":
        remove_profile(args.shortname)

    elif args.command == "display":
        display_profiles()

    elif args.command == "setup-service":
        setup_jupyterhub_service(exec_start=args.exec_start)

    elif args.command == "export":
        export_profiles_to_config(json_path=args.json_path, config_path=args.config_path)

    else:
        parser.print_help()

