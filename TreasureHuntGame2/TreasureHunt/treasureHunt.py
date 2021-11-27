from TreasureHunt.func import *

def login(username,password):
    player = select_player(username)
    ciphertext = encrypt(password)
    if (player == None)or(ciphertext != player['passwd']):
        return 'ERROR Check username&password'
    update_player_set(username,login=True)
    log = {
        'ops': 'login',
        'pname': player
    }
    return 'Login success'

def logout(username):
    rows = update_player_set(username,login=False)
    if(rows < 1):
        return "ERROR Check username"
    log = {
        'ops': 'logout',
        'pname': username
    }
    return "Logout success"

def register(player,password):
    if (len(player) >= 64):
        return "ERROR too long username"
    docs = select_player(player)
    if docs != None:
        return 'Register failed'
    ciphertext = encrypt(password)
    ins = Player.insert().values(
        pname=player,
        passwd=ciphertext
    )
    result = connect.execute(ins)
    log = {
        'ops': 'register',
        'pname': player,
        'passwd': ciphertext
    }
    make_log(log)
    return 'Register success'

def work(username):
    player = select_player(username)
    if (player == None):
        return "ERROR Check username"
    if (player['login'] == False):
        return "Please login"
    if (gettime() - player["lasttime"]) < 10:
        return 'try again 10 secs later'
    gain = int(player['capability'] * (0.5 + random.random()) * 100)
    update_player_set(username,money=(player['money'] + gain),lasttime=gettime())
    log = {
        'ops': 'work',
        'pname': username,
        'gain': gain
    }
    make_log(log)
    return gain

def seek(username):
    player = select_player(username)
    if (player == None):
        return "ERROR Check username"
    if (player['login'] == False):
        return "Please login"
    if (gettime() - player["lasttime"]) < 10:
        return 'try again 10 secs later'
    new_treasure = insert_treasure(username, player['fortune'])
    update_player_set(username,lasttime=gettime())
    log = {
        'ops': "seek",
        'pname': username,
        'tname': new_treasure['tname'],
        'type': new_treasure['type'],
        'value': new_treasure['value']
    }
    make_log(log)
    return new_treasure

def get_user_info(username):
    player = select_player(username)
    if(player == None):
        return 'NONE', 'NONE', 'NONE'
    if (player['login'] == False):
        return "Please login", "Please login", "Please login"
    return player['money'], player['capability'], player['fortune']

def check_market():
    sql = select([Market])
    result = connect.execute(sql)
    if (result == None):
        return None
    treasures = []
    for treasure in result:
        trea = {
            'tname': treasure.tname,
            'type': treasure.type,
            'value': treasure.value,
            'owner': treasure.owner,
            'price': treasure.price
        }
        treasures.append(trea)
    return treasures

def check_my_market(username):
    player = select_player(username)
    if (player == None):
        return "ERROR Check username"
    if (player['login'] == False):
        return "Please login"
    taxrate = 1.2
    money_buy = int(player['money'] / taxrate)
    sql = select([Market]).where(Market.c.price <= money_buy)
    result = connect.execute(sql)
    if (result == None):
        return None
    treasures = []
    for treasure in result:
        trea = {
            'tname': treasure.tname,
            'type': treasure.type,
            'value': treasure.value,
            'owner': treasure.owner,
            'price': treasure.price
        }
        treasures.append(trea)
    return treasures

def check_my_treasure(username):
    sql = select([Treasure]).where(Treasure.c.owner == username)
    result = connect.execute(sql)
    if (result == None):
        return None
    treasures = []
    for treasure in result:
        trea = {
            'tname': treasure.tname,
            'type': treasure.type,
            'value': treasure.value,
            'wearing': treasure.wearing,
        }
        if treasure.price != None:
            trea['selling'] = True
            trea['price'] = treasure.price
        else:
            trea['selling'] = False
        treasures.append(trea)
    return treasures

def wear(username,treasurename):
    player = select_player(username)
    if (player == None):
        return "ERROR Check username"
    if (player['login'] == False):
        return "Please login"
    treasure = select_treasure(username,treasurename)
    if (treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == True) or (treasure['price'] != None):
        return "Treasure wearing or selling"
    if (treasure['type'] == 'tool'):
        replace_tool(username)
        update_player_set(username,capability=treasure['value'])
    else:
        replace = replace_accessory(username)
        f = treasure['value']
        if (replace != None):
            f -= replace['value']
        update_player_inc(username,fortune=f)
    update_treasure(username,treasurename,wearing=True)
    log = {
        'ops': "wear",
        'pname': username,
        'tname': treasurename,
    }
    make_log(log)
    return 'Wear success'

def unwear(username,treasurename):
    player = select_player(username)
    if (player == None):
        return "ERROR Check username"
    if (player['login'] == False):
        return "Please login"
    treasure = select_treasure(username,treasurename)
    if (treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == False):
        return 'U R not wearing it'
    update_treasure(username,treasurename,wearing=False)
    if (treasure['type'] == 'tool'):
        update_player_set(username,capability=1.0)
    else:
        update_player_inc(username,fortune=-treasure['value'])
    log = {
        'ops': 'unwear',
        'pname': username,
        'tname': treasurename,
    }
    make_log(log)
    return 'Unwear success'

