#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import signal
import sys
sys.path.append('..')
import utils

mylog = utils.init_log()
channel, connection = utils.create_channel()


def fib(n):
    if n < 1:
        return []
    elif n == 1:
        return [1, ]
    elif n == 2:
        return [1, 1, ]
    else:
        result = [1, 1]
        while len(result) < n:
            result.append(result[-1] + result[-2])
        return result


def request(ch, method, properties, body):
    para = int(body)
    mylog.info('[x] Get request fib(%d)' % para)
    result = fib(para)
    mylog.info('[x] calc : %s' % str(result))
    channel.basic_publish(exchange='',
                          routing_key=properties.reply_to,
                          properties=pika.BasicProperties(
                              correlation_id=properties.correlation_id),
                          body=str(result))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    pass


def SignalHandler(signum, frame):
    connection.close()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, SignalHandler)
    channel.queue_declare(queue='rpc_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(request, queue='rpc_queue')
    mylog.info('[s] server start')
    channel.start_consuming()
