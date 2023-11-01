%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           system-storage-manager
Version:        1.4
Release:        1%{?dist}
Summary:        A single tool to manage your storage

Group:          System Environment/Base
License:        GPLv2+
URL:            https://system-storage-manager.github.io/
Source0:        https://github.com/system-storage-manager/ssm/archive/%{name}-%{version}.tar.gz

Patch1:		0001-ssm-enforce-python3.patch
Patch2:		0002-Remove-info-command-for-RHEL.patch
Patch3:		0003-unittests-better-multipath-message-on-fail.patch
Patch4:		0004-bashtests-allow-testing-of-system-wide-ssm.patch
Patch5:		0005-bashtests-remove-btrfs-tests.patch
Patch6:		0006-tests-add-bash-test-skipping-capabilities.patch
Patch7:		0007-show-available-memory-when-running-tests.patch
Patch8:		0008-tests-018-remove-unnecessary-check-for-crypt.patch
Patch9:	0009-tests-rhel8-changed-default-luks1-to-luks2.patch
Patch10:	0010-crypt-accept-versions-with-rc-suffix-as-well.patch


BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-pwquality
Requires:       util-linux
Requires:       which
Requires:       xfsprogs
Requires:       e2fsprogs
Requires:       python3-pwquality


%description
System Storage Manager provides an easy to use command line interface to manage
your storage using various technologies like lvm, btrfs, encrypted volumes and
more.

In more sophisticated enterprise storage environments, management with Device
Mapper (dm), Logical Volume Manager (LVM), or Multiple Devices (md) is becoming
increasingly more difficult.  With file systems added to the mix, the number of
tools needed to configure and manage storage has grown so large that it is
simply not user friendly.  With so many options for a system administrator to
consider, the opportunity for errors and problems is large.

The btrfs administration tools have shown us that storage management can be
simplified, and we are working to bring that ease of use to Linux file systems
in general.

You should install the ssm if you need to manage your storage with various
technologies via a single unified interface.


%prep
%setup -q -n ssm-%{name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1



%build
make docs


%install
rm -rf ${RPM_BUILD_ROOT}
%{__python3} setup.py install --root=${RPM_BUILD_ROOT}
if [ "%{_pkgdocdir}" != "%{_docdir}/%{name}-%{version}" ]; then
    mv ${RPM_BUILD_ROOT}/{%{_docdir}/%{name}-%{version},%{_pkgdocdir}}
fi

%check
# run unit tests, these have to pass
%{__python3} test.py -u


%files
%{_bindir}/ssm
%{_pkgdocdir}/
%{_mandir}/man8/ssm.8*
%{python3_sitelib}/ssmlib/
%{python3_sitelib}/*.egg-info


%changelog
*Wed Jun 5 2019 Jan Tulak <jtulak@redhat.com> - 1.4-1:
- Bring changes from upstream 1.4 (mostly bugfixes)
- Remove multipath from the list of default backends (rhbz#1685019)
- Fix locale issue (rhbz#1679587)

*Fri Feb 15 2019 Jan Tulak <jtulak@redhat.com> - 1.2-3:
- Gating tests implementation, which meant adding few more changes
  to the existing patches (#1681969)
- sphinx patch was merged to python3 change
- add seq numbers to patch files

*Fri Feb 15 2019 Jan Tulak <jtulak@redhat.com> - 1.2-2:
- fix poor luks password leads to ssm crash (rhbz#1670714)

* Sun Aug 12 2018 Jan Tulak <jtulak@redhat.com> - 1.2-1
- Upstream release 1.2 which fixes:
- use pwquality to test password strength for cryptsetup (#1141871)
- add multipath detection support (#1309729)
- add migrate command (#1014708)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 30 2017 Jan Tulak <jtulak@redhat.com> - 0.5-0
- New upstream stable version 0.5

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4-12
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-11
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5


* Mon Jul 27 2015 Lukas Czerner <lczerner@redhat.com> 0.4-7
- Big upstream update
- Python3 support (#1239016)
- Error out if file system is not supported (#1196428)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Lukas Czerner <lczerner@redhat.com> 0.4-4
- Update to a new upstream release v0.4
- Remove btrfs resize support
- Unmount all btrfs subvolumes when removing a filesystem
- Fix size argument parsing for create and snapshot command
- Fix list output for some cases
- Add support to create encrypted volumes with crypt backend
- Add dry-run option
- Fix removing volumes with crypt backend
- Add raid1 and raid10 support for lvm backend
- Allow to check btrfs volumes
- Fix error handling when trying to resize btrfs subvolume
- Fix ssm mount command so it detects directory properly
- Suppress backtrace when a command fails
- Fix ssm to recognize units in new btrfs output properly
- Use correct sysfs file to get size for a partition
- Fix ssm to be able add a device with signature to btrfs file system
- Resognize btrfs devices from new btrfs output properly


* Mon Dec 16 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.2-4
- Install docs to %%{_pkgdocdir} where available (#994122).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jun  1 2012 Lukas Czerner <lczerner@redhat.com> 0.2-1
- Initial version of the package
