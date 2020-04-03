FROM fedora

RUN yum install ipxe-bootimgs dnsmasq iproute procps-ng python3-jinja2 -y
RUN mkdir /tftpboot
# RUN chcon -t tftpdir_t /tftpboot
RUN mkdir /httpboot
RUN cp /usr/share/ipxe/undionly.kpxe /tftpboot
RUN cp /usr/share/ipxe/ipxe-x86_64.efi /tftpboot/ipxe.efi
RUN mkdir /tftpboot/menu
COPY boot.ipxe /tftpboot/menu/boot.ipxe
COPY dnsmasq.conf.j2 /dnsmasq.conf.j2
COPY config /config
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ./entrypoint.sh
