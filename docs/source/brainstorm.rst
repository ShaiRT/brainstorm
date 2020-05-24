brainstorm package
==================

This package includes a client, which streams cognition snapshots to a server, which then publishes them to a message queue, where multiple parsers read the snapshot, parse various parts of it, and publish the parsed results, which are then saved to a database.
The results are then exposed via a RESTful API, which is consumed by a CLI; there’s also a GUI, which visualizes the results in various ways.

See instructions for deployment with docker and CLI usage `here <https://brainstormproject.readthedocs.io/en/latest/README.html>`_

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   brainstorm.api
   brainstorm.cli
   brainstorm.client
   brainstorm.database_drivers
   brainstorm.gui
   brainstorm.mq_drivers
   brainstorm.parsers
   brainstorm.saver
   brainstorm.server
