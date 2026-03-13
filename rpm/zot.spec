%define _bindir /usr/local/bin

Name:           zot
Version:        %{zot_version}
Release:        1%{?dist}
Summary:        OCI Distribution Specification compliant container image registry
License:        Apache-2.0
URL:            https://github.com/project-zot/zot

Source0:        zot
Source1:        zot.service
Source2:        config.json
Source3:        credentials.json

BuildArch:      x86_64

Requires:       jq

%description
Zot is a production-ready, open-source, vendor-neutral OCI-native container
image registry that is compliant with the OCI Distribution Specification.
It supports OCI image and artifact types including container images, Helm charts,
OPA bundles, and Singularity.

%install
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 %{SOURCE0} %{buildroot}%{_bindir}/zot

install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/zot.service

install -d -m 0755 %{buildroot}/etc/zot
install -m 0644 %{SOURCE2} %{buildroot}/etc/zot/config.json
install -m 0600 %{SOURCE3} %{buildroot}/etc/zot/credentials.json

install -d -m 0755 %{buildroot}/var/lib/zot

%files
%{_bindir}/zot
%{_unitdir}/zot.service
%dir /etc/zot
%config(noreplace) /etc/zot/config.json
%config(noreplace) /etc/zot/credentials.json
%dir /var/lib/zot

%pre
getent group zot >/dev/null || groupadd -r zot
getent passwd zot >/dev/null || useradd -r -g zot -d /var/lib/zot -s /sbin/nologin -c "Zot Registry" zot
exit 0

%post
%systemd_post zot.service
echo "Zot registry installed. Edit /etc/zot/config.json and start with: systemctl start zot"

%preun
%systemd_preun zot.service

%postun
%systemd_postun_with_restart zot.service

%changelog
