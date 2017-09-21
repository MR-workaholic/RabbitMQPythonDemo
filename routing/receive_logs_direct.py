#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import utils

myLog = utils.init_log()
log_levels = [
    'debug',
    'info',
    'error'
]


def recv_info(ch, method, properties, body):
    myLog.info(body)


if __name__ == '__main__':
    channel, connection = utils.create_channel()

    channel.exchange_declare('logs_direct', 'direct')
    # 声明一个随机的队列result，当消费者断开的时候，队列会被删除
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    for log_level in log_levels:
        channel.queue_bind(exchange='logs_direct',
                           queue=queue_name,
                           routing_key=log_level)

    myLog.info(" [*] Waiting for log message. To exit press C-C")

    channel.basic_consume(recv_info, queue=queue_name, no_ack=True)
    channel.start_consuming()
