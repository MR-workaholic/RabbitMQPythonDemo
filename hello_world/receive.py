#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pika

'''
 hello     mes
||||||||--------->C
'''


def recv_mes(ch, method, properties, body):
    print "[x] Received %r" % body


if __name__ == '__main__':
    # 连接服务器
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # 声明是否存在该队列
    channel.queue_declare(queue='hello')
    # 消费信息
    channel.basic_consume(recv_mes, queue='hello', no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    pass
