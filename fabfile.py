# -*- coding: utf-8 -*-

"""
Setup:
    pip install -U "fabric>=2.5.0"
    Put file `.fabric.py` with `user = "name"` into your home directory.
"""

from fabric import task as remote_task
from invoke import task as local_task

DEFAULT_PASSWORD_LENGTH = 25
DOCKER_AVAILABLE_COMMANDS = {"ps", "term", "stop", "start", "restart", "rm", "logs"}
DOCKER_COMMANDS = {
    "ps": 'ps -a --no-trunc --format="table {{.Names}}\\t{{.Status}}\\t{{.Command}}"',
    "term": "kill --signal TERM",
    "rm": "rm -v",
}


@remote_task
def init(c):
    c.put("dotfiles/.bash_aliases", "~/.bash_aliases")
    c.put("dotfiles/.gitconfig", "~/.gitconfig")
    c.put("dotfiles/.vimrc", "~/.vimrc")
    c.put("dotfiles/.bashrc", "~/bashrc.append")
    c.run("cat ~/.bashrc ~/bashrc.append > ~/bashrc.new")
    c.run("mv ~/.bashrc ~/bashrc.backup")
    c.run("mv ~/bashrc.new ~/.bashrc")
    c.run("rm -f ~/bashrc.append ~/bashrc.new")


@local_task
def password(_, length=DEFAULT_PASSWORD_LENGTH, no_special_chars=False):
    print(generate_password(length, not no_special_chars))


def generate_password(length, special_chars):
    import string
    from random import SystemRandom

    generator = SystemRandom()
    chars = string.ascii_letters + string.digits + "._+=-"
    if special_chars:
        chars += "|?!@#$%^&*(),;~"

    return ''.join(generator.choice(chars) for i in range(length))


@local_task
def pg_dump(c, database, only_schema=False):
    c.run(
        'pg_dump --schema-only --quote-all-identifiers --no-security-labels --no-owner --no-privileges '
        f'-U postgres -d "{database}" -f schema.sql',
    )

    if not only_schema:
        c.run(
            'pg_dump --data-only --table=applied_migrations --quote-all-identifiers '
            f'-U postgres -d "{database}" -f data.sql',
        )


@local_task
def pg_load(c, database, only_data=True):
    if not only_data:
        c.run(f'psql -U postgres -d "{database}" -f schema.sql')

    c.run(f'psql -U postgres -d "{database}" -f data.sql')


@remote_task
def docker(c, command="ps"):
    if command not in DOCKER_AVAILABLE_COMMANDS:
        print(f"Please specify valid docker command: {DOCKER_AVAILABLE_COMMANDS}")
        return

    c.run("docker " + DOCKER_COMMANDS.get(command, command))
