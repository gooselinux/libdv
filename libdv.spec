Summary:        Software decoder for DV format video
Name:           libdv
Version:        1.0.0
Release:        8.1%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://libdv.sourceforge.net/
Source:         http://downloads.sourceforge.net/libdv/libdv-%{version}.tar.gz
Patch1:         libdv-0.104-no-exec-stack.patch
Patch2:         libdv-1.0.0-pic.patch
Patch3:         libdv-1.0.0-gtk2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  gtk2-devel
BuildRequires:  libXt-devel, libXv-devel
# Required for the gtk2 patch
BuildRequires:  autoconf, automake, libtool, SDL-devel
%if 0%{?fedora} >= 8 || 0%{?rhel} >= 6
BuildRequires: popt-devel
%endif
ExcludeArch:    s390 s390x

%description
The Quasar DV codec (libdv) is a software codec for DV video, the
encoding format used by most digital camcorders, typically those that
support the IEEE 1394 (a.k.a. FireWire or i.Link) interface. libdv was
developed according to the official standards for DV video: IEC 61834
and SMPTE 314M.

%package tools
Summary:        Basic tools to manipulate Digital Video streams
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description tools
This package contains some basic programs to display and encode
digital video streams. This programs uses the Quasar DV codec (libdv),
a software codec for DV video, the encoding format used by most
digital camcorders, typically those that support the IEEE 1394
(a.k.a. FireWire or i.Link) interface.

%package devel
Summary:        Development package for libdv
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for libdv.

%prep
%setup -q
%patch1 -p0 -b .no-exec-stack
%patch2 -p1 -b .pic
%patch3 -p1 -b .gtk2
# Required for libtool 2.2
libtoolize
# Required for the gtk2 patch
autoreconf

%build
%configure --with-pic
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/libdv.a
rm $RPM_BUILD_ROOT%{_libdir}/libdv.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING COPYRIGHT ChangeLog
%{_libdir}/libdv.so.*

%files tools
%defattr(-,root,root,-)
%doc README.*
%{_bindir}/dubdv
%{_bindir}/dvconnect
%{_bindir}/encodedv
%{_bindir}/playdv
%{_mandir}/man1/dubdv.1*
%{_mandir}/man1/dvconnect.1*
%{_mandir}/man1/encodedv.1*
%{_mandir}/man1/playdv.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libdv/
%{_libdir}/libdv.so
%{_libdir}/pkgconfig/libdv.pc

%changelog
* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.0.0-8.1
- Fix conditional for RHEL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Robert Scheck <robert@fedoraproject.org> 1.0.0-7
- Rebuilt against libtool 2.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.0-5
- fix conditional comparison

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> 1.0.0-4
- Bump and rebuild with gcc 4.3

* Wed Sep 12 2007 Jarod Wilson <jwilson@redhat.com> 1.0.0-3
- A few more fixes from Matthias Saou:
 - List man pages in %%files consistently w/o gz extension
 - Add BR: popt-devel for f8+, its now split fromm rpm-devel

* Wed Sep 12 2007 Jarod Wilson <jwilson@redhat.com> 1.0.0-2
- Update License field (Matthias Saou)
- Remove useless zero epoch (Matthias Saou)
- Add pkgconfig devel sub-package req (Matthias Saou)
- Minor spec formatting changes and clean-ups

* Fri Jan 19 2007 Jarod Wilson <jwilson@redhat.com> 1.0.0-1
- New upstream release
- PIC patch from Mike Frysinger <vapier@gentoo.org> (#146596)
- Re-enable asm on i386

* Thu Sep 21 2006 Jarod Wilson <jwilson@redhat.com> 0.104-5
- Disable asm on i386 for now to prevent text relocations in DSO

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:0.104-4.fc6.1
- rebuild

* Wed May 24 2006 Jarod Wilson <jwilson@redhat.com> 0.104-4
- disable PIC patch for now, it reliably causes segfaults on x86

* Sat May 13 2006 Jarod Wilson <jwilson@redhat.com> 0.104-3
- rebuilt against latest X libs

* Tue Mar 07 2006 Warren Togami <wtogami@redhat.com> 0.104-2
- remove instead of exclude static libs

* Wed Feb 15 2006 Matthias Saou <http://freshrpms.net/> 0.104-1
- Update to 0.104 at last (#147311)
- Include no-exec-stack, pic-fix, amd64reloc and gtk2 patches from Gentoo
  and PLD (merge gcc4 fix to the pic-fix patch).
- Now build against gtk2 (thanks to the patch above).
- Exclude static library.

* Mon Feb 13 2006 Paul Nasrat <pnasrat@redhat.com> - 0:0.103-4.3
- Patch to build with gcc 4.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:0.103-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:0.103-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Warren Togami <wtogami@redhat.com> - 0:0.103-3
- gcc4 rebuild

* Sun Feb 06 2005 Warren Togami <wtogami@redhat.com> - 0:0.103-2
- Fix erroneously requiring an executable stack (Nicholas Miell #146590)

* Sun Sep 19 2004 Warren Togami <wtogami@redhat.com> - 0:0.103-1
- upgrade to 0.103

* Sun Jun 20 2004 Jeremy Katz <katzj@redhat.com> - 0:0.102-4
- gtk+ doesn't need to be in the .pc file (committed upstream, reported
- don't require gtk+-devel for -devel package (unneeded)
  to fedora-devel-list by John Thacker)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 30 2004 Warren Togami <wtogami@redhat.com> 0:0.102-2
- Bug #123367 -devel Req gtk+-devel

* Mon Mar 29 2004 Warren Togami <wtogami@redhat.com> 0:0.102-1
- update to 0.102

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 14 2004 Warren Togami <wtogami@redhat.com> 0:0.101-2
- upgrade to 0.101
- spec cleanup
- exclude from mainframes
- GPL -> LGPL

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:0.99-0.fdr.2
- Added post/postun scriptlets

* Fri Apr 25 2003 Dams <anvil[AT]livna.org>
- Initial build.


