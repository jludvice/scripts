#!/bin/env bash

# example usage
# dips > /etc/dnsmasq.d/docker.conf && systemctl restart dnsmasq.service 

CONF='/etc/dnsmasq.d/docker.conf'

NET=`docker network ls | sed 1d | awk '{print $2}'`

dockerips() {
  RUNNING_CONTAINERS=`docker ps | sed 1d | awk '{print $NF}'`
  NETWORK_NAME="$1"
  IPS=''
  for C in $RUNNING_CONTAINERS
  do
    ip=$(docker inspect --format "{{.NetworkSettings.Networks.${NETWORK_NAME}.IPAddress}}" $C)
    if [ "${ip}" != "<no value>" ]; then
      echo "address=/$C.$NETWORK_NAME/$ip"
    fi
  done
}

dips() {
  for N in $NET
  do
    dockerips $N
  done
}

dips
