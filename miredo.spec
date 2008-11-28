Summary:	IPv6 Tunneling daemon
Summary(pl.UTF-8):	Demon do tunelowania IPv6
Name:		miredo
Version:	1.1.5
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.remlab.net/files/miredo/archive/%{name}-%{version}.tar.bz2
# Source0-md5:	c339a7dd24a985157e5e6c0dfd175a75
Source1:	%{name}-server.init
Source2:	%{name}-teredo.init
Source3:	%{name}-isatapd.init
URL:		http://www.simphalempin.com/dev/miredo/
BuildRequires:	judy-devel
Requires:	%{name}-common = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Miredo is an open-source Teredo IPv6 tunneling software, for Linux and
the BSD operating systems. It includes functional implementations of
all components of the Teredo specification (client, relay and server).
It is meant to provide IPv6 connectivity even from behind NAT devices.

This package contains Teredo server.

%description -l pl.UTF-8
Miredo to oprogramowanie do tunelowania IPv6 Toredo z otwartymi
źródłami dla systemów operacyjnych Linux i BSD. Zawiera funkcjonalne
implementacje wszystkich składników specyfikacji Toredo (klienta,
przekaźnika i serwera). Ma dostarczyć łączność z IPv6 nawet za
urządzeniami NAT.

Ten pakiet zawiera serwer Teredo.

%package common
Summary:	Common Miredo files
Group:		Daemons

%description common
Common Miredo files.

%package client-teredo
Summary:	Miredo Teredo client
Group:		Daemons
Requires:	%{name}-common = %{version}-%{release}

%description client-teredo
Miredo Teredo client.

%package client-isatap
Summary:	Miredo ISATAP client
Group:		Daemons
Requires:	%{name}-common = %{version}-%{release}

%description client-isatap
Miredo ISATAP client.

%package libs
Summary:	Miredo libraries
Group:		Libraries

%description libs
Miredo libraries.

%package devel
Summary:	Development files for miredo
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for miredo.

%package static
Summary:	Static miredo libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static miredo libraries.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-server
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-teredo
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}-isatapd

%find_lang %{name}

%post
/sbin/chkconfig --add miredo-server
%service miredo-server restart

%preun
if [ "$1" = "0" ]; then
        %service miredo-server stop
        /sbin/chkconfig --del miredo-server
fi

%post client-teredo
/sbin/chkconfig --add miredo-teredo
%service miredo-teredo restart

%preun client-teredo
if [ "$1" = "0" ]; then
        %service miredo-teredo stop
        /sbin/chkconfig --del miredo-teredo
fi

%post client-isatap
/sbin/chkconfig --add miredo-isatapd
%service miredo-isatapd restart

%preun client-isatap
if [ "$1" = "0" ]; then
        %service miredo-isatapd stop
        /sbin/chkconfig --del miredo-isatapd
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/miredo
%attr(755,root,root) %{_sbindir}/miredo-server
%{_mandir}/man5/miredo-server.conf.5*
%{_mandir}/man8/miredo-server.8*
%attr(754,root,root) /etc/rc.d/init.d/miredo-server

%files -f %{name}.lang common
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/teredo-mire
%attr(755,root,root) %{_sbindir}/miredo-checkconf
%dir %{_sysconfdir}/miredo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/miredo/miredo.conf
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/miredo/client-hook
%{_mandir}/man1/teredo-mire.1*
%{_mandir}/man8/miredo-checkconf.8*

%files client-teredo
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/miredo
%{_mandir}/man5/miredo.conf.5*
%{_mandir}/man8/miredo.8*
%attr(754,root,root) /etc/rc.d/init.d/miredo-teredo

%files client-isatap
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/isatapd
%{_mandir}/man5/isatapd.conf.5*
%{_mandir}/man8/isatapd.8*
%attr(754,root,root) /etc/rc.d/init.d/miredo-isatapd

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/libteredo
%{_includedir}/libtun6
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
