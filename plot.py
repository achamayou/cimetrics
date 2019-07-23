import yaml
import pymongo
import os

def get_settings():
  with open('metrics.yml') as cfgf:
    cfg = yaml.safe_load(cfgf)
    return cfg['db'], cfg['collection'], cfg['main_branch']

DB, COLLECTION, MAIN_BRANCH = get_settings()

class Metrics:
  def __init__(self):
    uri = os.getenv("COSMOS_CONNECTION")
    self.client = pymongo.MongoClient(uri)
    db = self.client[DB]
    self.col = db[COLLECTION]

  def all(self):
    return self.col.find()

  def last_for_branch(self, branch): 
    return next(self.col.find({'branch': branch}).sort([('created', pymongo.DESCENDING)]).limit(1))

  def bars(self, branch, reference):
    branch_metrics = self.last_for_branch(branch)['metrics']
    reference_metrics = self.last_for_branch(reference)['metrics']

    b = []
    r = []
    ticks = []
    for field in branch_metrics.keys() | reference_metrics.keys():
      b = branch_metrics.get
 
if __name__ == '__main__':
  m = Metrics()
  #for p in m.all():
  #  print(p)
  print(next(m.last_for_branch(MAIN_BRANCH)))