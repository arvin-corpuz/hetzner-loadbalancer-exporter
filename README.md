Prometheus Hetzner Load Balancer Exporter
-----------------------

Setup - Running on OS
-----------------------

1. Install python pip `sudo apt install python3-pip`
2. Install requirements `pip3 install -r requirements.txt`
3. Update Hetzner token and Load balancer ID on server.py
4. Copy required files, change permissions and reload daemon

```
cp server.py /opt/hetzner_lb_metrics/server.py
chmod +x /opt/hetzner_lb_metrics/server.py
cp systemd.service /etc/systemd/system/hetzner-lb-exporter.service
systemctl daemon-reload
systemctl enable hetzner-lb-exporter.service
systemctl start hetzner-lb-exporter.service
```

Setup - with Docker
--------------------------------
TBD