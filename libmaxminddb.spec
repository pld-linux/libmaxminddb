#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# build without tests

Summary:	Library for working with MaxMind DB files
Summary(pl.UTF-8):	BIblioteka do pracy z plikami MaxMind DB
Name:		libmaxminddb
Version:	1.4.3
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/maxmind/libmaxminddb/releases
Source0:	https://github.com/maxmind/libmaxminddb/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	97896f01e3d5922237b11718d0dcae85
URL:		http://maxmind.github.io/libmaxminddb/
%if %{with tests}
BuildRequires:	perl-IPC-Run3
BuildRequires:	perl-Test-Output
BuildRequires:	perl-Test-Simple >= 0.88
%endif
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libmaxminddb library provides a C library for reading MaxMind DB
files, including the GeoIP2 databases from MaxMind. This is a custom
binary format designed to facilitate fast lookups of IP addresses
while allowing for great flexibility in the type of data associated
with an address.

%description -l pl.UTF-8
Biblioteka libmaxminddb jest biblioteką C do odczytu plików MaxMind
DB, zawierających bazy danych GeoIP2 firmy MaxMind. Jest to własny
format binarny zaprojektowany z myślą o szybkim wyszukiwaniu adresów
IP i dużej elastyczności typu danych powiązanych z adresem.

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

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmaxminddb.la

# bogus link
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/defined.3

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changes.md NOTICE README.md
%attr(755,root,root) %{_bindir}/mmdblookup
%attr(755,root,root) %{_libdir}/libmaxminddb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmaxminddb.so.0
%{_mandir}/man1/mmdblookup.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmaxminddb.so
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config.h
%{_pkgconfigdir}/libmaxminddb.pc
%{_mandir}/man3/MMDB_*.3
%{_mandir}/man3/libmaxminddb.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmaxminddb.a
%endif
