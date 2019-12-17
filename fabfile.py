# -*- coding: utf-8 -*-

"""
Setup:
    pip install -U "fabric>=2.5.0" invocations
    Put file `.fabric.py` with `user = "name"` into your home directory.
"""
from pathlib import Path

from fabric import task as remote_task
from invocations.console import confirm
from invoke import task as local_task

DEFAULT_PASSWORD_LENGTH = 25
DOCKER_AVAILABLE_COMMANDS = {"ps", "term", "stop", "start", "restart", "rm", "logs"}
DOCKER_COMMANDS = {
    "ps": 'ps -a --no-trunc --format="table {{.Names}}\\t{{.Status}}\\t{{.Command}}"',
    "term": "kill --signal TERM",
    "rm": "rm -v",
}


@remote_task
def server_init(c):
    c.put("dotfiles/.bash_aliases", "~/.bash_aliases")
    c.put("dotfiles/.gitconfig", "~/.gitconfig")
    c.put("dotfiles/.vimrc", "~/.vimrc")
    c.put("dotfiles/.bashrc", "~/bashrc.append")
    c.run("cat ~/.bashrc ~/bashrc.append > ~/bashrc.new")
    c.run("mv ~/.bashrc ~/bashrc.backup")
    c.run("mv ~/bashrc.new ~/.bashrc")
    c.run("rm -f ~/bashrc.append ~/bashrc.new")


@local_task
def password(c, nginx=False, length=DEFAULT_PASSWORD_LENGTH, special_chars=True):
    """[--nginx --length=25 --no-special-chars]"""
    print(generate_password(length, special_chars))
    if nginx:
        c.run("openssl passwd -apr1")


@remote_task
def add_group(c, group="docker"):
    """[--group=docker]"""
    c.run(f"usermod -a -G {group} {c.user}")


@remote_task(password)
def create_user(c, name):
    """<name>"""
    c.sudo(f"useradd --groups docker --create-home --shell /bin/bash {name}")
    c.sudo(f"passwd {name}")


@local_task
def etc_hosts(_, add=None, remove=None):
    """[--add="127.0.0.1 postgres" | --remove=<ip/host>] """
    path = Path("c:/Windows/System32/drivers/etc/hosts")
    content = path.read_text(encoding="utf-8")

    new_lines = []
    if add:
        new_lines = content.splitlines() + [add]
    elif remove:
        new_lines = [l for l in content.splitlines() if not l.startswith(remove) and not l.endswith(remove)]

    if new_lines:
        new_content = "\n".join(new_lines)
        print(new_content)

        if confirm("OK?", assume_yes=False):
            path.write_text(new_content, encoding="utf-8")
    else:
        print(content)


@local_task
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

    return ''.join(generator.choice(chars) for i in range(length))


@local_task
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


@local_task
def pg_load(c, database, only_data=True):
    """--database=<name> [--only-data]"""
    if not only_data:
        c.run(f'psql -U postgres -d "{database}" -f schema.sql')

    c.run(f'psql -U postgres -d "{database}" -f data.sql')


@remote_task(iterable=["container"])
def docker(c, statement, container):
    """-H example.com,domain.org ps | (logs | term | stop | start | restart | rm --container=<name>...)"""
    if statement not in DOCKER_AVAILABLE_COMMANDS:
        print(f"Please specify valid docker statement: {DOCKER_AVAILABLE_COMMANDS}")
        return

    if statement == "ps":
        c.run("docker " + DOCKER_COMMANDS.get(statement, statement))
    else:
        for name in container:
            c.run(f"docker {DOCKER_COMMANDS.get(statement, statement)} {name}", warn=True)
