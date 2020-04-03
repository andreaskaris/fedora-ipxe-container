build : 
	buildah bud -t localhost/fedora-ipxe-server .

run : build
	podman run -d --network host -e PXE_SERVER_NIC=eth0 --name fedora-pxe-server localhost/fedora-ipxe-server

stop :
	podman stop fedora-pxe-server

remove-container : stop
	podman rm fedora-pxe-server

clean : remove-container
	podman image rm localhost/fedora-ipxe-server
