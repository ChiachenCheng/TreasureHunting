from connectDB import Player,Treasure,Log,Log_overflow,Market,connect
from sqlalchemy.sql import select,update,and_,delete,desc
import random
import time
import decimal
import hashlib

def gettime():
    return decimal.Decimal.from_float(time.time())

def encrypt(pw):
    hash = hashlib.md5()
    hash.update(pw.encode('utf-8'))
    return hash.hexdigest()

def select_player(username):
    sql = select([Player]).where(Player.c.pname == username)
    result = connect.execute(sql)
    player = result.first()
    if(player == None):
        return None
    user = {
        'pname': username,
        'passwd': player.passwd,
        'money': player.money,
        'capability': player.capability,
        'fortune': player.fortune,
        'lasttime': player.lasttime,
        'login': player.login
    }
    return user

# def update_player(user): #the first version, stop using
#     sql = update(Player).where(Player.c.pname == user['pname'])
#     sql = sql.values(
#         money = user['money'],
#         capability = user['capability'],
#         fortune = user['fortune'],
#         lasttime = user['lasttime']
#     )
#     result = connect.execute(sql)
#     return result.rowcount

def update_player_inc(username,money=0,capability=0,fortune=0):
    sql = update(Player).where(Player.c.pname == username)
    sql = sql.values(
        money=(Player.c.money+money),
        capability=(Player.c.capability+capability),
        fortune=(Player.c.fortune+fortune),
    )
    result = connect.execute(sql)
    return result.rowcount

def update_player_set(username,passwd=-1,money=-1,capability=-1,fortune=-1,lasttime=-1,login=-1):
    sql = update(Player).where(Player.c.pname == username)
    if passwd != -1:
        sql = sql.values(passwd=passwd)
    if money != -1:
        sql = sql.values(money=money)
    if capability != -1:
        sql = sql.values(capability=capability)
    if fortune != -1:
        sql = sql.values(fortune=fortune)
    if lasttime != -1:
        sql = sql.values(lasttime=lasttime)
    if login != -1:
        sql = sql.values(login=login)
    result = connect.execute(sql)
    return result.rowcount

def insert_treasure(owner, fortune):
    rd = random.random()
    i = fortune * (0.5 + random.random())
    if rd > 0.666666 :
        ttype = 'tool'
    else:
        ttype = 'accessory'
        i = i / 2
    ins = Treasure.insert().values(
        tname=ttype+str(rd),
        type=ttype,
        value=i,
        owner=owner
    )
    connect.execute(ins)
    tnew = {
        'tname': ttype+str(rd),
        'type': ttype,
        'value': i,
    }
    return tnew

def select_treasure(username, treasurename):
    sql = select([Treasure]).where(and_(Treasure.c.owner == username, Treasure.c.tname == treasurename))
    result = connect.execute(sql)
    treasure = result.first()
    if(treasure == None):
        return None
    trea = {
        'tname': treasurename,
        'type': treasure.type,
        'value': treasure.value,
        'owner': username,
        'wearing': treasure.wearing,
        'price': treasure.price
    }
    return trea

# def update_treasure(username,treasuername,treasure): #the first version, stop using
#     sql = update(Treasure).where(and_(Treasure.c.owner == username, Treasure.c.tname == treasuername))
#     sql = sql.values(
#         tname = treasure['tname'],
#         owner = treasure['owner'],
#         wearing = treasure['wearing'],
#         price = treasure['price']
#     )
#     result = connect.execute(sql)
#     return result.rowcount

def update_treasure(username,treasuername,tname=-1,owner=-1,wearing=-1,price=-1):
    sql = update(Treasure).where(and_(Treasure.c.owner == username, Treasure.c.tname == treasuername))
    if tname != -1:
        sql = sql.values(tname = tname)
    if owner != -1:
        sql = sql.values(owner = owner)
    if wearing != -1:
        sql = sql.values(wearing = wearing)
    if price != -1:
        sql = sql.values(price = price)
    result = connect.execute(sql)
    return result.rowcount

# def select_and_update_treasure(username,treasuername,tname=-1,owner=-1,wearing=-1,price=-1): #not been used,useable
#     sql = update(Treasure).where(and_(Treasure.c.owner == username, Treasure.c.tname == treasuername)).returning(Treasure)
#     if tname != -1:
#         sql = sql.values(tname = tname)
#     if owner != -1:
#         sql = sql.values(owner = owner)
#     if wearing != -1:
#         sql = sql.values(wearing = wearing)
#     if price != -1:
#         sql = sql.values(price = price)
#     result = connect.execute(sql)
#     treasure = result.first()
#     if (treasure == None):
#         return None
#     trea = {
#         'tname': treasure.tname,
#         'type': treasure.type,
#         'value': treasure.value,
#         'owner': treasure.owner,
#         'wearing': treasure.wearing,
#         'price': treasure.price
#     }
#     return trea

def replace_tool(owner):
    sql = update(Treasure).where(and_(Treasure.c.owner == owner, Treasure.c.type == 'tool', Treasure.c.wearing == True))
    sql = sql.values(wearing=False)
    result = connect.execute(sql)
    return result.rowcount

def replace_accessory(owner):
    sql = select([Treasure]).where(and_(Treasure.c.owner == owner, Treasure.c.type == 'accessory', Treasure.c.wearing == True))
    sql = sql.order_by(Treasure.c.value)
    result = connect.execute(sql)
    if (result.rowcount >= 2):
        treasure = result.first()
        trea = {
            'tname': treasure.tname,
            'type': treasure.type,
            'value': treasure.value,
            'owner': owner,
            'wearing': False,
            'price': treasure.price
        }
        update_treasure(owner,trea['tname'],wearing=False)
        return trea
    return None

def make_log(log):
    t = gettime()
    over = False
    li = []
    for k, v in log.items():
        if(k == 'ops')or(k == 'pname')or(k =='tname'):
            continue
        over = True
        i = {
            'time': t,
            'attr': k,
            'value': str(v)
        }
        li.append(i)
    sql = Log.insert().values(
        ops = log['ops'],
        time = t,
        pname = log['pname'],
        overflow = over
    )
    if 'tname' in log.keys():
        sql = sql.values(tname=log['tname'])
    result = connect.execute(sql)
    if over == True:
        ins = Log_overflow.insert()
        result = connect.execute(ins, li)
    return 1

def select_market(username, treasurename):
    sql = select([Market]).where(and_(Market.c.owner == username, Market.c.tname == treasurename))
    result = connect.execute(sql)
    treasure = result.first()
    if(treasure == None):
        return None
    trea = {
        'tname': treasurename,
        'type': treasure.type,
        'value': treasure.value,
        'owner': username,
        'wearing': treasure.wearing,
        'price': treasure.price
    }
    return trea