# Instructions

* Edit config file and adjust to your needs.

* Build the container:
~~~
make build
~~~

* Create directory /dhcphosts
Use this as a directory for dnsmasq --dhcp-hostsdir= entries

* Create directory /httpboot
Each sub-directory is a menuentry (see httpboot dir for an example)

* Run the container:
~~~
make run
~~~

* Run container with custom, ad-hoc configuration:
~~~
podman run -d \
--network host \
--privileged \
-v /httpboot:/httpboot \
-e PXE_LISTEN_ADDRESS=192.168.124.1 \
-e PXE_INTERFACE=eth1 \
-e PXE_DHCP_RANGE=192.168.124.200,192.168.124.250,255.255.255.0,24h \
-e PXE_GATEWAY=192.168.124.1 \
-e PXE_DOMAIN_NAME=example.net \
-e PXE_BROADCAST=192.168.124.255 \
-e PXE_DNS_SERVERS=8.8.8.8,8.8.4.4 \
-e PXE_DHCP6_RANGE=fc00::1000,fc00::1999,24h \
--name fedora-ipxe-server \
localhost/fedora-ipxe-server
~~~

* If you need an example netinstall for testing, you can use:
~~~
make example-net-install
~~~
> You may need to adjust `example_netinstall.sh`

# Sources

* [https://dustymabe.com/2019/01/04/easy-pxe-boot-testing-with-only-http-using-ipxe-and-libvirt/](https://dustymabe.com/2019/01/04/easy-pxe-boot-testing-with-only-http-using-ipxe-and-libvirt/)
