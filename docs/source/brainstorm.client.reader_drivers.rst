brainstorm.client.reader\_drivers package
=========================================

A package for drivers to be used by ``brainstorm.client.reader``

Any ``DriverNameDriver`` class in a ``'.py'`` file in the ``'.py'`` file in the ``brainstorm/client/reader_drivers`` directory will be included in the package.
Files starting with ``'_'`` will be ignored.
The package imports as a dictionary of ``{'driver_name': DriverNameDriver}``.
To use package:

>>> import brainstorm.client.reader_drivers as reader_drivers
>>> driver_class = reader_drivers['driver_name']

The drivers should inplement the interface for the brainstorm.client.reader:

.. class:: DriverNameDriver(path)
    
    A driver to convert sample formats.
    A sample contains a user and then some snapshots of that user in some format.

   .. method:: get_user()
   
      :returns: user of the sample
      :rtype: dict
   
   .. method:: get_snapshot()
        
        get the next snapshot from the sample
        can assume ``self.get_user`` has been called previously

        :returns: the snapshot as a dictionary
        :rtype: dict


Submodules
**********

brainstorm.client.reader\_drivers.binary\_driver module
-------------------------------------------------------

.. class:: BinaryDriver(path)

   A driver that converts a sample in given path from a protobuf format to a dictionary format.
   The path must be to a ``'.mind'`` or ``'.mind.gz'`` file, and the file must contain a sample in the following format:
   The sample must be a binary (possibly gzipped), with a user information and then a list of snapshots.

   .. warning:: 

      Any other formats given to this driver will cause undefined behavior.


   .. method:: get_user()

      :returns: user of the sample
      :rtype: dict

    
   .. method:: get_snapshot()

      get the next snapshot from the sample
      assumes ``self.get_user`` has been called previously

      :returns: the snapshot as a dictionary
      :rtype: dict


brainstorm.client.reader\_drivers.protobuf\_driver module
---------------------------------------------------------

.. class:: ProtobufDriver(path)

   A driver that converts a sample in given path from a binary format to a dictionary format.
   The path must be to a ``'.mind'`` or ``'.mind.gz'`` file, and the file must contain a sample in the following format:
   The sample must be a binary (possibly gzipped), with a sequence of message sizes (uint32) and messages (of that size), where the first one is a User message, and the rest are Snapshot messages, as defined in 'sample.proto'.

   .. warning:: 

      Any other formats given to this driver will cause undefined behavior.


   .. method:: get_user()

      :returns: user of the sample
      :rtype: dict

    
   .. method:: get_snapshot()

      get the next snapshot from the sample
      assumes ``self.get_user`` has been called previously

      :returns: the snapshot as a dictionary
      :rtype: dict