container : buildah bud -t localhost/fedora-ipxe-server .
clean : podman image rm localhost/fedora-ipxe-server
