from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = endpoint
  def collect(self):
    # Fetch the JSON
    # FIXME 
    # response = json.loads(requests.get(self._endpoint).content.decode('UTF-8'))

    with open('stats.json', 'r') as f:
        response = json.load(f)

    for resp in response['pods']: 
        podname = resp['podRef']['name']
        namespace = resp['podRef']['namespace']
        labels = {
            'namespace' : namespace,
            'pod'       : podname
        }
        ephem = resp['ephemeral-storage']
        prefix = 'pod_ephemeralstorage'

        ephem_usedBytes =       resp['ephemeral-storage']['usedBytes']
        ephem_availableBytes =  resp['ephemeral-storage']['availableBytes']
        ephem_capacityBytes =   resp['ephemeral-storage']['capacityBytes']
        ephem_inodesFree =      resp['ephemeral-storage']['inodesFree']
        ephem_inodes =          resp['ephemeral-storage']['inodes']
        ephem_inodesUsed =      resp['ephemeral-storage']['inodesUsed']

        yield self.add_metric(prefix, 'usage_bytes', ephem_usedBytes, labels, 'UsedBytes represents the bytes used for a specific task on the filesystem. This may differ from the total bytes used on the filesystem and may not equal CapacityBytes - AvailableBytes.')
        yield self.add_metric(prefix, 'avail_bytes', ephem_availableBytes, labels, 'AvailableBytes represents the storage space available (bytes) for the filesystem.')
        yield self.add_metric(prefix, 'avail_bytes_total', ephem_capacityBytes, labels, 'CapacityBytes represents the total capacity (bytes) of the filesystems underlying storage.')
        yield self.add_metric(prefix, 'usage_inodes', ephem_inodesUsed, labels, 'InodesUsed represents the inodes used by the filesystem. This may not equal Inodes - InodesFree because this filesystem may share inodes with other "filesystems".')
        yield self.add_metric(prefix, 'avail_inodes', ephem_inodesFree, labels, 'InodesFree represents the free inodes in the filesystem.')
        yield self.add_metric(prefix, 'avail_inodes_total', ephem_inodes, labels, 'Inodes represents the total inodes in the filesystem.')

  
  def add_metric(self, prefix, name, value, labels, summary):
    metric = Metric(prefix + '_' + name, summary, 'summary')
    metric.add_sample(prefix + '_' + name, value=value, labels=labels)        
    return metric
 
if __name__ == '__main__':
  # Usage: json_exporter.py port endpoint
  print('Starting to serve on port ' + str(sys.argv[1]))
  start_http_server(int(sys.argv[1]))
  REGISTRY.register(JsonCollector(sys.argv[2]))

  while True: time.sleep(1)



# Metric explanation: 
# https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/apis/stats/v1alpha1/types.go