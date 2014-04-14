# -*- coding: utf-8 -*-
'''
Return data to logstash

:maintainer:    none
:maturity:      New
:depends:       none
:platform:      all

To enable this returner the minion will need the zmq installed and
the following values configured in the minion or master config::

    returner.logstash.address: tcp://127.0.0.1:2021
    returner.logstash.version: 0

    ZeroMQ Logging Handler
    ----------------------

    For versions of `Logstash`_ before 1.2.0:
    In the `Logstash`_ configuration file:
    .. code-block:: text

        input {
          zeromq {
            type => "zeromq-type"
            mode => "server"
            topology => "pubsub"
            address => "tcp://0.0.0.0:2021"
            charset => "UTF-8"
            format => "json_event"
          }
        }

    For version 1.2.0 of `Logstash`_ and newer:
    In the `Logstash`_ configuration file:
    .. code-block:: text

        input {
          zeromq {
            topology => "pubsub"
            address => "tcp://0.0.0.0:2021"
            codec => json
          }
        }


Required python modules: zmq

  To use the postgres returner, append '--return logstash' to the salt command. ex:

    salt '*' test.ping --return logstash
'''

# Import python libs
import json
import zmq

import random
import sys
import time


# Define the module's virtual name
__virtualname__ = 'logstash'


def __virtual__():
    return __virtualname__


def returner(ret):
    '''
    Return data to logstash
    '''
    def connect_to_zmq():
        host = port = address = None

        if 'returner' in __opts__ and 'logstash' in __opts__['returner']:
            address = __opts__['returner']['logstash'].get('address', None)
            zmq_hwm = __opts__['returner']['logstash'].get('hwm', 1000)
            version = __opts__['returner']['logstash'].get('version', 0)

            if address is None:
                log.debug(
                    'The required \'logstash_zmq_handler\' configuration key, '
                    '\'address\', is not properly configured. Not '
                    'configuring the logstash ZMQ logging handler.'
                )
            else:
                context = zmq.Context()
                socket = context.socket(zmq.PUB)
                socket.bind(address)
                yield socket
        else:
            return false

    socket = connect_to_zmq()
    socket.send("%d %d" % (ret['fun'], ret['jid']) )
    '''
            json.dumps(ret['return']),
            ret['id'],
            ret['success']
    '''
