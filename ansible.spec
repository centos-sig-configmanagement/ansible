%if 0%{?rhel} == 5
%define __python /usr/bin/python26
%endif

%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%endif

Name: ansible
Summary: SSH-based configuration management, deployment, and task execution system
Version: 2.0.2.0
Release: 1%{?dist}

Group: Development/Libraries
License: GPLv3+
Source0: http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
# To retrieve the unittests, run:
#   ./get-unittests.sh 2.0.1.0 v2.0.1.0-1
# Replace the first parameter with the version you want in the tarball name
# Replace the second parameter with the git tag or hash that you want to sync with
Source1: ansible-unittests-%{version}.tar.xz
Source100: get-unittests.sh

# Patch control_path in the example config file to use %C so that it is shorter.
# Helps with paths that exceed the system length.
# Upstream issue: https://github.com/ansible/ansible/issues/11536
Patch0: ansible-2.0.2.0-control_path.patch

# Patch to utilize a newer jinja2 package on epel6
# Non-upstreamable as it creates a dependency on a specific version of jinja.
# This is desirable for us as we have packages for that version but not for
# upstream as they don't know what their customers are running.
Patch100: ansible-newer-jinja.patch

Url: http://ansible.com
BuildArch: noarch

%if 0%{?rhel} && 0%{?rhel} <= 5
BuildRequires: python26-devel

Requires: python26-PyYAML
Requires: python26-paramiko
Requires: python26-jinja2
Requires: python26-keyczar
Requires: python26-httplib2

%else

BuildRequires: python2-devel
BuildRequires: python-setuptools

# For tests
BuildRequires: PyYAML
BuildRequires: python-paramiko
BuildRequires: python-keyczar
BuildRequires: python-httplib2
BuildRequires: python-setuptools
BuildRequires: python-six
BuildRequires: python-nose
BuildRequires: python-coverage
BuildRequires: python-mock

%if (0%{?rhel} && 0%{?rhel} <= 6)
# Ansible will work with the jinja2 shipped with RHEL6 but users can gain
# additional jinja features by using the newer version
Requires: python-jinja2-26
BuildRequires: python-jinja2-26

# Distros with python < 2.7.0
BuildRequires: python-unittest2

%else
Requires: python-jinja2
BuildRequires: python-jinja2
%endif

Requires: PyYAML
Requires: python-paramiko
Requires: python-keyczar
Requires: python-httplib2
Requires: python-setuptools
Requires: python-six
Requires: sshpass
%endif

%if 0%{?rhel} == 6
# RHEL 6 needs a newer version of the pycrypto library for the ansible-vault
# command.  Note: If other pieces of ansible also grow to need pycrypto you may
# need to add: Requires: python-crypto or patch the other pieces of ansible to
# make use of this forward compat package (see the patch for ansible-vault
# above to see what needs to be done.)
Requires: python-crypto2.6
# The python-2.6 stdlib json module has a bug that affects the ansible
# to_nice_json filter
Requires: python-simplejson

# For testing
BuildRequires: python-crypto2.6
BuildRequires: python-simplejson
%endif

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

# RHEL7 doesn't have a recent enough ssh client to use this patch (needs to
# support %C in ControlPath).  So only apply it on Fedora.
%if 0%{?fedora}
%patch0 -p1
%endif

%if 0%{?rhel} == 6
%patch100 -p1
%endif

