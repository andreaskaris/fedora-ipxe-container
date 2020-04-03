#!/bin/bash

./render_config.py
mv dnsmasq.conf /etc/dnsmasq.conf
/usr/sbin/dnsmasq -k --log-facility=/dev/stdout &

sleep infinity
