#Module-Specific definitions
%define mod_name mod_countm
%define mod_conf A22_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_countm is a DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	3.0
Release:	%mkrel 4
Group:		System/Servers
License:	BSD
URL:		http://sourceforge.net/projects/countm/
Source0:	%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
BuildRequires:	gd-devel
BuildRequires:	png-devel 
BuildRequires:	freetype-devel
BuildRequires:	libjpeg-devel
BuildRequires:	db4-devel
BuildRequires:	zlib-devel
PreReq:		rpm-helper
#Requires:	fonts-ttf-west_european
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Provides:	apache2-mod_countm
Obsoletes:	apache2-mod_countm
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
An apache only module serving link counting information via jpeg
and png images. Configuration commands include font selection,
font size, image type, image background and text color, digit
width, reset, ignore, access list database, and random.

%prep

%setup -q -n %{mod_name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -L%{_libdir} -lgd -lfreetype -ljpeg -lpng -lm -ldb -c mod_countm.c version.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

install -d %{buildroot}/var/lib/%{mod_name}/dbase

# install the font..., i have no clue where to put it, 
# so i go by intuition and educated wild guessing...
install -d %{buildroot}%{_datadir}/fonts/ttf/western
install -m0644 FreeMono.ttf %{buildroot}%{_datadir}/fonts/ttf/western/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc *.html manual.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*
%attr(0755,apache,apache) %dir /var/lib/%{mod_name}
%attr(0755,apache,apache) %dir /var/lib/%{mod_name}/dbase
%attr(0644,root,root) %{_datadir}/fonts/ttf/western/FreeMono.ttf


