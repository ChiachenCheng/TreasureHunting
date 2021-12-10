from sqlalchemy import Column,String,create_engine,Table,MetaData
from sqlalchemy.types import CHAR,Integer,String,Text,REAL,TIMESTAMP,Boolean,NUMERIC
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()
engine = create_engine('postgresql://postgres:40960032@127.0.0.1:5432/postgres',echo=True)
connect = engine.connect()

Player = Table(
    'players', metadata,
    Column('pname',String(64),primary_key=True),
    Column('passwd',String(64)),
    Column('money',Integer),
    Column('capability',REAL),
    Column('fortune',REAL),
    Column('lasttime',NUMERIC),
    Column('login',Boolean),
)

Treasure = Table(
    'treasures', metadata,
    Column('tname',String(64),primary_key=True),
    Column('type',String(10)),
    Column('value',REAL),
    Column('owner',String(64),primary_key=True),
    Column('wearing',Boolean),
    Column('price',Integer,nullable=True)
)

Log = Table(
    'logs', metadata,
    Column('ops',String(10)),
    Column('time',NUMERIC,primary_key=True),
    Column('pname',String(64)),
    Column('tname',String(64)),
    Column('overflow',Boolean),
)

Log_overflow = Table(
    'logs_overflow', metadata,
    Column('time',NUMERIC,primary_key=True),
    Column('attr',String(64),primary_key=True),
    Column('value',String(64))
)

Market = Table(
    'market', metadata,
    Column('tname',String(64),primary_key=True),
    Column('type',String(10)),
    Column('value',REAL),
    Column('owner',String(64),primary_key=True),
    Column('wearing',Boolean),
    Column('price',Integer,nullable=True)
)