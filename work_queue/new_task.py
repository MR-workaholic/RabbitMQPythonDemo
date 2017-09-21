#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import sys
sys.path.append("..")
import utils

if __name__ == '__main__':
    # 连接服务器
    mylog = utils.init_log()
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='work_queue', durable=True)
    message = ' '.join(sys.argv[1:]) or "Hello World!"

    channel.basic_publish(exchange='',  # 使用默认的空字串交换机
                          routing_key='work_queue',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    mylog.info(" [x] Sent %r" % (message,))
    connection.close()
