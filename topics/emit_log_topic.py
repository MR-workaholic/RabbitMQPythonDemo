#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import utils

#
# 路由键是这样的：<facility>.<severity>
#

facility_list = [
    'server_one',
    'server_two',
    'mq_one',
    'mq_two',
]

severity_list = [
    'debug',
    'info',
    'error'
]

if __name__ == '__main__':
    mylog = utils.init_log()
    channel, connection = utils.create_channel()

    # 创建一个主题交换机
    channel.exchange_declare('logs_topic', 'topic')

    message = ' '.join(sys.argv[1:]) or 'anonymous.info : hello world'
    facility = message.split('.')[0].strip()

    if facility in facility_list:
        severity = message.split('.')[1].split(':')[0].strip()
        if severity in severity_list:
            channel.basic_publish(exchange='logs_topic',
                                  routing_key='.'.join([facility, severity]),
                                  body=message)
            mylog.info(" [x] routing key : %s " %
                       '.'.join([facility, severity]))

    connection.close()
