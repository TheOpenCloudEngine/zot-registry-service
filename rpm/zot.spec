%define _bindir /usr/local/bin
%define _unitdir /usr/lib/systemd/system

Name:           zot
Version:        %{zot_version}
Release:        1%{?dist}
Summary:        OCI Distribution Specification compliant container image registry
License:        Apache-2.0
URL:            https://github.com/TheOpenCloudEngine/zot-registry-service
Packager:       Open Cloud Engine Community

Source0:        zot
Source1:        zot.service
Source2:        config.json
Source3:        credentials.json
Source4:        generate_certs.sh
Source5:        hosts.txt

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

install -d -m 0755 %{buildroot}/etc/zot/certs
install -m 0755 %{SOURCE4} %{buildroot}/etc/zot/certs/generate_certs.sh
install -m 0644 %{SOURCE5} %{buildroot}/etc/zot/certs/hosts.txt

install -d -m 0755 %{buildroot}/var/lib/zot

%files
%{_bindir}/zot
%{_unitdir}/zot.service
%dir /etc/zot
%config(noreplace) /etc/zot/config.json
%config(noreplace) /etc/zot/credentials.json
%dir /etc/zot/certs
/etc/zot/certs/generate_certs.sh
%config(noreplace) /etc/zot/certs/hosts.txt
%dir /var/lib/zot

%pre
getent group zot >/dev/null || groupadd -r zot
getent passwd zot >/dev/null || useradd -r -g zot -d /var/lib/zot -s /sbin/nologin -c "Zot Registry" zot
exit 0

%post
if [ $1 -eq 1 ] && command -v systemctl >/dev/null 2>&1; then
    systemctl daemon-reload >/dev/null 2>&1 || :
    systemctl enable zot.service >/dev/null 2>&1 || :
fi
echo "Zot registry installed. Edit /etc/zot/config.json and start with: systemctl start zot"

%preun
if [ $1 -eq 0 ] && command -v systemctl >/dev/null 2>&1; then
    systemctl stop zot.service >/dev/null 2>&1 || :
    systemctl disable zot.service >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ] && command -v systemctl >/dev/null 2>&1; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%changelog
