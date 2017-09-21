#! /usr/bin/venv python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import utils

log_levels = [
    'debug',
    'info',
    'error'
]


if __name__ == '__main__':
    mylog = utils.init_log()
    channel, connection = utils.create_channel()

    # 创建一个直连的交换机作为新日志系统交换机
    channel.exchange_declare('logs_direct', 'direct')

    message = ' '.join(sys.argv[1:]) or 'info: Hello World'
    mes_map = message.split(':')
    log_level = mes_map[0].strip()

    if log_level in log_levels:
        channel.basic_publish(exchange='logs_direct',
                              routing_key=log_level,
                              body=message)
        mylog.info(" [x] Sent Log : %s" % message)
    else:
        mylog.info("error log mes: %s" % message)

    connection.close()
