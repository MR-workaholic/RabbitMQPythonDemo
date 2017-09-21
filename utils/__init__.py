import logging
import pika


def init_log():
    mylog = logging.getLogger()
    # mylog.propagate = 0
    mylog.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    mylog.addHandler(console_handler)
    return mylog


def delete_queue(queue_name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_delete(queue=queue_name)
    connection.close()


def create_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    return (connection.channel(), connection)
