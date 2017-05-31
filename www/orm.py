#!usr/bin/env python3
#-*- conding: uft-8 -*-

import asyncio,logging
import aiomysql

def log(sql,args=()):
    logging.info('SQL:%s' %sql)

#创建连接池，每个http请求都从连接池链接到数据库
async def create_pool(loop,**kw):
    logging.info('creat database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host','localhost'),
        port=kw.get('port',3306),
        user=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf-8'),
        autocommit=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10)
        minsize=kw.get('minsize',1)
        loop=loop
    )

#销毁连接池
async def destory_pool():
    global __pool
    if __pool is not None:
        __pool.close()
        await __pool.wait_closed()

#select语言
async def select(sql,args,size=Nome):
    log(sql,args)
    global __pool
    aysnc with __pool.get() as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?','%s'),args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('rows returned %s' %len(rs))
        return rs

#insert,update,delete语句
async def execute(sql,args，autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?','%s'),args)
                affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

    def create_args_string(num):
        l = []
        for n in range(num)
            l.append('?')
        return ', '.join(l)

#定义Field类，负责保存（数据库）表的字段名和字段类型
class Field(object):
    def __init__(self,name,colunm_type,primary_key,default):
        self.name = name
        self.colunm_type = colunm_type
        self.primary_key = primary_key
        self.default = default
    def __str__(self):
        return '<%s,%s,%s>' %(self.__class__.__name__,self.colunm_type,self.name)

class StringField(Field):
    def __init__(self,name=Nome,primary_key=False,default=Nome,ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)
