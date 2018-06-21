from random import shuffle
from os import urandom
import time

def randint(l, r):
    return int.from_bytes(urandom(32), 'big') % (r - l) + l

commands = dict()

meal = [
    "盖浇饭", "砂锅", "大排档", "米线", "满汉全席", "西餐", "麻辣烫", "自助餐", "炒面", "冒菜", "水果",
    "西北风", "馄饨", "锅巴饭","麻辣香锅","方便火锅","711","罗森","火锅", "烧烤", "泡面", "水饺", "日料", "涮羊肉",
    "味千拉面", "面包", "扬州炒饭","隆江猪脚饭","煲仔饭","鸡排饭","石锅饭","三明治","凉面","凉皮","饭团",
    "茶餐厅", "海底捞", "披萨", "金拱门", "KFC", "汉堡王", "卡乐星", "兰州拉面", "沙县小吃",
    "烤鱼", "烤肉", "海鲜", "铁板烧", "韩国料理", "粥", "脆皮鸡饭", "萨莉亚", "桂林米粉", "东南亚菜", "甜点",
    "农家菜", "生活", "全家", "黄焖鸡米饭", "群主"
]


def register_commands(command):
    def closure(func):
        commands[command] = func
        return func

    return closure


def onQQMessage(bot, contact, member, content):
    if '大床' not in contact.nick or bot.isMe(contact, member):
        return
    msg = ''
    if '帮助' in content:
        msg += "这是现在可以公布的情报："
        for k, v in commands.items():
            msg += '\n{name} -- {doc}'.format(name=k, doc=v.__doc__)
    elif '[@ME]' in content:  # command dispatcher
        query = content.strip().replace('[@ME]', '')
        handler = commands.get(query.split()[0], None)
        if handler is None:
            msg = '么得这个功能'
        else:
            msg = handler(query, contact, member)
    elif randint(1, 100) <= 5:
        time.sleep(2)
        msg = content + ('（跌坑除外）' if randint(0, 4) == 0 else '')

    bot.SendTo(contact, msg)


@register_commands('吃什么')
def eating(query, contact, member):
    """随机返回一种吃的"""
    shuffle(meal)
    return "{name}，你阔以选择{meal}".format(
        name=member.nick, meal=meal[0])


# To add function:
# use register_commands to register your command handler
# for each handler, you will get the query string, the contact
# object and the member object
