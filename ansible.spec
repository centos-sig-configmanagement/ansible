%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif

Name: ansible
Release: 1%{?dist}
Summary: SSH-based configuration management, deployment, and task execution system
Version: 1.3.0

Group: Development/Libraries
License: GPLv3
Source0: http://ansibleworks.com/releases/%{name}-%{version}.tar.gz
Url: http://ansibleworks.com

BuildArch: noarch
BuildRequires: python2-devel

Requires: PyYAML
Requires: python-paramiko
Requires: python-jinja2
Requires: python-keyczar

# 
# This is needed to update the old ansible-firewall package that is no 
# longer needed. Note that you should also remove ansible-node-firewall manually
# Where you still have it installed. 
#
Provides: ansible-fireball = %{version}-%{release}
Obsoletes: ansible-fireball < 1.2.4

%description

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

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
cp -va library/* $RPM_BUILD_ROOT/%{_datadir}/ansible/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib}/ansible*
%{_bindir}/ansible*
%{_datadir}/ansible
%exclude %{_datadir}/ansible/utilities/fireball
%exclude %{_mandir}/man3/ansible.fireball.*
%config(noreplace) %{_sysconfdir}/ansible
%doc README.md PKG-INFO COPYING
%doc %{_mandir}/man1/ansible*
%doc %{_mandir}/man3/ansible*
%doc examples/playbooks

%changelog
* Thu Sep 12 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-1
- Update to 1.3.0
- Drop node-fireball subpackage entirely.
- Obsolete/provide fireball subpackage. 
- Add Requires python-keyczar on main package for accelerated mode.

* Wed Aug 21 2013 Kevin Fenzi <kevin@scrye.com> 1.2.3-2
- Update to 1.2.3
- Fixes CVE-2013-4260 and CVE-2013-4259

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Kevin Fenzi <kevin@scrye.com> 1.2.2-1
- Update to 1.2.2 with minor fixes

* Fri Jul 05 2013 Kevin Fenzi <kevin@scrye.com> 1.2.1-2
- Update to newer upstream re-release to fix a syntax error

* Thu Jul 04 2013 Kevin Fenzi <kevin@scrye.com> 1.2.1-1
- Update to 1.2.1
- Fixes CVE-2013-2233

* Mon Jun 10 2013 Kevin Fenzi <kevin@scrye.com> 1.2-1
- Update to 1.2

* Tue Apr 02 2013 Kevin Fenzi <kevin@scrye.com> 1.1-1
- Update to 1.1

* Mon Mar 18 2013 Kevin Fenzi <kevin@scrye.com> 1.0-1
- Update to 1.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.9-0
- Release 0.9

* Fri Oct 19 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.8-0
- Release of 0.8

* Thu Aug 9 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.7-0
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
