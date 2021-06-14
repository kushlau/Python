#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'ORM module'

__author__ = 'Wuruyue'

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time,aiomysql
from datetime import datetime

from aiohttp import web

＃用传入的字典来创建连接池
async def create_pool(loop, **kw):
	logging.info('create database connection pool...')
	＃用全局变量就省去了返回值
	global __pool
	＃kw.get方法可以保证给个默认值
	__pool = await aiomysql.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 3306),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset', 'utf8'),
        autocommit = kw.get('autocommit', True),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
        loop = loop
    )

＃用传入的SQL语句和参数去执行select函数达到执行SELECT语句的目的
async def select(sql, args, size = None):
	log(sql, args)
	global __pool
	with (await __pool) as conn:
		cur = await conn.cursor(aiomysql.DictCursor)
		await cur.execute(sql.replace('?', '%s'), args or ())
		if size:
			rs = await cur.fetchmany(size)
		else:
			rs = await cur.fetchall()
		await cur.close()
		logging.info('rows returned: %s' % len(rs))
		return rs
