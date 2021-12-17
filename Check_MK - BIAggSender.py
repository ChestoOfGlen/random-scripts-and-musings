#!/usr/bin/env python
# Script to extract LiveStatus information about BI Aggregations and send to Grafana
# Original Perl Script provided by Paul (paulmonitoring@gmail.com)
# Original Python Script provided by Check_MK (http://mathias-kettner.de/checkmk_livestatus.html)
# Modified by Adam Chesterton (chesterton.adam@gmail.com)
# Associated cron job. Place a file in /opt/omd/sites/<SITENAME>/etc/cron.d and note that the DB that was in use for this was InfluxDB
# */1 * * * * $OMD_ROOT/write-BI-InfluxDB.py > /tmp/bi_aggregation.txt.tmp; mv -f /tmp/bi_aggregation.txt.tmp /tmp/bi_aggregation.txt; curl -i -XPOST 'http://<GRAFANA-DB-SERVER-FQDN>:8086/write?db=<DB-NAME>' --data-binary @/tmp/bi_aggregation.txt > /dev/null 2>&1

import socket

socket_path = "/opt/omd/sites/<SITENAME>/tmp/run/live"
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(socket_path)

# Write command to socket and send
# Returned data example
# 0;Aggr TEST1
# 1;Aggr TEST2
query = "GET services\nColumns: state description\nFilter: description ~ ^Aggr\n"
s.sendall(query)

# Close sending direction, receive answer and cleanse string, strip last \n and then split on \n
s.shutdown(socket.SHUT_WR)
answer = s.recv(100000000)
answer = answer.rstrip('\n').split('\n')

#Loop through each line and print out in format for Influx to accept
for aggr in answer:
    aggr = aggr.replace(' ','_')
    status,service = aggr.split(';')
    print('bi-aggregation,service={} state={}').format(service, status)
