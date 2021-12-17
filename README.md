# random-scripts-and-musings
Just a collection of random scripts and musings found or created

## Check_MK - BIAggSender
This just pulls the status (OK, CRIT, WARN, UNKOWN) of a BI Aggregation check service using CMK LiveStatus query, and sends it to an INfluxDB for use in Grafana to create percentage uptime graphs
