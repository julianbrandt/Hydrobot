#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tinydb import TinyDB, Query

query = Query()


def notification_get(server, channel=None):
    notificationlist = TinyDB("notifications/NOTIFICATIONS" + server.id + ".json")
    if not notificationlist.contains(query["channel"] == channel.id):
        notificationlist.insert({"channel": channel.id, "commands": []})
    return notificationlist.search(query["channel"] == channel.id)[0]["commands"]


def notification_block(server, channel, command):
    notificationlist = TinyDB("notifications/NOTIFICATIONS" + server.id + ".json")
    notifications = notificationlist.search(query["channel"] == channel.id)[0]["commands"]
    notifications.append(command)
    notificationlist.update({"commands": notifications}, query["channel"] == channel.id)


def notification_allow(server, channel, command):
    notificationlist = TinyDB("notifications/NOTIFICATIONS" + server.id + ".json")
    notifications = notificationlist.search(query["channel"] == channel.id)[0]["commands"]
    notifications.remove(command)
    notificationlist.update({"commands": notifications}, query["channel"] == channel.id)


def notifications_closed(command, server, channel):
    if command in notification_get(server, channel):
        return True
    else:
        return False
