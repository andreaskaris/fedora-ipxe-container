FROM fedora

RUN yum install ipxe-bootimgs dnsmasq iproute procps-ng python3-jinja2 httpd -y
RUN mkdir /tftpboot
# RUN chcon -t tftpdir_t /tftpboot
RUN mkdir /httpboot
RUN cp /usr/share/ipxe/undionly.kpxe /tftpboot
RUN cp /usr/share/ipxe/ipxe-x86_64.efi /tftpboot/ipxe.efi
RUN mkdir /tftpboot/menu
COPY render_boot_ipxe.py /render_boot_ipxe.py
COPY dnsmasq.conf.j2 /dnsmasq.conf.j2
COPY config /config
COPY entrypoint.sh /entrypoint.sh
COPY render_config.py /render_config.py
ENTRYPOINT ./entrypoint.sh
