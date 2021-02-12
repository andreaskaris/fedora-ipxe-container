build : 
	buildah bud -t localhost/fedora-ipxe-server .

run :
	podman run -d \
	--network host \
	--privileged \
	-v /httpboot:/httpboot \
	-v /dhcphosts:/dhcphosts \
	--name fedora-ipxe-server \
	localhost/fedora-ipxe-server

run-custom-env :
	podman run -d \
	--network host \
	--privileged \
	-v /httpboot:/httpboot \
	-v /dhcphosts:/dhcphosts \
	-e PXE_LISTEN_ADDRESS=192.168.124.1 \
	-e PXE_LISTEN_PORT=8081 \
	-e PXE_INTERFACE=eth1 \
	-e PXE_DHCP_RANGE=192.168.124.200,192.168.124.250,255.255.255.0,24h \
	-e PXE_GATEWAY=192.168.124.1 \
	-e PXE_DOMAIN_NAME=example.net \
	-e PXE_BROADCAST=192.168.124.255 \
	-e PXE_DNS_SERVERS=8.8.8.8,8.8.4.4 \
	--name fedora-ipxe-server \
	localhost/fedora-ipxe-server

example-net-install:
	bash example_netinstall.sh

connect :
	podman exec -it fedora-ipxe-server /bin/bash

logs :
	podman logs -f fedora-ipxe-server

stop :
	podman stop fedora-ipxe-server

start :
	podman start fedora-ipxe-server

remove-container : stop
	podman rm fedora-ipxe-server

remove-image :
	podman image rm localhost/fedora-ipxe-server

clean : remove-container remove-image
