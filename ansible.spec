%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif

Name: ansible
Release: 1%{?dist}
Summary: SSH-based configuration management, deployment, and task execution system
Version: 0.9

Group: Development/Libraries
License: GPLv3
Source0: https://github.com/downloads/ansible/ansible/%{name}-%{version}.tar.gz
Url: http://ansible.github.com

BuildArch: noarch
BuildRequires: python2-devel

Requires: PyYAML
Requires: python-paramiko
Requires: python-jinja2

%description

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

%package fireball
Summary: Ansible fireball transport support
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: python-keyczar
Requires: python-zmq

%description fireball

Ansible can optionally use a 0MQ based transport mechanism, which is
considerably faster than the standard ssh mechanism when there are
multiple actions, but requires additional supporting packages.

%package node-fireball
Summary: Ansible fireball transport - node end support
Group: Development/Libraries
Requires: python-keyczar
Requires: python-zmq

%description node-fireball

Ansible can optionally use a 0MQ based transport mechanism, which has
additional requirements for nodes to use.  This package includes those
requirements.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/ansible/
cp examples/hosts $RPM_BUILD_ROOT/etc/ansible/
cp examples/ansible.cfg $RPM_BUILD_ROOT/etc/ansible/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man1,man3}/
cp -v docs/man/man1/*.1 $RPM_BUILD_ROOT/%{_mandir}/man1/
cp -v docs/man/man3/*.3 $RPM_BUILD_ROOT/%{_mandir}/man3/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/ansible
cp -v library/* $RPM_BUILD_ROOT/%{_datadir}/ansible/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib}/ansible*
%{_bindir}/ansible*
%dir %{_datadir}/ansible
%{_datadir}/ansible/[a-eg-z]*
%{_datadir}/ansible/f[a-hj-z]*
%{_datadir}/ansible/file
%config(noreplace) %{_sysconfdir}/ansible
%doc README.md PKG-INFO COPYING
%doc %{_mandir}/man1/ansible*
%doc %{_mandir}/man3/ansible.[a-eg-z]*
%doc %{_mandir}/man3/ansible.f[a-hj-z]*
%doc %{_mandir}/man3/ansible.file*
%doc examples/playbooks

%files fireball
%{_datadir}/ansible/fireball
%doc %{_mandir}/man3/ansible.fireball.*

%files node-fireball
%doc README.md PKG-INFO COPYING

%changelog
* Fri Nov 30 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.9-0
- Release 0.9

* Fri Oct 19 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.8-0
- Release of 0.8

* Thu Aug 6 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.7-0
- Release of 0.7

* Mon Aug 6 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.6-0
- Release of 0.6

* Wed Jul 4 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.5-0
- Release of 0.5

* Wed May 23 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.4-0
- Release of 0.4

* Mon Apr 23 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.3-1
- Release of 0.3

* Tue Apr  3 2012 John Eckersberg <jeckersb@redhat.com> - 0.0.2-1
- Release of 0.0.2

* Sat Mar 10 2012  <tbielawa@redhat.com> - 0.0.1-1
- Release of 0.0.1
