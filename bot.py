# -*- coding:utf-8 -*-
from random import shuffle
from os import urandom
from collections import namedtuple
from qqbot.utf8logger import ERROR, INFO
import time


class MsgContainer:
    def __init__(self, capacity):
        self.data = list()
        self.capacity = capacity

    def __getitem__(self, idx):
        return self.data[idx]

    def append(self, item):
        self.data.append(item)
        if len(self.data) > self.capacity:
            self.data.pop(0)

    def pop(self, idx=-1):
        return self.data.pop(idx)


MsgTuple = namedtuple('MsgTuple', ['sender', 'time', 'content'])


def randint(l, r):
    value = int.from_bytes(urandom(32), 'big') % (r - l) + l
    INFO('[randint] [%d ~ %d] 返回了 %d', l, r, value)
    return value


commands = dict()
history = MsgContainer(50)

meal_def = []
meal = []
try:
    with open('meal_def.txt', 'r') as f:
        for line in f:
            meal_def.append(line.strip())
except FileNotFoundError:
    INFO('路径出错啦，没有找到默认菜单！')

try:
    with open('meal.txt', 'r') as f:
        for line in f:
            meal.append(line.strip())
except FileNotFoundError:
    INFO('路径出错啦，没有找到群友菜单！')


def register_commands(command):
    def closure(func):
        commands[command] = func
        return func

    return closure


def onQQMessage(bot, contact, member, content):

    # availability filter
    if bot.isMe(contact, member):
        return

    # 记录
    history.append(
        MsgTuple(
            sender=member.nick,
            time=time.localtime(),
            content=('色图' if len(content) == 0 else content)))

    # command dispatcher
    returnMsg = ''
    if '[@ME]' in content:  
        query = content.replace('[@ME]', '').replace('\n', ' ').replace('\r', '').strip()
        handler = commands.get(query.split()[0], None)
        time.sleep(1)
        if handler is None:
            returnMsg = '么得这个功能'
        else:
            returnMsg = handler(query, contact, member)

    # 跌坑除外
    #elif randint(1, 100) <= 5:
    #    time.sleep(2)
    #    returnMsg = content + ('（跌坑除外）' if randint(0, 4) == 0 else '')

    # return
    if returnMsg is not None and len(returnMsg) != 0:
        bot.SendTo(contact, returnMsg)


@register_commands('帮助')
def help(query, contact, member):
    """显示帮助"""
    returnMsg = "这是目前可以公布的情报："
    for k, v in commands.items():
        if k != '帮助':
            returnMsg += '\n{name} -- {doc}'.format(name=k, doc=v.__doc__)
    returnMsg += '\n现在一共有{total}种菜！包括默认菜单{fb}味，群友提供{custom}味'.format(total=len(meal_def)+len(meal), fb=len(meal_def), custom=len(meal))
    return returnMsg

@register_commands('吃什么')
def eating(query, contact, member):
    """随机返回一种吃的"""
    if len(meal_def) + len(meal) == 0:
        return "菜卖完勒，求你加菜！"
    else:
        idx = randint(0, len(meal_def) + len(meal))
        if idx < len(meal_def):
            return "{name}，你阔以选择{meal}".format(name=member.name, meal=meal_def[idx])
        elif idx < len(meal_def) + len(meal):
            return "{name}，你阔以选择{meal}".format(name=member.name, meal=meal[idx - len(meal_def)])


food_blacklist = [
        '你妈',
        '你媽',
        '你母亲',
        '屎',
        '粪',
        '骨灰',
        '哈哈哈',
        'shit',
        'Shit',
        'SHIT',
        'poop',
        '便便',
        '什么',
        '提供',
        '哈哈'
        ]

@register_commands('加菜')
def eating(query, contact, member):
    """添加吃什么菜单"""
    food = query.split(' ', 1)[1]

    if food == '':
        return "空气不能吃的"

    if '/表情' in food:
        return "bot看不懂表情"

    for fb in food_blacklist:
        if fb in food:
            return "你加你妈呢"

    meal.append(food + " ({name}提供)".format(name=member.name))
    with open('meal.txt', 'a') as f:
        f.write(meal[-1] + '\n')
    return "已添加{meal}".format(meal=meal[-1])

#@register_commands('撤回')
def undo(query, contact, member):
    """返回撤回消息，格式：撤回 消息位置"""
    try:
        idx = int(query.split()[1]) - 1
        if idx >= -1:
            raise ValueError
        msg = history[idx]
        return '{who} 发了的xio息是：{detail}'.format(
            who=msg.sender, detail=msg.content)
    except ValueError:
        return "格式或消息位置有问题，请使用如：撤回 -1"
    except IndexError:
        return "么得这条消息，也许是我还没收集到 or 你问的太远"


# To add function:
# use register_commands to register your command handler
# for each handler, you will get the query string, the contact
# object and the member object
