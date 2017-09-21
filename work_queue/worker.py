#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import time
import sys
sys.path.append("..")
import utils
mylog = utils.init_log()


def recv_mes_no_ack(ch, method, properties, body):
    print '[x] Received %r' % body
    time.sleep(body.count('.'))
    print '[x] sleep %d seconds' % body.count('.')


def recv_mes_ack(ch, method, properties, body):
    mylog.info('[x] Received %r' % body)
    time.sleep(body.count('.'))
    mylog.info('[x] sleep %d seconds' % body.count('.'))
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='work_queue', durable=True)
    channel.basic_qos(prefetch_count=1)  # 使其公平调度信息

    # channel.basic_consume(recv_mes_no_ack, queue='work_queue', no_ack=True)
    channel.basic_consume(recv_mes_ack, queue='work_queue')
    mylog.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
