#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
import os

client = discord.Client()
Server = discord.Server

def folder_init():
    folders = ["litcoin", "level", "notifications"]
    for i in folders:
        try:
            os.stat(i)
        except:
            os.mkdir(i)
    return print("Stat-directories initialized")


def is_admin(member):
    if member.server_permissions == discord.Permissions.all():
        return True
    else:
        return False


def levelup(exp, level):
    level_up = False
    if exp > int(level**1.15 * 100):
        level_up = True
    return level_up
