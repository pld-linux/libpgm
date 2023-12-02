Summary:	PGM reliable multicast network protocol library
Summary(pl.UTF-8):	Biblioteka wiarygodnego multicastowego protokołu sieciowego PGM
Name:		libpgm
Version:	5.3.128
%define	tagver	%(echo %{version} | tr . -)
Release:	2
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/steve-o/openpgm/releases
Source0:	https://github.com/steve-o/openpgm/archive/release-%{tagver}/openpgm-%{version}.tar.gz
# Source0-md5:	134eb021a8e4618ef87d54456282d186
Patch0:		%{name}-inline.patch
Patch1:		python3.patch
URL:		https://github.com/steve-o/openpgm
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	libtool >= 2:2.2
BuildRequires:	perl-base
BuildRequires:	python3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenPGM is a library implementing the PGM reliable multicast network
protocol.

%description -l pl.UTF-8
OpenPGM to biblioteka implementująca wiarygodny sieciowy protokół
multicastowy PGM.

%package devel
Summary:	Header files for OpenPGM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenPGM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenPGM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenPGM.

%package static
Summary:	Static OpenPGM library
Summary(pl.UTF-8):	Statyczna biblioteka OpenPGM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenPGM library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenPGM.

%prep
%setup -q -n openpgm-release-%{tagver}
%patch0 -p1
%patch1 -p1

%{__mv} openpgm/pgm/openpgm-{5.2,5.3}.pc.in

%build
cd openpgm/pgm
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C openpgm/pgm install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# TODO: provide link/pointer to rfc3208 in common RFCs package
%doc openpgm/pgm/{LICENSE,README} openpgm/doc/draft-ietf-rmt-bb-pgmcc-03.txt
%attr(755,root,root) %{_libdir}/libpgm-5.3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpgm-5.3.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpgm.so
%{_includedir}/pgm-5.3
%{_pkgconfigdir}/openpgm-5.3.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpgm.a
