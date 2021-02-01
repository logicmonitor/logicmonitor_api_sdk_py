import logging
import os
import sys
import time

import psutil as psutil

sys.path.append("..")
import logicmonitor_api_sdk
from logicmonitor_api_sdk.api.response_interface import ResonseInterface
from logicmonitor_api_sdk.models import Resource, DataSource, DataPoint, \
  DataSourceInstance

from logicmonitor_api_sdk.api.metrics import Metrics

logger = logging.getLogger('lmingest.api')
logger.setLevel(logging.INFO)

configuration = logicmonitor_api_sdk.Configuration()
# For debug log, set the value to True
configuration.debug = False


class MyResponse(ResonseInterface):
  """
  Sample callback to handle the response from the REST endpoints
  """

  def success_callback(self, request, response, status, request_id):
    logger.info("%s: %s: %s", response, status, request_id)

  def error_callback(self, request, response, status, request_id, reason):
    logger.error("%s: %s: %s %s", response, status, reason, request_id)


def MetricRequest():
  """
  Main function to get the CPU values using `psutil` and send to Metrics REST endpoint
  """
  device_name = os.uname()[1]
  resource = Resource(ids={'system.displayname': device_name}, name=device_name,
                      create=True)
  datasource = DataSource(name="DiskUsingSDK")
  datapoints = ['total', 'used', 'free']
  metric_api = Metrics(batch=True, interval=10, response_callback=MyResponse())
  while True:
    partitions = psutil.disk_partitions()
    for p in partitions:
      # Using the device as instance name. We can use the mountpoint as well.
      instance_name = p.device
      usage = psutil.disk_usage(instance_name).__dict__
      # Create the instance object for every device. Name should not have the
      # special characters so replacing it with the '-'.
      instance = DataSourceInstance(name=instance_name.replace('/', '-'),
                                    display_name=instance_name)
      for one_datapoint in datapoints:
        datapoint = DataPoint(name=one_datapoint)
        values = {str(int(time.time())): str(usage[one_datapoint])}
        metric_api.send_metrics(resource=resource,
                                datasource=datasource,
                                instance=instance,
                                datapoint=datapoint,
                                values=values)
    time.sleep(10)


if __name__ == "__main__":
  MetricRequest()
