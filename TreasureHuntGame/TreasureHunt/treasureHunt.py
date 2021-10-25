import random
import time
from connectDB import db

def make_log(log):
    db["log"].insert_one(log)
    return

def create_tool(owner, n, i):
    new_tool = {
        'name': ("tool" + str(n)),
        'price': -1,
        'type': 'tool',
        'owner': owner,
        'capability': i,
        'wearing': False
    }
    db['treasures'].insert_one(new_tool)
    simple_tool = {
        'name': ("tool" + str(n)),
        'type': 'tool',
        'capability': i,
    }
    return simple_tool

def create_accessory(owner, n, i):
    new_accessory = {
        'name': ("accessory" + str(n)),
        'price': -1,
        'type': 'accessory',
        'owner': owner,
        'fortune': i/2,
        'wearing': False
    }
    db['treasures'].insert_one(new_accessory)
    simple_accessory = {
        'name': ("accessory" + str(n)),
        'type': 'accessory',
        'fortune': i/2,
    }
    return simple_accessory

def isplayer(username):
    player = db['players'].find_one({'name': username})
    if player == None:
        return 'no'
    return 'yes'

def get_user_info(username):
    player = db['players'].find_one({'name': username})
    if(player == None):
        return 'NONE', 'NONE', 'NONE'
    return player['money'], player['capability'], player['fortune']

def register(player):
    docs = db['players'].find_one({'name': player})
    if (docs != None) :
        return 'Register failed'
    new_player = {
        'name' : player,
        'money' : 1000,
        'capability' : 1,
        'fortune' : 1,
        'lasttime': 0,
        'wear' : [],
        'selling' : [],
        'treasures' : []
    }
    db['players'].insert_one(new_player)
    log = {
        'ops': 'register',
        'time': time.time(),
        'name': player
    }
    make_log(log)
    return 'Register success'

def work(username):
    player = db['players'].find_one({'name':username})
    if (player == None):
        return "ERROR Check username"
    if (time.time() - player["lasttime"]) < 10:
        return 'try again 10 secs later'
    gain = int(player['capability'] * (0.5 + random.random()) * 100)
    db['players'].update_one({'name':username},{'$set': {'lasttime': time.time()},'$inc':{'money':gain}})
    log = {
        'ops': 'work',
        'time': time.time(),
        'name': username,
        'gain': gain,
        'money': player['money'] + gain
    }
    make_log(log)
    return gain

def seek(username):
    player = db['players'].find_one({'name': username})
    if (player == None):
        return "ERROR Check username"
    if (time.time() - player["lasttime"]) < 10:
        return 'try again 10 secs later'
    i = player['fortune'] * (0.6 + random.random())
    rd = random.random()
    if rd > 0.666666 :
        new_treasure = create_tool(username, rd, i)
    else:
        new_treasure = create_accessory(username, rd, i)
    player['treasures'].append(new_treasure)
    db['players'].update_one({'name': username}, {'$set': {'lasttime': time.time(), 'treasures': player['treasures']}})
    log = {
        'ops': "seek",
        'time': time.time(),
        'name': username,
        'treasure': new_treasure,
        'treasures': player['treasures']
    }
    make_log(log)
    return new_treasure

def get_my_treasure(username):
    player = db['players'].find_one({'name': username}, {'_id':0, 'selling': 1, 'wear':1, 'treasures':1})
    if(player == None):
        return "ERROR Check username"
    return player

def check_market():
    market = db['market'].find({},{"_id": 0, 'wearing': 0})
    goods = []
    for good in market:
        goods.append(good)
    return goods

def check_my_market(username):
    player = db['players'].find_one({'name': username})
    if (player == None):
        return "ERROR Check username"
    taxrate = 1.2
    money_buy = int(player['money'] / taxrate)
    market = db['market'].find({'price': {'$lte': money_buy}, 'owner': {'$ne': username}}, {"_id": 0, 'wearing': 0})
    goods = []
    for good in market:
        goods.append(good)
    return goods

def check_my_treasure(username):
    docs = db["treasures"].find({"owner": username},{"_id": 0})
    treasures = []
    for treasure in docs:
        treasures.append(treasure)
    return treasures

