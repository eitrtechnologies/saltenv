import os

# https://pop.readthedocs.io/en/latest/tutorial/quickstart.html#adding-configuration-data

# In this dictionary goes all the immutable values you want to show up under hub.OPT.saltenv
CONFIG = {
    "config": {
        "default": None,
        "help": "Load extra options from a configuration file onto hub.OPT.saltenv",
    },
    "repo_url": {
        "default": "https://repo.saltproject.io/salt/singlebin",
        "help": "Salt single binary repository location. Version directories are expected here.",
    },
    "saltenv_dir": {
        "default": os.path.join(os.environ["HOME"], ".saltenv"),
        "help": "Working directory for saltenv downloads",
    },
}

# The selected subcommand for your cli tool will show up under hub.SUBPARSER
# The value for a subcommand is a dictionary that will be passed as kwargs to argparse.ArgumentParser.add_subparsers
SUBCOMMANDS = {
    "init": {},
    "install": {},
    "list": {},
    "list-remote": {},
    "pin": {},
    "uninstall": {},
    "use": {},
    "version": {},
}

# Include keys from the CONFIG dictionary that you want to expose on the cli
# The values for these keys are a dictionaries that will be passed as kwargs to argparse.ArgumentParser.add_option
CLI_CONFIG = {
    "config": {"options": ["-c"]},
    # "my_option1": {"subcommands": ["A list of subcommands that exclusively extend this option"]},
    # This option will be available under all subcommands and the root command
    "repo_url": {"options": ["-r", "--repo-url"], "subcommands": ["_global_"]},
    "saltenv_dir": {"options": ["-d", "--saltenv-dir"], "subcommands": ["_global_"]},
    "force": {"options": ["--force"], "subcommands": ["init"]},
    "salt_version": {
        "display_priority": 0,
        "positional": True,
        "subcommands": ["install", "use", "uninstall"],
        "help": "The version of Salt to act on.",
    },
}

# These are the namespaces that your project extends
# The hub will extend these keys with the modules listed in the values
DYNE = {"saltenv": ["saltenv"]}
