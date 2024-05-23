from pymongo import MongoClient
from datetime import datetime

class Model:
    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['people-occupancy']
    
    def get_unique_sites(self):
        return self.db['mobile_usages'].distinct('site_name')
    
    def get_floors(self,site):
        return self.db['mobile_usages'].find({'site_name':site}).distinct('workspace_name')
    
    def get_mobile_usages(self,site,floor,start_time,end_time):
        pipeline = [
            {
                "$match": {
                    "site_name": site,
                    "workspace_name": floor,
                    "start_time": {
                        "$gte": datetime.fromisoformat(start_time),
                        "$lte": datetime.fromisoformat(end_time)
                    }
                }
            },
            {
                # Group by image and get all document in the group 
                "$group": {
                    "_id": "$image",
                    "documents": {
                        "$push": "$$ROOT"
                    }
                }
            },
            {
                "$sort": {
                    "documents.start_time": 1
                }
            }
            
        ]
        return self.db['mobile_usages'].aggregate(pipeline)
    