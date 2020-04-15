import pymongo


class MongodbDriver:

    def __init__(self, database_url):
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
        query = {'user_id': user['user_id']}
        update = {'$set': user, '$setOnInsert': {'snapshots_count': 0}}
        self.users.update_one(query, update, upsert=True)

    def save_snapshot(self, snapshot):
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
        projection = {'_id': False, 'user_id': True, 'username': True}
        return list(self.users.find(projection=projection))

    def get_user(self, user_id):
        query = {'user_id': user_id}
        projection = {'_id': False, 'snapshots_count': False}
        return self.users.find_one(filter=query, projection=projection)

    def get_user_snapshots(self, user_id):
        query = {'user_id': user_id}
        projection = {'_id': False, 'snapshot_id': True, 'datetime': True}
        return list(self.snapshots.find(filter=query, projection=projection))

    def get_snapshot(self, user_id, snapshot_id):
        query = {'user_id': user_id, 'snapshot_id': snapshot_id}
        projection = {'_id': False}
        snapshot = self.snapshots.find_one(filter=query, projection=projection)
        if snapshot is None:
            return None
        ret = dict()
        ret['snapshot_id'] = snapshot['snapshot_id']
        ret['datetime'] = snapshot['datetime']
        ret['available_results'] = set(snapshot.keys())
        ret['available_results'] -= {'snapshot_id', 'datetime', 'user_id'}
        ret['available_results'] = list(ret['available_results'])
        if not ret['available_results']:
            ret['available_results'] = None
        return ret

    def get_snapshot_result(self, user_id, snapshot_id, result_name):
        query = {'user_id': user_id, 'snapshot_id': snapshot_id}
        projection = {'_id': False, result_name: True}
        result = self.snapshots.find_one(filter=query, projection=projection)
        if not result:
            return None
        return result[result_name]
