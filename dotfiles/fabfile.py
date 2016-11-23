# -*- coding: utf-8 -*-

from fabric.api import task, put, run


@task
def init():
    put(".bash_aliases", "~/.bash_aliases")
    put(".gitconfig", "~/.gitconfig")
    put(".vimrc", "~/.vimrc")
    put(".bashrc", "~/bashrc.append")
    run("cat ~/.bashrc ~/bashrc.append > ~/bashrc.new")
    run("mv ~/.bashrc ~/bashrc.backup")
    run("mv ~/bashrc.new ~/.bashrc")
    run("rm -f ~/bashrc.append ~/bashrc.new")
