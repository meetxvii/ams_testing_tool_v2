import pymongo 
from datetime import datetime
import constants


class Model:
    def __init__(self) -> None:
        
        self.client = pymongo.MongoClient(constants.DATABASE_URL)
        try:
            database_names = self.client.list_database_names()
            self.connected = True
        except :
            self.connected = False
        
        if self.connected and constants.DATABASE_NAME  in database_names:
            self.database_present = True
            self.db = self.client[constants.DATABASE_NAME]
        else:
            self.database_present = False

    def get_unique_sites(self):
        if not self.connected or not self.database_present:
            return []
        return self.db["mobile_usages"].distinct("site_name")

    def get_floors(self, site):
        if not self.connected or not self.database_present:
            return []
        return (
            self.db["mobile_usages"]
            .find({"site_name": site})
            .distinct("workspace_name")
        )

    def get_mobile_usages(self, site, floor, start_time, end_time):
        
        pipeline = [
            {
                "$match": {
                    "site_name": site,
                    "workspace_name": floor,
                    "start_time": {
                        "$gte": datetime.fromisoformat(start_time),
                        "$lte": datetime.fromisoformat(end_time),
                    },
                    "validated_by": {"$exists": False},
                }
            },
            {
                # Group by image and get all document in the group
                "$group": {"_id": "$image", "documents": {"$push": "$$ROOT"}}
            },
            {"$sort": {"documents.start_time": 1}},
        ]
        return self.db["mobile_usages"].aggregate(pipeline)

    def get_occupancy_data(self, site, floor, start_time, end_time):
        

        pipeline = [
            {
                "$match": {
                    "site_name": site,
                    "workspace_name": floor,
                    "event_time": {
                        "$gte": datetime.fromisoformat(start_time),
                        "$lte": datetime.fromisoformat(end_time),
                    },
                    "validated_by": {"$exists": False},
                }
            },
            {
                # Group by image and get all document in the group
                "$group": {"_id": "$image", "documents": {"$push": "$$ROOT"}}
            },
            {"$sort": {"documents.start_time": 1}},
        ]
        return self.db["occupancy"].aggregate(pipeline)

    def occupancy_classification_update_date(self, _id, status,name):
        self.db["occupancy"].update_one({"_id": _id}, {"$set": {"validated_by": name,"is_occupancy_correct":status}})

    def update_mobile_data(self,correct_bboxes,wrong_bboxes):
        collection = self.db['mobile_usages']
        
        correct_result = collection.update_many({"_id":{"$in":correct_bboxes}},
                                                {"$set":{"is_correct":True, "validated_by":constants.VALIDATOR_NAME}})
    
        wrong_result = collection.update_many({"_id":{"$in":wrong_bboxes}},
                                                {"$set":{"is_correct":False, "validated_by":constants.VALIDATOR_NAME}})

        return correct_result.modified_count and wrong_result.modified_count

    def store_new_bboxes(self,document):
        collection = self.db['corrected_mobiles']
        document['validated_by'] = constants.VALIDATOR_NAME
        return collection.insert_one(document).acknowledged