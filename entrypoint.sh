#!/bin/bash

./render_config.py
/usr/sbin/dnsmasq -k --log-facility=/dev/stdout &

sleep infinity