def wear(username,treasurename):
    treasure = db['treasures'].find_one({'name': treasurename, 'owner': username})
    if (treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == True) or (treasure['price'] != -1):
        return "Treasure wearing or selling"
    player = db['players'].find_one({'name': username})
    wears = player['wear']
    if (treasure['type'] == 'tool'):
        replacetreasure = db['treasures'].find_one_and_update({'owner': username, 'wearing': True, 'type': 'tool'},  {'$set': {'wearing': False}})
        db['treasures'].update_one({'name': treasurename}, {'$set': {'wearing': True}})
        log = {
            'ops': "wear",
            'time': time.time(),
            'name': username,
            'treasure': treasurename,
        }
        if replacetreasure != None:
            wears.remove(replacetreasure['name'])
            log['replace'] = replacetreasure['name']
        wears.append(treasurename)
        db['players'].update_one({'name': username},{'$set': {'capability': treasure['capability'],'wear': wears}})
        log['wear'] = wears
        make_log(log)
        return 'Wear success'
    else:
        docs = db['treasures'].find({'owner': username, 'wearing': True, 'type': 'accessory'})
        ftn = 0
        log = {
            'ops': 'wear',
            'time': time.time(),
            'name': username,
            'treasure': treasurename
        }
        if (docs.count() >= 2):
            docs.sort('fortune')
            doc = docs[0]
            ftn = doc['fortune']
            wears.remove(doc['name'])
            db['treasures'].update_one({'name': doc['name']}, {'$set': {'wearing': False}})
            log['replace'] = doc["name"]
        wears.append(treasurename)
        db['players'].update_one({'name': username}, {'$set': {'wear': wears}, '$inc':{'fortune': treasure['fortune']-ftn}})
        db['treasures'].update_one({'name': treasurename}, {'$set': {'wearing': True}})
        log['wear'] = wears
        make_log(log)
        return 'Wear success'

def unwear(username,treasurename):
    treasure = db['treasures'].find_one({'name': treasurename, 'owner': username})
    if (treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == False):
        return 'U R not wearing it'
    player = db['players'].find_one({'name': username})
    wears = player['wear']
    wears.remove(treasurename)
    db['treasures'].update_one({'_id': treasure['_id']}, {'$set': {'wearing': False}})
    if (treasure['type'] == 'tool'):
        db['players'].update_one({'name': username}, {'$set': {'capability': 1, 'wear': wears}})
    else:
        db['players'].update_one({'name': username}, {'$set': {'wear': wears}, '$inc': {'fortune': -treasure['fortune']}})
    log = {
        'ops': 'unwear',
        'time': time.time(),
        'name': username,
        'treasure': treasurename,
        'wear': wears
    }
    make_log(log)
    return 'Unwear success'

def sell(username, treasurename, price):
    if (price < 0):
        return 'NI ZHEN SHI GE SHENG YI TIAN CAI'
    treasure = db['treasures'].find_one({'name': treasurename, 'owner': username})
    if (treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == True):
        return "Treasure wearing"
    player = db['players'].find_one({'name': username})
    treasure['price'] = price
    if (treasure['name'] not in player['selling']):
        player['selling'].append(treasure['name'])
        db['players'].update_one({'name': username}, {'$set': {'selling': player['selling']}})
        db['market'].insert_one(treasure)
    else:
        db['market'].update_one({'name': treasurename},{'$set': {'price': price}})
    db['treasures'].update_one({'name': treasurename},{'$set': {'price': price}})
    log = {
        'ops': 'sell',
        'time': time.time(),
        'name': username,
        'treasure': treasurename,
        'price': price,
        'selling': player['selling']
    }
    make_log(log)
    return 'Selling success'

def callback(username, treasurename):
    treasure = db['market'].find_one_and_delete({'name': treasurename, 'owner': username})
    if (treasure == None):
        return "ERROR Check username&treasurename"
    player = db['players'].find_one({'name': username})
    db['treasures'].update_one({'name': treasurename}, {'$set': {'price': -1}})
    player['selling'].remove(treasure['name'])
    db['players'].update_one({'name': username}, {'$set': {'selling': player['selling']}})
    log = {
        'ops': 'callback',
        'time': time.time(),
        'name': username,
        'treasure': treasurename,
        'selling': player['selling']
    }
    make_log(log)
    return 'Callback success'

