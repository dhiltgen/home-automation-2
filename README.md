# home-automation-2
Revamp of the home automation project

# Initial setup
* Set up the owfs.conf using either owfs-usb.conf or owfs-i2c.conf as a basis
* Set up the monitor/sensor.json using one of the templates in that dir

then

```bash
docker-compose up -d
```

# Notes:

* Write a batch of accumulated sensor data
```bash
SERVER=http://localhost:8086
QUEUE_FILE=hiltgen_queue
INFLUX_DB=sensors
INFLUX_USER='admin'
read -s INFLUX_PASSWORD

sudo mv ${QUEUE_FILE} ${QUEUE_FILE}.tmp && \
curl -u ${INFLUX_USER}:${INFLUX_PASSWORD} -X POST \
    "${SERVER}/write?db=${INFLUX_DB}&precision=s" \
    --data-binary @${QUEUE_FILE}.tmp && \
sudo rm -f ${QUEUE_FILE}.tmp
