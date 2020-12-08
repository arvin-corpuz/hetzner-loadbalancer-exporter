from prometheus_client import Gauge, start_http_server
from datetime import datetime, timedelta
import requests
import time

OPEN_CONNECTIONS = Gauge('feedapi_lb_open_connections', 'No of Open connections')
REQUESTS_PER_SECOND = Gauge('feedapi_lb_requests_per_second', 'No of Requests per second')
CONNECTIONS_PER_SECOND = Gauge('feedapi_lb_connections_per_second', 'No of Connections per second')
BANDWIDTH_IN = Gauge('feedapi_lb_bandwidth_in', 'Ingress bandwidth in bytes')
BANDWIDTH_OUT = Gauge('feedapi_lb_bandwidth_out', 'Egress bandwidth in bytes')

headers = {'Authorization': 'Bearer <hetzner_token>'}
payload = {'type': 'requests_per_second,open_connections,connections_per_second,bandwidth', 'step': '15'}
url = 'https://api.hetzner.cloud/v1/load_balancers/<loadbalancer_id>/metrics'


def set_zero_metrics():
    metrics = [OPEN_CONNECTIONS, REQUESTS_PER_SECOND, CONNECTIONS_PER_SECOND, BANDWIDTH_IN, BANDWIDTH_OUT]
    for metric in metrics:
        metric.set(0)

def get_metric_data(data_list):
    sum = 0.0
    for data in data_list:
        try:
            sum = sum + float(data[1])
        except:
            pass
    return sum

def get_metrics():
    # Get start and end time 15 secs interval
    end = datetime.utcnow()
    start = end - timedelta(seconds=15)
    iso_end = end.strftime("%Y-%m-%dT%H%M%S")
    iso_start = start.strftime("%Y-%m-%dT%H%M%S")

    # Build request
    payload['start'] = iso_start
    payload['end'] = iso_end
    r = requests.get(url, headers=headers, params=payload)
    data = r.json().get('metrics').get('time_series')

    if not data:
        set_zero_metrics()

    # Set gauges
    OPEN_CONNECTIONS.set(get_metric_data(data.get('connections_per_second').get('values')))
    REQUESTS_PER_SECOND.set(get_metric_data(data.get('requests_per_second').get('values')))
    CONNECTIONS_PER_SECOND.set(get_metric_data(data.get('connections_per_second').get('values')))
    BANDWIDTH_IN.set(get_metric_data(data.get('bandwidth.in').get('values')))
    BANDWIDTH_OUT.set(get_metric_data(data.get('bandwidth.out').get('values')))


if __name__ == '__main__':
    start_http_server(9110)

    while True:
        time.sleep(5)
        get_metrics()