def sold(username1, username2, treasurename):
    treasure = db['market'].find_one_and_delete({'name': treasurename})
    if (treasure == None):
        return "ERROR Check treasurename"
    players = db['players'].find({'$or': [{'name': username1}, {'name': username2}]})
    player1 = None
    player2 = None
    for tempplayer in players:
        if treasure['owner'] == tempplayer['name']:
            player1 = tempplayer
        else:
            player2 = tempplayer
    if (player1 == None) or (player2 == None):
        db['market'].insert_one(treasure)
        return "ERROR Check username"
    taxrate = 1.2
    realprice = int(treasure['price'] * taxrate)
    if (player2['money'] < realprice):
        db['market'].insert_one(treasure)
        # Soviet_Joke = False
        # if(Soviet_Joke == True):
        #     revolution_fee = int(treasure['price'] * (taxrate - 1))
        #     if(player2['money'] >= revolution_fee):
        #         db['players'].update_one({'name': player2['name']}, {'$inc': {'money': -revolution_fee}})
        #         log = {
        #             'ops': 'revolution_fee',
        #             'time': time.time(),
        #             'name': player2['name'],
        #             'gain': -revolution_fee,
        #             'money': player2['money'] - revolution_fee
        #         }
        #         make_log(log)
        #         return "The beer has been sold out."
        return "NI GE QIONG B"
    for simple_treasure in player1['treasures']:
        if simple_treasure['name'] == treasurename:
            player1['treasures'].remove(simple_treasure)
            break
    player1['selling'].remove(treasurename)
    player2['treasures'].append(simple_treasure)
    db['players'].update_one({'name': player1['name']},
                             {'$set': {'treasures': player1['treasures'], 'selling': player1['selling']},
                              '$inc': {'money': treasure['price']}})
    db['players'].update_one({'name': player2['name']},
                             {'$set': {'treasures': player2['treasures']}, '$inc': {'money': -realprice}})
    db['treasures'].update_one({'name': treasurename}, {'$set': {'owner': username2, 'price': -1}})
    log1 = {
        'ops': 'sold',
        'time': time.time(),
        'name': player1['name'],
        'buyer': player2['name'],
        'treasure': treasurename,
        'price': treasure["price"],
        'treasures': player1['treasures'],
        'money': player1['money'] + treasure['price']
    }
    make_log(log1)
    log2 = {
        'ops': 'buy',
        'time': time.time(),
        'seller': player1['name'],
        'name': player2['name'],
        'treasure': treasurename,
        'price': realprice,
        'treasures': player2['treasures'],
        'money': player2['money'] - realprice
    }
    make_log(log2)
    return 'Buy success'

def rename(username,treasurename,newtreasurename):
    treasure = db['treasures'].find_one({'name': treasurename, 'owner': username})
    if (treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == True) or (treasure['price'] != -1):
        return "Treasure wearing or selling"
    testtreasure = db['treasures'].find_one({'name': newtreasurename})
    if (testtreasure != None) :
        return "Change newtreasurename"
    player = db['players'].find_one({'name': username})
    for simple_treasure in player['treasures']:
        if (simple_treasure['name'] == treasurename):
            player['treasures'].remove(simple_treasure)
            break
    simple_treasure['name'] = newtreasurename
    player['treasures'].append(simple_treasure)
    db['players'].update_one({'name': username},
                             {'$set': {'treasures': player['treasures']}})
    db['treasures'].update_one({'name': treasurename}, {'$set': {'name': newtreasurename}})
    log = {
        'ops': 'rename',
        'time': time.time(),
        'name': username,
        'treasure': treasurename,
        'newname': newtreasurename,
    }
    make_log(log)
    return "Rename success"

def drop(username,treasurename):
    treasure = db['treasures'].find_one({'name': treasurename, 'owner': username})
    if (treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == True) or (treasure['price'] != -1):
        return "Treasure wearing or selling"
    player = db['players'].find_one({'name': username})
    for simple_treasure in player['treasures']:
        if (simple_treasure['name'] == treasurename):
            player['treasures'].remove(simple_treasure)
            break
    db['treasures'].delete_one({'name': treasurename, 'owner': username})
    db['players'].update_one({'name': username},
                             {'$set': {'treasures': player['treasures']}})
    log = {
        'ops': 'drop',
        'time': time.time(),
        'name': username,
        'treasure': treasurename,
        'treasures': player['treasures']
    }
    make_log(log)
    return "Drop success"

def remove(username):
    player = db["players"].find_one_and_delete({"name": username})
    if (player == None):
        return "ERROR Check username"
    db["market"].delete_many({"owner": username})
    db["treasures"].delete_many({"owner": username})
    log = {
        'ops': 'remove',
        'time': time.time(),
        'name': username,
    }
    make_log(log)
    return "BYE"

def history(username, number):
    logs = db['log'].find({"name": username}, {"_id": 0, 'name': 0})
    if (logs.count() == 0):
        return "ERROR Check username"
    logs.sort('time')
    history = []
    i = 1
    for log in logs:
        log['seq'] = i
        del log["time"]
        history.append(log)
        i += 1
    if (i > number):
        return history[(i-number-1):]
    else:
        return history