#!/usr/bin/env python3
from flask.testing import FlaskClient
import time
import pytest

username = 'test'
treasurename = 'treatest'
username2 = 'test2'
username3 = 'test3'
treasurename2 = 'treatest2'
treasurename3 = 'treatest3'
price = '5'
newprice = '50'
bigprice = '100000000'
password = 'password'
newpasswd = 'newpasswd'

def test_register(client: FlaskClient):
    response = client.get("/%s/register/%s" % (username, password))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l - 1] == 'success'

    response = client.get("/%s/register/%s" % (username2, password))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

    response = client.get("/%s/register/%s" % (username2, password))
    json = response.get_json()
    print(json)
    assert json['status'] == 'Register failed'

def test_login(client):
    response = client.get("/%s/login/%s" % (username, password))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l - 1] == 'success'

    response = client.get("/%s/login/%s" % (username2, 'pass'))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/login/%s" % (username2, password))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

def test_market(client: FlaskClient):
    response = client.get("/market")
    json = response.get_json()
    print(json)

def test_info(client: FlaskClient):
    response = client.get("/%s/info" % (username))
    json = response.get_json()
    print(json)

def test_seek_and_rename(client: FlaskClient):
    response = client.get("/%s/seek" % (username))
    json = response.get_json()
    print(json)
    tname = json['tname']
    type = json['type']

    response = client.get("/%s/rename/%s/%s" % (username, tname, treasurename))
    jsons = response.get_json()
    print(jsons)
    assert jsons['status'] == 'Rename success'

    while (type == json['type']):
        time.sleep(10)
        response = client.get("/%s/seek" % (username))
        json = response.get_json()

    tname = json['tname']
    response = client.get("/%s/rename/%s/%s" % (username, tname, treasurename2))
    jsons = response.get_json()
    print(jsons)
    assert jsons['status'] == 'Rename success'

def test_work(client: FlaskClient):
    response = client.get("/%s/work" % (username2))
    json = response.get_json()
    print(json)
    assert json['gain'] >= 0

    response = client.get("/%s/work" % (username))
    json = response.get_json()
    print(json)
    assert json['gain'] == 'try again 10 secs later'

    response = client.get("/%s/seek" % (username2))
    json = response.get_json()
    print(json)
    assert json == 'try again 10 secs later'

def test_treasures(client: FlaskClient):
    response = client.get("/%s/treasures" % (username))
    json = response.get_json()
    print(json)

def test_more_treasures(client: FlaskClient):
    response = client.get("/%s/treasures/more" % (username))
    json = response.get_json()
    print(json)

def test_wrong_1(client: FlaskClient):
    response = client.get("/%s/work" % (username3))
    json = response.get_json()
    print(json)
    tlist = json["gain"].split(' ')
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/seek" % (username3))
    json = response.get_json()
    print(json)
    tlist = json.split(' ')
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/market" % (username3))
    json = response.get_json()
    print(json)
    tlist = json['market'].split(' ')
    assert tlist[0] == 'ERROR'

def test_wear(client: FlaskClient):
    response = client.get("/%s/wear/%s" % (username, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

    response = client.get("/%s/wear/%s" % (username, treasurename2))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

def test_wrong_2(client: FlaskClient):
    response = client.get("/%s/wear/%s" % (username, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'Treasure'

    response = client.get("/%s/sell/%s/%s" % (username, treasurename, price))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'Treasure'

def test_unwear(client: FlaskClient):
    response = client.get("/%s/unwear/%s" % (username, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

def test_sell(client: FlaskClient):
    response = client.get("/%s/sell/%s/%s" % (username, treasurename, price))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

    response = client.get("/%s/sell/%s/%s" % (username, treasurename, newprice))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

def test_my_market(client: FlaskClient):
    response = client.get("/%s/market" % (username2))
    json = response.get_json()
    print(json)

def test_wrong_3(client: FlaskClient):
    response = client.get("/%s/wear/%s" % (username, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'Treasure'

    response = client.get("/%s/unwear/%s" % (username, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'U'

    response = client.get("/%s/wear/%s" % (username, treasurename3))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/sell/%s/%s" % (username, treasurename3, price))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/rename/%s/%s" % (username, treasurename2, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'Change'

    response = client.get("/%s/rename/%s/%s" % (username, treasurename3, treasurename3))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/drop/%s" % (username, treasurename3))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/remove" % (username3))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'ERROR'

def test_callback(client: FlaskClient):
    response = client.get("/%s/callback/%s" % (username, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

def test_buy(client: FlaskClient):
    response = client.get("/%s/sell/%s/%s" % (username, treasurename, price))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l - 1] == 'success'

    response = client.get("/%s/sold/%s/%s" % (username, treasurename, username))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/sold/%s/%s" % (username, treasurename, username2))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'success'

    response = client.get("/%s/sell/%s/%s" % (username2, treasurename, bigprice))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l - 1] == 'success'

    response = client.get("/%s/sold/%s/%s" % (username2, treasurename, username))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l-1] == 'B'

    response = client.get("/%s/callback/%s" % (username2, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l - 1] == 'success'

def test_drop(client: FlaskClient):
    response = client.get("/%s/drop/%s" % (username2, treasurename))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l - 1] == 'success'

def test_history(client: FlaskClient):
    response = client.get("/%s/history" % (username))
    json = response.get_json()
    print(json)

def test_changepw(client):
    response = client.get("/%s/changepw/%s/%s" % (username, newpasswd, newpasswd))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/changepw/%s/%s" % (username3, password, newpasswd))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[0] == 'ERROR'

    response = client.get("/%s/changepw/%s/%s" % (username, password, newpasswd))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l -1] == 'success'

def test_logout(client):
    response = client.get("/%s/logout" % (username))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l - 1] == 'success'

    response = client.get("/%s/login/%s" % (username,newpasswd))
    json = response.get_json()
    print(json)
    tlist = json["status"].split(' ')
    l = len(tlist)
    assert tlist[l - 1] == 'success'


def test_remove(client: FlaskClient):
    response = client.get("/%s/remove" % (username))
    json = response.get_json()
    print(json)
    assert json["status"] == 'BYE'

    response = client.get("/%s/remove" % (username2))
    json = response.get_json()
    print(json)
    assert json["status"] == 'BYE'