brainstorm.mq\_drivers package
==============================

A package for message queue drivers.

Any ``Publisher`` or ``Subscriber`` class in a ``'driver_name_driver.py'`` file in the ``brainstorm/mq_drivers`` directory will be included in the package.
Files starting with ``'_'`` will be ignored.
The package imports as a dictionary of ``{'driver_name': {'publisher': Publiser, 'subscriber': Subscriber}}``.

To use module:

>>> import brainstorm.mq_drivers as mq_drivers
>>> driver_class = mq_drivers['driver_name']

The drivers should inplement the following interface:

.. class:: Publisher(url, exchange, exchange_type='fanout', routing_key='')

   :param url: message queue url of the form ``'driver_name://host:port'``
   :type url: str
   :param exchange: exchange name to publish to
   :type exchange: str
   :param exchange_type: exchange type (default: {'fanout'})
   :type exchange_type: str
   :param routing_key: routing key to use for messages (default: {''})
   :type routing_key: str

   .. method:: publish(message)
        
      publish message to the message queue in ``self.exchange`` with ``self.routing_key``

      :param message: the message to be published
      :type message: str


.. class:: Subscriber(url, exchange, exchange_type='fanout'):
        
   :param url: message queue url
   :type url: str
   :param exchange: exchange name to subscribe to
   :type exchange: str
   :param exchange_type: exchange type (default: {'fanout'})
   :type exchange_type: str

   .. method subscribe(queue, callback, *, routing_key='#', just_one=False):
        
      Consume messages from given queue in ``self.exchange`` with given routing key. use callback to handle the messages.
      This function doesn't return (consumes forever).

      :param queue: name of queue to consume
      :type queue: str
      :param callback: callback to handle messages
      :type callback: function
      :param routing_key: routing key to filter messages (default: {'#'})
      :type routing_key: str


Submodules
**********

brainstorm.mq\_drivers.rabbitmq\_driver module
----------------------------------------------


Rabbitmq message queue driver with Publisher and Subscriber


.. class:: Publisher(url, exchange, exchange_type='fanout', routing_key='')

   :param url: message queue url of the form ``'rabbitmq://host:port'``
   :type url: str
   :param exchange: exchange name to publish to
   :type exchange: str
   :param exchange_type: exchange type (default: {'fanout'})
   :type exchange_type: str
   :param routing_key: routing key to use for messages (default: {''})
   :type routing_key: str

   .. method:: publish(message)
        
      publish message to the message queue in ``self.exchange`` with ``self.routing_key``

      :param message: the message to be published
      :type message: str


.. class:: Subscriber(url, exchange, exchange_type='fanout'):
        
   :param url: message queue url
   :type url: str
   :param exchange: exchange name to subscribe to
   :type exchange: str
   :param exchange_type: exchange type (default: {'fanout'})
   :type exchange_type: str

   .. method subscribe(queue, callback, *, routing_key='#', just_one=False):
        
      Consume messages from given queue in ``self.exchange`` with given routing key. use callback to handle the messages.
      This function doesn't return (consumes forever), unless ``just_one == True``, in which case only one message is consumed.

      :param queue: name of queue to consume
      :type queue: str
      :param callback: callback to handle messages
      :type callback: function
      :param routing_key: routing key to filter messages (default: {'#'})
      :type routing_key: str
      :param just_one: consume only one message (default: {False})
      :type just_one: bool