# Unittests
tar -xJvf %{SOURCE1}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/ansible/
mkdir -p $RPM_BUILD_ROOT/etc/ansible/roles/
cp examples/hosts $RPM_BUILD_ROOT/etc/ansible/
cp examples/ansible.cfg $RPM_BUILD_ROOT/etc/ansible/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp -v docs/man/man1/*.1 $RPM_BUILD_ROOT/%{_mandir}/man1/
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/ansible
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/ansible_plugins/{action,callback,connection,lookup,vars,filter}_plugins

%check
# RHEL <= 6 doesn't have a new enough python-mock to run the tests
%if 0%{?fedora} || 0%{?rhel} >= 7
make tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib}/ansible*
%{_bindir}/ansible*
%config(noreplace) %{_sysconfdir}/ansible/
%doc README.md PKG-INFO COPYING CHANGELOG.md
%doc %{_mandir}/man1/ansible*

%changelog
* Tue Apr 19 2016 Kevin Fenzi <kevin@scrye.com> - 2.0.2.0-1
- Update to 2.0.2.0. https://github.com/ansible/ansible/blob/stable-2.0/CHANGELOG.md
- Fixes CVE-2016-3096
- Fix for failed to resolve remote temporary directory issue. bug #1328359

* Thu Feb 25 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1.0-2
- Patch control_path to be not hit path length limitations (RH BZ #1311729)
- Version the test tarball

* Thu Feb 25 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1.0-1
- Update to upstream bugfix for 2.0.x release series.

* Thu Feb  4 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.0.0.2-3
- Utilize the python-jinja26 package on EPEL6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.0.0.2-1
- Ansible 2.0.0.2 release from upstream.  (Minor bugfix to one callback plugin
  API).

* Tue Jan 12 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.0.1-1
- Ansible 2.0.0.1 from upstream.  Rewrite with many bugfixes, rewritten code,
  and new features. See the upstream changelog for details:
  https://github.com/ansible/ansible/blob/devel/CHANGELOG.md

* Wed Oct 14 2015 Adam Williamson <awilliam@redhat.com> - 1.9.4-2
- backport upstream fix for GH #2043 (crash when pulling Docker images)

* Fri Oct 09 2015 Kevin Fenzi <kevin@scrye.com> 1.9.4-1
- Update to 1.9.4

* Sun Oct 04 2015 Kevin Fenzi <kevin@scrye.com> 1.9.3-3
- Backport dnf module from head. Fixes bug #1267018

* Tue Sep  8 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.3-2
- Pull in patch for yum module that fixes state=latest issue

* Thu Sep 03 2015 Kevin Fenzi <kevin@scrye.com> 1.9.3-1
- Update to 1.9.3
- Patch dnf as package manager. Fixes bug #1258080
- Fixes bug #1251392 (in 1.9.3 release)
- Add requires for sshpass package. Fixes bug #1258799

* Thu Jun 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.2-1
- Update to 1.9.2

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.1-2
- Fix for dnf

* Tue Apr 28 2015 Kevin Fenzi <kevin@scrye.com> 1.9.1-1
- Update to 1.9.1

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0.1-2
- Drop upstreamed epel6 patches. 

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0.1-1
- Update to 1.9.0.1

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0-1
- Update to 1.9.0

* Thu Feb 19 2015 Kevin Fenzi <kevin@scrye.com> 1.8.4-1
- Update to 1.8.4

* Tue Feb 17 2015 Kevin Fenzi <kevin@scrye.com> 1.8.3-1
- Update to 1.8.3

* Sun Jan 11 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.8.2-3
- Work around a bug in python2.6 by using simplejson (applies in EPEL6)

* Wed Dec 17 2014 Michael Scherer <misc@zarb.org> 1.8.2-2
- precreate /etc/ansible/roles and /usr/share/ansible_plugins

* Sun Dec 07 2014 Kevin Fenzi <kevin@scrye.com> 1.8.2-1
- Update to 1.8.2

* Thu Nov 27 2014 Kevin Fenzi <kevin@scrye.com> 1.8.1-1
- Update to 1.8.1

* Tue Nov 25 2014 Kevin Fenzi <kevin@scrye.com> 1.8-2
- Rebase el6 patch

* Tue Nov 25 2014 Kevin Fenzi <kevin@scrye.com> 1.8-1
- Update to 1.8

* Thu Oct  9 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.2-2
- Add /usr/bin/ansible to the rhel6 newer pycrypto patch

* Wed Sep 24 2014 Kevin Fenzi <kevin@scrye.com> 1.7.2-1
- Update to 1.7.2

* Thu Aug 14 2014 Kevin Fenzi <kevin@scrye.com> 1.7.1-1
- Update to 1.7.1

* Wed Aug 06 2014 Kevin Fenzi <kevin@scrye.com> 1.7-1
- Update to 1.7

* Fri Jul 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.10-1
- Update to 1.6.10

* Thu Jul 24 2014 Kevin Fenzi <kevin@scrye.com> 1.6.9-1
- Update to 1.6.9 with more shell quoting fixes.

* Tue Jul 22 2014 Kevin Fenzi <kevin@scrye.com> 1.6.8-1
- Update to 1.6.8 with fixes for shell quoting from previous release. 
- Fixes bugs #1122060 #1122061 #1122062

* Mon Jul 21 2014 Kevin Fenzi <kevin@scrye.com> 1.6.7-1
- Update to 1.6.7
- Fixes CVE-2014-4966 and CVE-2014-4967

* Tue Jul 01 2014 Kevin Fenzi <kevin@scrye.com> 1.6.6-1
- Update to 1.6.6

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.5-1
- Update to 1.6.5

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.4-1
- Update to 1.6.4

* Mon Jun 09 2014 Kevin Fenzi <kevin@scrye.com> 1.6.3-1
- Update to 1.6.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Kevin Fenzi <kevin@scrye.com> 1.6.2-1
- Update to 1.6.2 release

* Wed May  7 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6.1-1
- Bugfix 1.6.1 release

* Mon May  5 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6-1
- Update to 1.6
- Drop accelerate fix, merged upstream
- Refresh RHEL6 pycrypto patch.  It was half-merged upstream.

* Fri Apr 18 2014 Kevin Fenzi <kevin@scrye.com> 1.5.5-1
- Update to 1.5.5

* Mon Apr  7 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-2
- Fix setuptools requirement to apply to rhel=6, not rhel<6

* Wed Apr  2 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4
- Add upstream patch to fix accelerator mode
- Merge fedora and el6 spec files

* Fri Mar 14 2014 Kevin Fenzi <kevin@scrye.com> 1.5.3-2
- Update to NEW 1.5.3 upstream release.
- Add missing dependency on python-setuptools (el6 build)

* Thu Mar 13 2014 Kevin Fenzi <kevin@scrye.com> 1.5.3-1
- Update to 1.5.3
- Fix ansible-vault for newer python-crypto dependency (el6 build)

* Tue Mar 11 2014 Kevin Fenzi <kevin@scrye.com> 1.5.2-2
- Update to redone 1.5.2 release

* Tue Mar 11 2014 Kevin Fenzi <kevin@scrye.com> 1.5.2-1
- Update to 1.5.2

* Mon Mar 10 2014 Kevin Fenzi <kevin@scrye.com> 1.5.1-1
- Update to 1.5.1

* Fri Feb 28 2014 Kevin Fenzi <kevin@scrye.com> 1.5-1
- Update to 1.5

* Wed Feb 12 2014 Kevin Fenzi <kevin@scrye.com> 1.4.5-1
- Update to 1.4.5

* Sat Dec 28 2013 Kevin Fenzi <kevin@scrye.com> 1.4.3-1
- Update to 1.4.3 with ansible galaxy commands.
- Adds python-httplib2 to requires

* Wed Nov 27 2013 Kevin Fenzi <kevin@scrye.com> 1.4.1-1
- Update to upstream 1.4.1 bugfix release

* Thu Nov 21 2013 Kevin Fenzi <kevin@scrye.com> 1.4-1
- Update to 1.4

* Tue Oct 29 2013 Kevin Fenzi <kevin@scrye.com> 1.3.4-1
- Update to 1.3.4

* Tue Oct 08 2013 Kevin Fenzi <kevin@scrye.com> 1.3.3-1
- Update to 1.3.3

* Thu Sep 19 2013 Kevin Fenzi <kevin@scrye.com> 1.3.2-1
- Update to 1.3.2 with minor upstream fixes

* Mon Sep 16 2013 Kevin Fenzi <kevin@scrye.com> 1.3.1-1
- Update to 1.3.1

* Sat Sep 14 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-2
- Merge upstream spec changes to support EPEL5
- (Still needs python26-keyczar and deps added to EPEL)

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
