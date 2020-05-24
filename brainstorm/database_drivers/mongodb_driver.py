"""Mongodb driver to save and read data from mongodb
"""
import pymongo


class MongodbDriver:

    def __init__(self, database_url):
        """
        Args:
            database_url (str): url of the database
        """
        self.client = pymongo.MongoClient(database_url)
        self.db = self.client.brainstorm
        self.users = self.db.users
        self.snapshots = self.db.snapshots
        self.users.create_index([('user_id', pymongo.ASCENDING)],
                                unique=True)
        index1 = pymongo.IndexModel([('user_id', pymongo.ASCENDING),
                                     ('datetime', pymongo.ASCENDING)])
        index2 = pymongo.IndexModel([('user_id', pymongo.ASCENDING),
                                     ('snapshot_id', pymongo.ASCENDING)],
                                    unique=True)
        self.snapshots.create_indexes([index1, index2])

    def save_user(self, user):
        """Save a user to the database
        user must have 'user_id'
        
        Args:
            user (dict): the user
        """
        query = {'user_id': user['user_id']}
        update = {'$set': user, '$setOnInsert': {'snapshots_count': 0}}
        self.users.update_one(query, update, upsert=True)

    def save_snapshot(self, snapshot):
        """Save a snapshot to the database.
        snapshot must have 'datetime' and 'user_id'
        
        Args:
            snapshot (dict): the snapshot
        """
        query = {'user_id': snapshot['user_id'],
                 'datetime': snapshot['datetime']}
        update = {'$set': snapshot}
        result = self.snapshots.update_one(query, update, upsert=True)
        if result.upserted_id is not None:
            user = self.users.find_one_and_update({'user_id': snapshot['user_id']},
                                                  {'$inc': {'snapshots_count': 1}},
                                                  return_document=pymongo.ReturnDocument.AFTER)
            update = {'$set': {'snapshot_id': user['snapshots_count']}}
            self.snapshots.update_one(query, update)

    def get_users(self):
        """Get all the users in the database
        
        Returns:
            list: users (with 'user_id' and 'username')
        """
        projection = {'_id': False, 'user_id': True, 'username': True}
        return list(self.users.find(projection=projection))

    def get_user(self, user_id):
        """Get user with specified user_id
        
        Args:
            user_id (int): user_id of requested user
        
        Returns:
            dict: the user
        """
        query = {'user_id': user_id}
        projection = {'_id': False, 'snapshots_count': False}
        return self.users.find_one(filter=query, projection=projection)

    def get_snapshots(self, user_id):
        """Get all the snapshots of user with specified user_id
        
        Args:
            user_id (int): the user_id
        
        Returns:
            list: snapshots (with 'datetime' and 'snapshot_id')
        """
        query = {'user_id': user_id}
        projection = {'_id': False, 'snapshot_id': True, 'datetime': True}
        return list(self.snapshots.find(filter=query, projection=projection))

    def get_snapshot(self, user_id, snapshot_id):
        """Get the snapshot with snapshot_id of user with user_id
        
        Args:
            user_id (int): the user_id
            snapshot_id (int): the snapshot_id
        
        Returns:
            dict: snapshot (with 'snapshot_id', 'datetime' and 'available_results')
        """
        query = {'user_id': user_id, 'snapshot_id': snapshot_id}
        projection = {'_id': False}
        snapshot = self.snapshots.find_one(filter=query, projection=projection)
        if snapshot is None:
            return None
        ret = dict()
        ret['snapshot_id'] = snapshot['snapshot_id']
        ret['datetime'] = snapshot['datetime']
        ret['available_results'] = [key for key, val in snapshot.items() 
                                    if val and key not in {'snapshot_id', 'datetime', 'user_id'}]
        if not ret['available_results']:
            ret['available_results'] = None
        return ret

    def get_result(self, user_id, snapshot_id, result_name):
        """Get the requested result of the snapshot with snapshot_id of user with user_id
        
        Args:
            user_id (int): the user_id
            snapshot_id (int): the snapshot_id
            result_name (str): the desired result
        
        Returns:
            dict: the requested result (or None if the result isn't available)
        """
        query = {'user_id': user_id, 'snapshot_id': snapshot_id}
        projection = {'_id': False, result_name: True}
        result = self.snapshots.find_one(filter=query, projection=projection)
        if not result:
            return None
        return result[result_name]
