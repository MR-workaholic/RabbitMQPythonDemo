#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import sys
sys.path.append("..")
from utils import init_log, create_channel

if __name__ == '__main__':
    mylog = init_log()
    channel, connection = create_channel()

    # 这次不使用默认的直连交换机而是扇形交换机
    # channel.exchange_declare(exchange='logs', type='fanout')
    channel.exchange_declare('logs', 'fanout')

    message = ' '.join(sys.argv[1:]) or 'INFO : Hello World'

    channel.basic_publish(exchange='logs', routing_key='', body=message)
    mylog.info(" [x] Sent Log : %r" % (message, ))

    connection.close()