def sell(username, treasurename, price):
    if (price < 0):
        return 'NI ZHEN SHI GE SHENG YI TIAN CAI'
    player = select_player(username)
    if (player == None):
        return "ERROR Check username"
    if (player['login'] == False):
        return "Please login"
    treasure = select_treasure(username,treasurename)
    if (treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == True):
        return "Treasure wearing"
    update_treasure(username,treasurename,price=price)
    log = {
        'ops': 'sell',
        'pname': username,
        'tname': treasurename,
        'price': price
    }
    make_log(log)
    return 'Selling success'

def callback(username, treasurename):
    rows = update_treasure(username,treasurename,price=None)
    if (rows < 1):
        return "ERROR Check username&treasurename"
    log = {
        'ops': 'callback',
        'pname': username,
        'tname': treasurename
    }
    make_log(log)
    return 'Callback success'

def sold(username1, username2, treasurename):
    treasure = select_market(username1,treasurename)
    treatest = select_treasure(username2,treasurename)
    if (treasure == None or treatest != None):
        return "ERROR Check treasurename"
    buyer = select_player(username2)
    if (buyer['login'] == False):
        return "Please login"
    taxrate = 1.2
    price = treasure['price']
    realprice = int(treasure['price'] * taxrate)
    if (buyer['money'] < realprice):
        # Soviet_Joke = False
        # if(Soviet_Joke == True):
        #     revolution_fee = int(treasure['price'] * (taxrate - 1))
        #     if(buyer['money'] >= revolution_fee):
        #         update_player_inc(username2,money=-revolution_fee)
        #         log = {
        #             'ops': 'revo_fee',
        #             'name': buyer['name'],
        #             'gain': -revolution_fee,
        #         }
        #         make_log(log)
        #         return "The beer has been sold out."
        return "NI GE QIONG B"
    update_player_inc(username1,money=price)
    update_player_inc(username2,money=-realprice)
    update_treasure(username1,treasurename,owner=username2,price=None)
    log1 = {
        'ops': 'sold',
        'pname': username1,
        'buyer': buyer['pname'],
        'tname': treasurename
    }
    make_log(log1)
    log2 = {
        'ops': 'buy',
        'seller': username1,
        'pname': buyer['pname'],
        'tname': treasurename
    }
    make_log(log2)
    return 'Buy success'

def rename(username,treasurename,newtreasurename):
    if (len(newtreasurename) >= 64):
        return "ERROR too long treasurename"
    testtreasure = select_treasure(username,newtreasurename)
    if (testtreasure != None) :
        return "Change newtreasurename"
    rows = update_treasure(username,treasurename,tname=newtreasurename)
    if (rows < 1):
        return "ERROR Check username&treasurename"
    log = {
        'ops': 'rename',
        'pname': username,
        'tname': treasurename,
        'newname': newtreasurename
    }
    make_log(log)
    return "Rename success"

def drop(username,treasurename):
    player = select_player(username)
    if (player == None):
        return "ERROR Check username"
    if (player['login'] == False):
        return "Please login"
    sql = delete(Treasure).where(and_(Treasure.c.owner == username, Treasure.c.tname == treasurename)).returning(Treasure)
    result = connect.execute(sql)
    treasure = result.first()
    if (result.rowcount == 0 or treasure == None):
        return "ERROR Check username&treasurename"
    if (treasure['wearing'] == True):
        if (treasure['type'] == 'tool'):
            update_player_set(username, capability=1.0)
        else:
            update_player_inc(username, fortune=-treasure['value'])
    log = {
        'ops': 'drop',
        'pname': username,
        'tname': treasurename
    }
    make_log(log)
    return "Drop success"

def remove(username):
    player = select_player(username)
    if (player == None):
        return "ERROR Check username"
    if (player['login'] == False):
        return "Please login"
    sql = delete(Treasure).where(Treasure.c.owner == username)
    result = connect.execute(sql)
    sql = delete(Player).where(Player.c.pname == username)
    result = connect.execute(sql)
    if (result.rowcount < 1):
        return "ERROR Check username"
    log = {
        'ops': 'remove',
        'pname': username
    }
    make_log(log)
    return "BYE"

def history(username, number):
    sql = select([Log]).where(Log.c.pname == username).order_by(desc(Log.c.time)).limit(number)
    result = connect.execute(sql)
    if (result.rowcount == 0):
        return "ERROR Check username"
    history = []
    i = 1
    for log in result:
        if log.ops == 'remove':
            break
        tlog = {
            'NO.': i,
            'ops': log.ops,
            'pname': log.pname,
            'tname': log.tname,
        }
        if log.overflow == True:
            sql_o = select([Log_overflow]).where(Log_overflow.c.time == log.time)
            result_o = connect.execute(sql_o)
            for log_o in result_o:
                tlog[log_o.attr] = log_o.value
        history.append(tlog)
        i += 1
    return history

def changepw(username,oldpw,newpw,newpwagain):
    if (newpw != newpwagain):
        return "ERROR check newpassword"
    player = select_player(username)
    ciphertext = encrypt(oldpw)
    if (player == None):
        return 'ERROR Check username&password'
    if (player['login'] == False):
            return "Please login"
    if (ciphertext != player['passwd']):
        return 'ERROR Check username&password'
    newciphertext = encrypt(newpw)
    update_player_set(username,passwd=newciphertext)
    log = {
        'ops': 'changepw',
        'pname': username,
        'newpw': newciphertext
    }
    return "Change password success"