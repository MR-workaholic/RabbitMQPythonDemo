#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import utils

myLog = utils.init_log()


def recv_info(ch, method, properties, body):
    myLog.info(body)


if __name__ == '__main__':
    channel, connection = utils.create_channel()

    channel.exchange_declare('logs_topic', 'topic')
    # 声明一个随机的队列result，当消费者断开的时候，队列会被删除
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    # 绑定键从用户输入
    routing_keys = sys.argv[1:] if len(sys.argv) > 1 else ['anonymous.info', ]
    for item in routing_keys:
        myLog.info(item)
        channel.queue_bind(exchange='logs_topic',
                           queue=queue_name,
                           routing_key=item)

    myLog.info(" [*] Waiting for log message. To exit press C-C")

    channel.basic_consume(recv_info, queue=queue_name, no_ack=True)
    channel.start_consuming()
