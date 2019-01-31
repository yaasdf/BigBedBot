# -*- coding: utf-8 -*-
from random import shuffle
from os import urandom
from collections import namedtuple
import time

from cqsdk import CQBot, CQAt, RcvdPrivateMessage, RcvdGroupMessage, SendGroupMessage

qqbot = CQBot(11235)
CQATME = "[CQ:at,qq=3303205712]"

def randint(l, r):
    value = int.from_bytes(urandom(32), 'big') % (r - l) + l
    print('[randint] [%d ~ %d] 返回了 %d', l, r, value)
    return value


commands = dict()

meal_def = []
meal = []
drink = []
try:
    with open('meal_def.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            meal_def.append(line.strip())
except FileNotFoundError:
    print('路径出错啦，没有找到默认菜单！')

try:
    with open('meal.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            meal.append(line.strip())
except FileNotFoundError:
    print('路径出错啦，没有找到群友菜单！')

try:
    with open('drink.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            if len(line.strip()) > 0 and line[0] != '#':
                drink.append(line.strip())
except FileNotFoundError:
    print('路径出错啦，没有找到饮料菜单！')
    
def register_commands(command):
    def closure(func):
        commands[command] = func
        return func

    return closure


def getFood(idx):
    if idx < len(meal_def):
        return meal_def[idx]
    elif idx < len(meal_def) + len(meal):
        return meal[idx - len(meal_def)]


@register_commands('帮助')
def help(at, qq, query):
    """显示帮助"""
    returnMsg = "这是目前可以公布的情报："
    for k, v in commands.items():
        if k != '帮助':
            returnMsg += '\n{name} -- {doc}'.format(name=k, doc=v.__doc__)
    returnMsg += '\n现在一共有{total}种菜！包括默认菜单{fb}味，群友提供{custom}味'.format(total=len(meal_def)+len(meal), fb=len(meal_def), custom=len(meal))
    return returnMsg

@register_commands('吃什么')
def eating(at, qq, query):
    """随机返回一种吃的"""
    if len(meal_def) + len(meal) == 0:
        return "菜卖完勒，求你加菜！"
    else:
        idx = randint(0, len(meal_def) + len(meal))
        return "{name}，你阔以选择{meal}".format(name=at, meal=getFood(idx))

@register_commands('喝什么')
def drinking(at, qq, query):
    """随机返回一种喝的"""
    if len(drink) == 0:
        return "?"
    else:
        idx = randint(0, len(drink))
        return "{name}，你阔以选择{meal}".format(name=at, meal=drink[idx])

@register_commands('玩什么')
def playing(at, qq, query):
    """问就是L"""
    return "L"

@register_commands('吃什么十连')
def eating10(at, qq, query):
    """审判的时间到了"""
    ret = '{name}，你阔以选择：\n'.format(name=at)
    foods = []
    for i in range(0, 10):
        foods.append(randint(0, len(meal_def) + len(meal)))
    foods.sort()
    for f in foods:
        ret += '- ' + getFood(f) + '\n'
    ret += "吃东西还十连，祝您撑死，哈哈"
    return ret

food_blacklist = [
        '你妈',
        '你媽',
        '你吗',
        '你爸',
        '你娘',
        '你爹',
        '你母亲',
        '屎',
        '粪',
        '骨灰',
        'shit',
        'Shit',
        'SHIT',
        'poop',
        '便便',
        '什么',
        '提供',
        '哈哈',
        '小号',
        '群主',
        '杀了'
        ]

@register_commands('加菜')
def eating(at, qq, query):
    """添加吃什么菜单"""
    food = query.split(' ', 1)[1]
    food = food.split('\n', 1)[0].strip()
    #air
    if food == '':
        return "空气不能吃的"
    #默认菜单过滤
    if food in meal_def:
        return "{meal}已经有了！！！！".format(meal=food)
    #添加菜单过滤
    for fd in meal:
        if food == fd.split(' ', 1)[0]:
            return "{meal}已经有了！！！！".format(meal=food)
    #表情过滤
    if '/表情' in food or '/Emoji' in food:
        return "bot看不懂表情"
    #黑名单过滤
    for fb in food_blacklist:
        if fb in food:
            return "你加你妈呢"
    #meal.append(food + " ({name}提供)".format(name=at))
    meal.append(food)
    with open('meal.txt', 'a', encoding='UTF-8') as f:
        f.write(meal[-1] + '\n')
    return "已添加{meal}".format(meal=meal[-1])
    
    
@register_commands('菜单')
def eating(at, qq, query):
    """查找指定位置附近的菜单"""
    start = 0
    end = 0
    total_len = len(meal_def) + len(meal)
    #没有指定长度，返回最后9条
    if len(query.split(' ', 1)) == 1 or not query.split(' ', 1)[1].isdecimal():
        end = total_len
        start = end - 9
    else:
        mid = int(query.split(' ', 1)[1]) - 1
        start = mid - 4
        end = mid + 4 + 1
    #边界
    if start < 0:
        start = 0
        end = start + 9
    if end > total_len:
        end = total_len
        start = end - 9 
    if start < 0:
        start = 0
    #遍历返回   
    if end == 0:
        return "没菜！"
    ret = ''
    for idx in range(start, end):
        ret += "{index}: {food}\n".format(index=idx + 1, food=getFood(idx))
    return ret.rstrip('\n')

#@register_commands('撤回')
def undo(at, qq, query):
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




        
        
        
def onQQMessage(at, qq, content):
    # availability filter
    if at == CQATME:
        return
    # command dispatcher
    returnMsg = ''
    if CQATME in content:  
        query = content.replace(CQATME, '').replace('\n', ' ').replace('\r', '').strip()
        handler = commands.get(query.split()[0], None)
        time.sleep(1)
        if handler is None:
            returnMsg = '么得这个功能'
        else:
            returnMsg = handler(at, qq, query)
    else:
        query = content
        handler = commands.get(query.split()[0], None)
        if handler is not None:
            time.sleep(1)
            returnMsg = handler(at, qq, query)
    # 跌坑除外
    #elif randint(1, 100) <= 5:
    #    time.sleep(2)
    #    returnMsg = content + ('（跌坑除外）' if randint(0, 4) == 0 else '')
    return returnMsg

# To add function:
# use register_commands to register your command handler
# for each handler, you will get the query string, the contact
# object and the member object

@qqbot.listener((RcvdGroupMessage, ))
def procmsg(message):
    msg = onQQMessage(CQAt(message.qq), message.qq, message.text)
    if msg is not None and len(msg) > 0:
        qqbot.send(SendGroupMessage(
            group=message.group,
            text=msg
        ))

if __name__ == '__main__':
    try:
        qqbot.start()
        # scheduler.start()
        print("Running...")
        input()
        print("Stopping...")
    except KeyboardInterrupt:
        pass
