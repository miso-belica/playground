# -*- coding: utf-8 -*-

"""
Setup:
    pip install -U "fabric>=2.5.0" invocations
    Put file `.fabric.py` with `user = "name"` into your home directory.
"""
from pathlib import Path

from fabric import Connection
from invocations.console import confirm
from invoke import task

DEFAULT_PASSWORD_LENGTH = 25
DOCKER_AVAILABLE_COMMANDS = {"ps", "term", "stop", "start", "restart", "rm", "logs"}
DOCKER_COMMANDS = {
    "ps": 'ps -a --no-trunc --format="table {{.Names}}\\t{{.Status}}\\t{{.Command}}"',
    "term": "kill --signal TERM",
    "rm": "rm -v",
}


@task
def server_init(_, host, user=None):
    """<host> [--user=<name>]"""
    with Connection(host, user) as remote:
        remote.put("dotfiles/.bash_aliases", "~/.bash_aliases")
        remote.put("dotfiles/.gitconfig", "~/.gitconfig")
        remote.put("dotfiles/.vimrc", "~/.vimrc")
        remote.put("dotfiles/.bashrc", "~/bashrc.append")
        remote.run("cat ~/.bashrc ~/bashrc.append > ~/bashrc.new")
        remote.run("mv ~/.bashrc ~/bashrc.backup")
        remote.run("mv ~/bashrc.new ~/.bashrc")
        remote.run("rm -f ~/bashrc.append ~/bashrc.new")


@task
def password(c, nginx=False, length=DEFAULT_PASSWORD_LENGTH, special_chars=True):
    """[--nginx --length=25 --no-special-chars]"""
    print(generate_password(length, special_chars))
    if nginx:
        c.run("openssl passwd -apr1")


@task
def add_group(_, host, user, group="docker"):
    """<host> [--group=docker]"""
    with Connection(host, user) as remote:
        remote.run(f"usermod -a -G {group} {user}")


@task
def create_user(c, host, name, creator="root"):
    """<host> <name> [--creator=<root>]"""
    password(c)
    with Connection(host, creator) as remote:
        remote.sudo(f"useradd --groups docker --create-home --shell /bin/bash {name}")
        remote.sudo(f"passwd {name}")


@task
def etc_hosts(_, add=None, remove=None):
    """[--add="127.0.0.1 postgres" | --remove=<ip/host>] """
    path = Path("c:/Windows/System32/drivers/etc/hosts")
    content = path.read_text(encoding="utf-8")

    new_lines = []
    if add:
        new_lines = content.splitlines() + [add]
    elif remove:
        new_lines = [line for line in content.splitlines() if not line.startswith(remove) and not line.endswith(remove)]

    if new_lines:
        new_content = "\n".join(new_lines)
        print(new_content)

        if confirm("OK?", assume_yes=False):
            path.write_text(new_content, encoding="utf-8")
    else:
        print(content)


@task
def ssh_key(c, comment):
    """--comment=<e-mail>"""
    c.run(f'ssh-keygen -t rsa -b 4096 -C "{comment}"')


def generate_password(length, special_chars):
    import string
    from random import SystemRandom

    generator = SystemRandom()
    chars = string.ascii_letters + string.digits + "._+=-"
    if special_chars:
        chars += "|?!@#$%^&*(),;~"

    return ''.join(generator.choice(chars) for _ in range(length))


@task
def pg_dump(c, database, only_schema=False):
    """--database=<name> [--only-schema]"""
    c.run(
        'pg_dump --schema-only --quote-all-identifiers --no-security-labels --no-owner --no-privileges '
        f'-U postgres -d "{database}" -f schema.sql',
    )

    if not only_schema:
        c.run(
            'pg_dump --data-only --table=applied_migrations --quote-all-identifiers '
            f'-U postgres -d "{database}" -f data.sql',
        )


@task
def pg_load(c, database, only_data=True):
    """--database=<name> [--only-data]"""
    if not only_data:
        c.run(f'psql -U postgres -d "{database}" -f schema.sql')

    c.run(f'psql -U postgres -d "{database}" -f data.sql')


@task(iterable=["container"])
def docker(_, host, statement, container):
    """<host> ps | (logs | term | stop | start | restart | rm --container=<name>...)"""
    if statement not in DOCKER_AVAILABLE_COMMANDS:
        print(f"Please specify valid docker statement: {DOCKER_AVAILABLE_COMMANDS}")
        return

    with Connection(host) as remote:
        if statement == "ps":
            remote.run("docker " + DOCKER_COMMANDS.get(statement, statement))
        else:
            for name in container:
                remote.run(f"docker {DOCKER_COMMANDS.get(statement, statement)} {name}", warn=True)


@task
def git_changes(c, base_branch="master"):
    """[--patterns=<file>]"""
    result = c.run("git branch --all", hide="out")
    branches = [line.strip(" *") for line in result.stdout.splitlines() if "->" not in line]

    changed_files = set()
    for branch in branches:
        if branch != base_branch and not branch.startswith("remotes/"):
            result = c.run(f"git merge-base {branch} {base_branch}", hide="out", echo=False, warn=True)
            result = c.run(f"git diff --name-only {branch} {result.stdout}", hide="out", echo=False, warn=True)
            changed_files.update(result.stdout.splitlines())

    print("\n".join(sorted(changed_files)))


@task
def python_profile(c, command):
    """script.py

    https://thirld.com/blog/2014/11/30/visualizing-the-results-of-profiling-python-code/
    sudo apt install kcachegrind
    pip install pyprof2calltree
    pyprof2calltree -i profiling.out -k
    """
    c.run(f"python -m cProfile -s cumtime -o profiling.out {command}")
