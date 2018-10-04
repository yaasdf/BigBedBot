from random import shuffle
from os import urandom
from collections import namedtuple
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
    return int.from_bytes(urandom(32), 'big') % (r - l) + l


commands = dict()
history = MsgContainer(50)

meal = [
    "盖浇饭", "砂锅", "大排档", "米线", "满汉全席", "西餐", "麻辣烫", "自助餐", "炒面", "冒菜", "水果",
    "西北风", "馄饨", "锅巴饭","麻辣香锅","方便火锅","711","罗森","火锅", "烧烤", "泡面", "水饺", "日料", "涮羊肉",
    "味千拉面", "面包", "扬州炒饭","隆江猪脚饭","煲仔饭","鸡排饭","石锅饭","三明治","凉面","凉皮","饭团",
    "茶餐厅", "海底捞", "披萨", "金拱门", "KFC", "汉堡王", "卡乐星", "兰州拉面", "沙县小吃",
    "烤鱼", "烤肉", "海鲜", "铁板烧", "韩国料理", "粥", "脆皮鸡饭", "萨莉亚", "桂林米粉", "东南亚菜", "甜点",
    "农家菜", "生活", "全家", "黄焖鸡米饭", "群主", 
    "虾饺", "斋肠", "牛肉肠", "叉烧肠", "虾肠", "红米肠", "烧卖", "牛肉烧卖", "糯米鸡","珍珠鸡", 
    "凤爪", "白云凤爪", "蒜蓉排骨", "炸云吞", "炸春卷", "煎虾米肠", "鱿鱼酥", "金钱肚", "叉烧包",
    "流沙包", "奶黄包", "茅根粥", "皮蛋瘦肉粥", "蛋挞", "椰子布丁", "双皮奶", "马拉糕", "烤田鸡肉", 
    "蟹煲", "香辣虾", "香辣蟹", "小龙虾", "酸汤肥牛", "椒盐皮皮虾", "芝士年糕", "火锅", 
    "口水鸡", "藤椒鸡", "周黑鸭", "鸭翅", "鸭脖", "鸭锁骨", "鸭腿", "香辣鳗鱼条", "鱿鱼丝", 
    "三文鱼刺身", "蒲烧鳗鱼", "帝王蟹柳", "鲜芋仙", "仙草芋圆", "杨枝甘露", "芒果西米", 
    "寿司食べたい", "拉面", "意大利面", "披萨", "可口可乐", "旺仔牛奶", "板烧", "巨无霸", 
    "吮指原味鸡", "云吞面", "麻辣烫", "手抓饼", "盆菜", "冒菜", "豆花", "爆浆鸡排", "车仔面", 
    "叉烧", "烧鹅", "干炒牛河", "田螺", "水饺", "串", "巧克力", "可可脆片", "脱水饼干", 
    "炒板栗", "龟龄膏", "鸳鸯馒头", "蛋糕", "博多", "蛋挞", "小笼包", "兰州拉面", "冚家便当", 
    "海底捞", "鸡肉卷"
])


def register_commands(command):
    def closure(func):
        commands[command] = func
        return func

    return closure


def onQQMessage(bot, contact, member, content):
    if '大床' not in contact.nick or bot.isMe(contact, member):
        return
    history.append(
        MsgTuple(
            sender=member.nick,
            time=time.localtime(),
            content=('色图' if len(content) == 0 else content)))
    returnMsg = ''
    if '帮助' in content:
        returnMsg += "这是现在可以公布的情报："
        for k, v in commands.items():
            returnMsg += '\n{name} -- {doc}'.format(name=k, doc=v.__doc__)
    elif '[@ME]' in content:  # command dispatcher
        query = content.strip().replace('[@ME]', '')
        handler = commands.get(query.split()[0], None)
        if handler is None:
            returnMsg = '么得这个功能'
        else:
            returnMsg = handler(query, contact, member)
    elif randint(1, 100) <= 5:
        time.sleep(2)
        returnMsg = content + ('（跌坑除外）' if randint(0, 4) == 0 else '')

    if returnMsg is not None and len(returnMsg) != 0:
        bot.SendTo(contact, returnMsg)


@register_commands('吃什么')
def eating(query, contact, member):
    """随机返回一种吃的"""
    shuffle(meal)
    return "{name}，你阔以选择{meal}".format(name=member.nick, meal=meal[0])


@register_commands('撤回')
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
