#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	Library for working with MaxMind DB files
Name:		libmaxminddb
Version:	0.5.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/maxmind/libmaxminddb/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	475386f4cb6d12cbae2eaa05dbaa7851
URL:		http://maxmind.github.io/libmaxminddb/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libmaxminddb library provides functions for working MaxMind DB
files.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q

%build
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mmdblookup
%attr(755,root,root) %{_libdir}/libmaxminddb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmaxminddb.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/libmaxminddb.md
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config.h
%{_libdir}/libmaxminddb.la
%{_mandir}/man3/MMDB_*.3
%{_mandir}/man3/libmaxminddb.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmaxminddb.a
%endif
