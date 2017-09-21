#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import sys
sys.path.append('..')
import utils


mylog = utils.init_log()


def recv_info(ch, method, properties, body):
    try:
        fobj = open('./text.txt', 'a')
        fobj.writelines("Log: %r" % (body,))
        fobj.close()
    except IOError, e:
        mylog.error("file open error: %s", e)


if __name__ == '__main__':
    channel, connection = utils.create_channel()

    channel.exchange_declare('logs', 'fanout')

    # 声明一个随机的队列result，当消费者断开的时候，队列会被删除
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    # 将这个随机的队列result与扇形交换机进行绑定即可接收扇形交换机发布的内容
    channel.queue_bind(exchange='logs', queue=queue_name)

    mylog.info(" [*] Waiting for log message. To exit press C-C")

    channel.basic_consume(recv_info, queue=queue_name, no_ack=True)

    channel.start_consuming()
