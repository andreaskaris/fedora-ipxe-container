build : 
	buildah bud -t localhost/fedora-ipxe-server .

run :
	podman run -d \
	--network host \
	--name fedora-pxe-server \
	localhost/fedora-ipxe-server

run-custom-env :
	podman run -d \
	--network host \
	-e PXE_LISTEN_ADDRESS=192.168.124.1 \
	-e PXE_INTERFACE=eth1 \
	-e PXE_DHCP_RANGE=192.168.124.200,192.168.124.250,255.255.255.0,24h \
	-e PXE_GATEWAY=192.168.124.1 \
	-e PXE_DOMAIN_NAME=example.net \
	-e PXE_BROADCAST=192.168.124.255 \
	--name fedora-pxe-server \
	localhost/fedora-ipxe-server

stop :
	podman stop fedora-pxe-server

remove-container : stop
	podman rm fedora-pxe-server

clean : remove-container
	podman image rm localhost/fedora-ipxe-server
