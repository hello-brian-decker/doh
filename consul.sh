#!/usr/bin/env bash

mkdir -p /etc/profile.d/ && touch /etc/profile.d/env.sh
services=("$@")
ip="$2"
for service in "${services[@]}"; do
  until $(curl --output /dev/null --silent --head --fail http://$ip:8500/v1/catalog/service/$service); do
    sleep 5
  echo ${service}_HOST=${service_ip} >> /etc/profile.d/env.sh
  echo ${service}_PORT=${service_port} >> /etc/profile.d/env.sh
  unset service service_ip service_port
  done
done