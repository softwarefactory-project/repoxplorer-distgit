Name:           repoxplorer
Version:        1.0.2
Release:        1%{?dist}
Summary:        RepoXplorer is a stats and charts utility for GIT repositories

License:        ASL 2.0
URL:            https://github.com/morucci/repoxplorer
Source0:        https://github.com/morucci/%{name}/archive/%{version}.tar.gz

Source1:        %{name}.service
Source2:        %{name}-webui.service
Source3:        index.yaml
Source4:        config.py

BuildArch:      noarch

Requires:       PyYAML
Requires:       python-pecan
Requires:       python-crypto
Requires:       python-dulwich
Requires:       python-urllib3
Requires:       python-elasticsearch
Requires:       uwsgi-plugin-python
Requires:       python-jsonschema
Requires:       pytz

BuildRequires:  systemd
Buildrequires:  python2-devel

%description
RepoXplorer is a stats and charts utility for Git repositories. Its main purpose is to
ease the visualization of stats for projects composed of one or multiple Git repositories.
Indeed lot of projects are splitted and have a Git repository by
components (server, client, library A, ...) and most of classic Git stat tools
do not handle that. RepoXplorer let's you describe how a project is composed and then
computes stats across them. RepoXplorer provides a Web user interface based on Bootstrap
and Jquery to let a user access data easily. It relies on ElasticSearch for its data backend.

%prep
%autosetup -n %{name}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/repoxplorer
mkdir -p %{buildroot}/%{_sysconfdir}/repoxplorer
mkdir -p %{buildroot}/%{_var}/lib/repoxplorer
mkdir -p %{buildroot}/%{_var}/log/repoxplorer
mv %{buildroot}/usr/local/share/repoxplorer %{buildroot}/%{_datadir}/
rm %{buildroot}/%{_datadir}/repoxplorer/*.yaml
rm %{buildroot}/%{_datadir}/repoxplorer/config.*
rm %{buildroot}/%{_datadir}/repoxplorer/repoxplorer.service
rm %{buildroot}/%{_datadir}/repoxplorer/repoxplorer-webui.service
install -p -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -p -D -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}-webui.service
install -p -D -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/%{name}/index.yaml
install -p -D -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}/config.py

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
* Wed Aug 09 2017 Fabien Boucher <fboucher@redhat.com> - 1.0.2-1
- Bump to 1.0.2

* Tue Aug 08 2017 Fabien Boucher <fboucher@redhat.com> - 1.0.1-1
- Bump to 1.0.1

* Tue May 02 2017 Fabien Boucher <fboucher@redhat.com> - 0.8.0-2
- Again extends static-map search dirs to be compatible with Software Factory

* Wed Apr 12 2017 Fabien Boucher <fboucher@redhat.com> - 0.8.0-1
- Bump to 0.8.0

* Wed Mar 15 2017 Fabien Boucher <fboucher@redhat.com> - 0.7.2-2
- Extends static-map search dirs to be compatible with Software Factory

* Sat Mar 11 2017 Fabien Boucher <fboucher@redhat.com> - 0.7.2-1
- Bump to 0.7.2

* Mon Mar 06 2017 Fabien Boucher <fboucher@redhat.com> - 0.7.1-1
- Bump to 0.7.1

* Mon Mar 06 2017 Fabien Boucher <fboucher@redhat.com> - 0.7-1
- Bump to 0.7

* Wed Mar 01 2017 Fabien Boucher <fboucher@redhat.com> - 0.6.2-2
- Change default config debug state in order to make pecan
  serves static files. This is to ease deployment. A better
  solution with a bundled uwsgi config will come soon.

* Mon Feb 20 2017 Fabien Boucher <fboucher@redhat.com> - 0.6.2-1
- Bump to 0.6.2

* Fri Feb 17 2017 Fabien Boucher - 0.6.1-1
- Bump to 0.6.1

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

* Thu Feb 16 2017 Fabien Boucher - 0.6-2
- Improve package

* Wed Feb 15 2017 Fabien Boucher - 0.6-1
- Initial packaging of release 0.6 of repoXplorer
