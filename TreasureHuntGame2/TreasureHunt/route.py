import flask
from flask import Blueprint
from flask import jsonify
from flask import request
from TreasureHunt.treasureHunt import *

bp = Blueprint("TreasureHuntGame", __name__, url_prefix="/")

@bp.route('/')
def index():
    return flask.render_template('index.html', has_result=False)

@bp.route('/signup', methods=['POST'])
def user_register():
    username = request.form.get('username')
    password = request.form.get('password')
    status = register(username,password)
    if (status == 'Register success'):
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0})

@bp.route('/login', methods=['POST'])
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')
    status = login(username,password)
    if (status == 'Login success'):
        return jsonify({'success': 1})
    else:
        return jsonify({'success': 0})

@bp.route("/operation/<string:username>", methods=['GET','POST'])
def operation(username):
    return flask.render_template('operation.html',username=username)

# 获得用户基本信息
@bp.route("/<username>/info", methods=['GET'])
def user(username):
    money, capability, fortune = get_user_info(username)
    return jsonify({
        "username": username,
        "money": money,
        "capability": capability,
        "fortune": fortune
    })

# 用户工作路由
@bp.route("/<username>/work", methods=['GET']) #POST
def work_route(username):
    gain = work(username)
    return jsonify({'gain': gain})

@bp.route("/<username>/register/<password>", methods=['GET'])
def register_route(username,password):
    status = register(username,password)
    return jsonify({'status': status})

@bp.route("/<username>/login/<password>", methods=['GET'])
def login_route(username,password):
    status = login(username,password)
    return jsonify({'status': status})

@bp.route("/<username>/logout", methods=['GET'])
def logout_route(username):
    status = logout(username)
    return jsonify({'status': status})

@bp.route("/<username>/seek", methods=['GET']) #POST
def seek_route(username):
    treasure = seek(username)
    return jsonify(treasure)

@bp.route("/market", methods=['GET'])
def market_route():
    market = check_market()
    return jsonify({
        'market': market,
        'tips': 'the above price do not include tax, tax rate == 0.2'
    })

@bp.route("<username>/market", methods=['GET'])
def my_market_route(username):
    market = check_my_market(username)
    return jsonify({
        'market': market,
        'tips': 'the above price do not include tax, tax rate == 0.2'
    })

@bp.route("/<username>/treasures", methods=['GET'])
def check_my_treasure_route(username):
    treasures = check_my_treasure(username)
    return jsonify(treasures)

@bp.route("/<username>/wear/<treasurename>", methods=['GET'])
def wear_route(username,treasurename):
    status = wear(username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/unwear/<treasurename>", methods=['GET'])
def unwear_route(username,treasurename):
    status = unwear(username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/sell/<treasurename>/<int:price>", methods=['GET'])
def sell_route(username,treasurename,price):
    status = sell(username,treasurename,price)
    return jsonify({'status': status})

@bp.route("/<username>/callback/<treasurename>", methods=['GET'])
def callback_route(username,treasurename):
    status = callback(username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username1>/sold/<treasurename>/<username2>", methods=['GET'])
def sold_route(username1,username2,treasurename):
    status = sold(username1,username2,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/rename/<treasurename>/<newtreasurename>", methods=['GET'])
def rename_route(username,treasurename,newtreasurename):
    status = rename(username,treasurename,newtreasurename)
    return jsonify({'status': status})

@bp.route("/<username>/drop/<treasurename>", methods=['GET'])
def drop_route(username,treasurename):
    status = drop(username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/remove", methods=['GET'])
def remove_route(username):
    status = remove(username)
    return jsonify({'status': status})

@bp.route("/<username>/history/<int:number>", methods=['GET'])
def history_route(username, number):
    logs = history(username, number)
    return jsonify(logs)

@bp.route("/<username>/changepw/<oldpw>/<newpw>", methods=['GET'])
def changepw_route(username, oldpw, newpw):
    status = changepw(username, oldpw, newpw, newpw)
    return jsonify({'status': status})

@bp.route("/<username>/wear/", methods=['POST'])
def bak_wear_route(username):
    treasurename = request.form.get('treasurename')
    status = wear(username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/unwear/", methods=['POST'])
def bak_unwear_route(username):
    treasurename = request.form.get('treasurename')
    status = unwear(username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/drop/", methods=['POST'])
def bak_drop_route(username):
    treasurename = request.form.get('treasurename')
    status = drop(username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/rename", methods=['POST'])
def bak_rename_route(username):
    treasurename = request.form.get('treasurename')
    newtreasurename = request.form.get('newtreasurename')
    status = rename(username,treasurename,newtreasurename)
    return jsonify({'status': status})

@bp.route("/<username>/sell", methods=['POST'])
def bak_sell_route(username):
    treasurename = request.form.get('treasurename')
    pricestr = request.form.get('price')
    price = int(pricestr)
    status = sell(username,treasurename,price)
    return jsonify({'status': status})

@bp.route("/<username>/callback", methods=['POST'])
def bak_callback_route(username):
    treasurename = request.form.get('treasurename')
    status = callback(username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/buy", methods=['POST'])
def buy_route(username):
    treasurename = request.form.get('treasurename')
    sellername = request.form.get('sellername')
    status = sold(sellername,username,treasurename)
    return jsonify({'status': status})

@bp.route("/<username>/history", methods=['POST'])
def bak_history_route(username):
    numberstr = request.form.get('number')
    number = int(numberstr)
    ops = history(username,number)
    return jsonify(ops)

@bp.route("/<username>/changepw", methods=['POST'])
def bak_changepw_route(username):
    oldpw = request.form.get('oldpw')
    newpw = request.form.get('newpw')
    newpwagain = request.form.get('newpwagain')
    status = changepw(username,oldpw,newpw,newpwagain)
    return jsonify({'status': status})