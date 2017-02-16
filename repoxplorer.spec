Name:           repoxplorer
Version:        0.6
Release:        7%{?dist}
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
mkdir -p %{buildroot}/%{_datadir}/repoxplorer
mkdir -p %{buildroot}/%{_sysconfdir}/repoxplorer
mkdir -p %{buildroot}/%{_var}/lib/repoxplorer
mkdir -p %{buildroot}/%{_var}/log/repoxplorer
mv %{buildroot}/usr/local/share/repoxplorer %{buildroot}/%{_datadir}/
rm %{buildroot}/usr/bin/el-*.sh
rm %{buildroot}/%{_datadir}/repoxplorer/projects.yaml
rm %{buildroot}/%{_datadir}/repoxplorer/idents.yaml
rm %{buildroot}/%{_datadir}/repoxplorer/config.*
rm %{buildroot}/%{_datadir}/repoxplorer/repoxplorer.service
rm %{buildroot}/%{_datadir}/repoxplorer/repoxplorer-webui.service
install -p -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -p -D -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}-webui.service
install -p -D -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/%{name}/projects.yaml
install -p -D -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}/idents.yaml
install -p -D -m 644 %{SOURCE5} %{buildroot}/%{_sysconfdir}/%{name}/config.py

%check
#%{__python2} setup.py nosetests

%pre
getent group repoxplorer >/dev/null || groupadd -r repoxplorer
getent passwd repoxplorer >/dev/null || \
useradd -r -g repoxplorer -G repoxplorer -d /usr/share/repoxplorer -s /sbin/nologin \
-c "Repoxplorer daemons" repoxplorer
exit 0

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
%attr(-, repoxplorer, repoxplorer) %{_var}/lib/repoxplorer
%attr(-, repoxplorer, repoxplorer) %{_var}/log/repoxplorer

%changelog
* Fri Feb 17 2017 Fabien Boucher - 0.6-7
- Fix perms

* Fri Feb 17 2017 Fabien Boucher - 0.6-6
- Add repoxplorer-indexer patch
- Define repoxplorer user and set service files

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
