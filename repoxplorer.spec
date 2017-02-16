%global srcname repoxplorer

Name:           %{srcname}
Version:        0.6
Release:        1%{?dist}
Summary:        RepoXplorer is a small stats and charts utility for GIT repositories

License:        ASL 2.0
URL:            https://github.com/morucci/repoxplorer
Source0:        https://github.com/morucci/%{srcname}/archive/%{version}.tar.gz

BuildArch:      noarch

Requires:       python-pecan
Requires:       python-wsgi

Buildrequires:  python2-devel
Buildrequires:  python-nose

%description
RepoXplorer is a small stats and charts utility for Git repositories.
Its main purpose is to ease the visualization of stats for one or more
project(s) composed of multiple Git repositories.

%prep
%autosetup -n %{srcname}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/usr/share/repoxplorer
mv %{buildroot}/usr/local/share/repoxplorer %{buildroot}/usr/share/repoxplorer
rm %{buildroot}/usr/bin/el-*.sh

%check
#%{__python2} setup.py nosetests

%files
%{python2_sitelib}/*
%{_datadir}/*
%{_bindir}/*

%changelog
* Wed Feb 15 2017 Fabien Boucher - 0.6-1
- Initial packaging of release 0.6 of repoXplorer
