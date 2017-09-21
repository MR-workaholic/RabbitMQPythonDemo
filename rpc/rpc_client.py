#! /usr/bin/env python
# -*- coding: utf-8 -*-
import signal
import pika
import sys
import uuid
sys.path.append('..')
import utils

mylog = utils.init_log()
channel, connection = utils.create_channel()


class FibonacciRpcClient():
    def __init__(self):
        self.queue_recall = channel.queue_declare(exclusive=True)
        self.queue_recall_name = self.queue_recall.method.queue
        # 不需要绑定交换机，因为是使用默认直连交换机
        channel.basic_consume(
            self.request, queue=self.queue_recall_name, no_ack=True)

    def request(self, ch, method, prop, body):
        if self.uuid == prop.correlation_id:
            self.response = [int(ele) for ele in body.strip('[]').split(', ')]

    def call(self, para):
        self.response = None
        self.uuid = str(uuid.uuid4())
        channel.queue_declare(queue='rpc_queue')
        channel.basic_publish(exchange='',
                              routing_key='rpc_queue',
                              properties=pika.BasicProperties(
                                  reply_to=self.queue_recall_name,
                                  correlation_id=self.uuid),
                              body=str(para))
        # RPC同步阻塞调用
        while self.response is None:
            connection.process_data_events()

        return self.response
        pass


def SignalHandler(signum, frame):
    connection.close()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, SignalHandler)
    fibonacci_rpc = FibonacciRpcClient()

    print " [x] Requesting fib(30)"
    response = fibonacci_rpc.call(30)
    print " [.] Got %r" % (response,)
