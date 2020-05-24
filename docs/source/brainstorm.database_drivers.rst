brainstorm.database\_drivers package
====================================

A package for database drivers to be used by ``brainstorm.saver``

Any ``DriverNameDriver`` class in a ``'.py'`` file in the ``brainstorm/database_drivers`` directory will be included in the package.
Files starting with ``'_'`` will be ignored.
The package imports as a dictionary of ``{'driver_name': DriverNameDriver}``.

To use module:

>>> import brainstorm.database_drivers as db_drivers
>>> driver_class = db_drivers['driver_name']

The drivers should inplement the interface for the brainstorm.saver:

.. class:: DriverNameDriver(database_url)

	A driver for database with given url.
	The url should be of the form ``driver_name://host:port``

   .. method:: save_user(user):

      Save a user to the database.
      user must have 'user_id'

      :param user: the user
      :type user: dict

    
	.. method:: save_snapshot(snapshot)

		Save a snapshot to the database.
		snapshot must have 'datetime' and 'user_id'
        
      :param snapshot: the snapshot
      :type snapshot: dict

   .. method:: get_users()

   	Get all the users in the database.

   	:returns: users (with 'user_id' and 'username')
   	:rtype: list

   .. method:: get_user(user_id)
      
      Get user with specified user_id.

      :param user_id: user_id of requested user
      :type user_id: int
      :returns: the user
      :rtype: dict

   .. method:: get_snapshots(user_id)

   	Get all the snapshots of user with specified user_id
      
      :param user_id: the user_id
      :type user_id: int
      :returns: snapshots (with 'datetime' and 'snapshot_id')
      :rtype: list

   .. method:: get_snapshot(user_id, snapshot_id)

   	Get the snapshot with snapshot_id of user with user_id
      
      :param user_id: the user_id
      :type user_id: int
      :param snapshot_id: the snapshot_id
      :type snapshot_id: int
      :returns: snapshot (with 'snapshot_id', 'datetime' and 'available_results')
      :rtype: dict

   .. method:: get_result(user_id, snapshot_id, result_name)
      
      Get the requested result of the snapshot with snapshot_id of user with user_id
      
      :param user_id: the user_id
      :type user_id: int
      :param snapshot_id: the snapshot_id
      :type snapshot_id: int
      :param result_name: the desired result
      :type result_name: str
      :returns: the requested result (or None if the result isn't available)
      :rtype: dict


Submodules
----------

brainstorm.database\_drivers.mongodb\_driver module
---------------------------------------------------

Mongodb driver to save and read data from mongodb.


.. class:: MongodbDriver(database_url)

	A driver for database with given url.
	The url should be of the form ``mongodb://host:port``.

   .. method:: save_user(user):

      Save a user to the database.
      user must have 'user_id'

      :param user: the user
      :type user: dict

    
	.. method:: save_snapshot(snapshot)

		Save a snapshot to the database.
		snapshot must have 'datetime' and 'user_id'
        
      :param snapshot: the snapshot
      :type snapshot: dict

   .. method:: get_users()

   	Get all the users in the database.

   	:returns: users (with 'user_id' and 'username')
   	:rtype: list

   .. method:: get_user(user_id)
      
      Get user with specified user_id.

      :param user_id: user_id of requested user
      :type user_id: int
      :returns: the user
      :rtype: dict

   .. method:: get_snapshots(user_id)

   	Get all the snapshots of user with specified user_id
      
      :param user_id: the user_id
      :type user_id: int
      :returns: snapshots (with 'datetime' and 'snapshot_id')
      :rtype: list

   .. method:: get_snapshot(user_id, snapshot_id)

   	Get the snapshot with snapshot_id of user with user_id
      
      :param user_id: the user_id
      :type user_id: int
      :param snapshot_id: the snapshot_id
      :type snapshot_id: int
      :returns: snapshot (with 'snapshot_id', 'datetime' and 'available_results')
      :rtype: dict

   .. method:: get_result(user_id, snapshot_id, result_name)
      
      Get the requested result of the snapshot with snapshot_id of user with user_id
      
      :param user_id: the user_id
      :type user_id: int
      :param snapshot_id: the snapshot_id
      :type snapshot_id: int
      :param result_name: the desired result
      :type result_name: str
      :returns: the requested result (or None if the result isn't available)
      :rtype: dict
