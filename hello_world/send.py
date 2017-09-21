#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pika

'''
   mes    hello
p------> ||||||||
'''

if __name__ == '__main__':
    # 连接服务器
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # 创建（已经创建的话会自动忽略）名字为hello的接收端队列，需要有队列去接收发送出来的信息
    channel.queue_declare(queue='hello')
    # 发送信息到路由键为‘hello’的队列
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World')
    print " [x] Sent 'Hello World'"
    connection.close()
