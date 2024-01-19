#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import subprocess
import sys
from typing import List

import yaml
import git

"""convert_reqs_to_env.py: Convert Python project requirements.txt file to 
                            Conda's environment.yml file."""

__author__  = "Vratislav Besta"
__group__   = "50"
__version__ = "1.0.1"
__email__   = "bestavra@fel.cvut.cz"
__date__    = "2024/01/18" 


def read_requirements(req_file: str) -> List[str]:
    """
    Read and parse the requirements from requirements.txt
    """
    with open(req_file, 'r') as file:
        requirements = file.readlines()

    parsed_requirements = []
    for req in requirements:
        req = req.strip()
        if req and not req.startswith('#'):
            parsed_requirements.append(req)

    return parsed_requirements


def create_env_yaml(requirements: List[str], env_template: dict, git_root: str) -> None:
    """
    Create the environment.yml file based on the requirements and a template
    """
    env_data = env_template
    env_data['dependencies'] = ['python=3.10', 'pip', 'dvc', {'pip': requirements}]

    with open(os.path.join(git_root, 'environment.yml'), 'w') as file:
        yaml.dump(env_data, file, default_flow_style=False)


def find_git_root_folder() -> None | str:
    """
    Finds the root folder of the git repository to automatically set the paths to the data folders.
    """
    try:
        repo = git.Repo(search_parent_directories=True)
        git_root = repo.git.rev_parse("--show-toplevel")
        return git_root
    except git.InvalidGitRepositoryError:
        return None


def is_main_branch():
    # Get the current branch name
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
    return branch == 'main'
    

def main():
    # Check if the script is running on the main branch
    if is_main_branch():
        print("This script does not run on the main branch.")
        sys.exit(0)

    # Template for environment.yml
    env_template = {
        'channels': ['conda-forge', 'defaults'],
        'name': 'DTU_ML_Ops',
        'dependencies': []
    }

    git_root = find_git_root_folder()

    requirements = read_requirements(os.path.join(git_root, 'requirements.txt'))
    create_env_yaml(requirements, env_template, git_root)


if __name__ == '__main__':
    main()