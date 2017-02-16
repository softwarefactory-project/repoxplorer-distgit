Name:           repoxplorer
Version:        0.6
Release:        6%{?dist}
Summary:        RepoXplorer is a small stats and charts utility for GIT repositories

License:        ASL 2.0
URL:            https://github.com/morucci/repoxplorer
Source0:        https://github.com/morucci/%{name}/archive/%{version}.tar.gz

Source1:        %{name}.service
Source2:        %{name}-webui.service
Source3:        projects.yaml
Source4:        idents.yaml
Source5:        config.py
Source6:        repoxplorer-indexer.patch

BuildArch:      noarch

Requires:       PyYAML
Requires:       python-pecan
Requires:       python-crypto
Requires:       python-dulwich
Requires:       python-urllib3
Requires:       python-elasticsearch
Requires:       uwsgi-plugin-python

BuildRequires:  systemd
Buildrequires:  python2-devel

%description
RepoXplorer is a small stats and charts utility for Git repositories.
Its main purpose is to ease the visualization of stats for one or more
project(s) composed of multiple Git repositories.

%prep
%autosetup -n %{name}-%{version}
patch -p0 < %{SOURCE6}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/usr/share/repoxplorer
mkdir -p %{buildroot}/%{_sysconfdir}/repoxplorer
mkdir -p %{buildroot}/%{_var}/lib/repoxplorer
mkdir -p %{buildroot}/%{_var}/log/repoxplorer
mv %{buildroot}/usr/local/share/repoxplorer %{buildroot}/usr/share/
rm %{buildroot}/usr/bin/el-*.sh
rm %{buildroot}/usr/share/repoxplorer/projects.yaml
rm %{buildroot}/usr/share/repoxplorer/idents.yaml
rm %{buildroot}/usr/share/repoxplorer/config.*
rm %{buildroot}/usr/share/repoxplorer/repoxplorer.service
rm %{buildroot}/usr/share/repoxplorer/repoxplorer-webui.service
install -p -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -p -D -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}-webui.service
install -p -D -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/%{name}/projects.yaml
install -p -D -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}/idents.yaml
install -p -D -m 644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/%{name}/config.py

%check
#%{__python2} setup.py nosetests

%pre
#getent group repoxplorer >/dev/null || groupadd -r repoxplorer -g 160
#getent passwd repoxplorer >/dev/null || \
#useradd -r -g repoxplorer -u 160 -d /usr/share/repoxplorer -s /sbin/nologin \
#-c "Repoxplorer Daemons" repoxplorer
#exit 0

%post
%systemd_post %{name}.service
%systemd_post %{name}-webui.service

%preun
%systemd_preun %{name}.service
%systemd_preun %{name}-webui.service

%postun
%systemd_postun %{name}.service
%systemd_postun %{name}-webui.service

%files
%{python2_sitelib}/*
%{_datadir}/*
%{_bindir}/*
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/*
%{_var}/lib/*
%{_var}/log/*

%changelog
* Fri Feb 17 2017 Fabien Boucher - 0.6-6
- Add repoxplorer-indexer patch

* Fri Feb 17 2017 Fabien Boucher - 0.6-5
- Fix paths to templates files
- Set elasticsearch host to localhost

* Fri Feb 17 2017 Fabien Boucher - 0.6-4
- Add missing dependencies and fix uwsgi options

* Fri Feb 17 2017 Fabien Boucher - 0.6-3
- Change default webui listening port to TCP/51000

* Tue Feb 16 2017 Fabien Boucher - 0.6-2
- Improve package

* Wed Feb 15 2017 Fabien Boucher - 0.6-1
- Initial packaging of release 0.6 of repoXplorer
