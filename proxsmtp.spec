%define	rname	proxsmtp
%define	name	%{rname}d

Summary:	ProxSMTP: An SMTP Filter
Name:		%{name}
Version:	1.8
Release:	%mkrel 3
License:	BSD
Group:		System/Servers
URL:		http://memberwebs.com/nielsen/software/proxsmtp/
Source0:	http://memberwebs.com/nielsen/software/proxsmtp/%{rname}-%{version}.tar.gz
Source1:	proxsmtpd.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ProxSMTP is a flexible tool that allows you to reject, change or
log email based on arbitrary critera.  It accepts SMTP connections
and forwards the SMTP commands and responses to another SMTP
server.  The 'DATA' email body is intercepted and filtered before
forwarding.

You need to be able to write the filtering scripts that integrate
it with your particular needs. If you're looking for something
that does virus filtering, take a look at ClamSMTP which behaves
similarly and uses a similar code base.

I wrote this with the Postfix mail server in mind.  ProxSMTP can
also be used as a transparent proxy to filter an entire network's
SMTP traffic at the router.

%prep

%setup -q -n %{rname}-%{version}

cp %{SOURCE1} proxsmtpd.init

for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build

%configure2_5x

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/run/proxsmtpd

%makeinstall

install -m0755 proxsmtpd.init %{buildroot}%{_initrddir}/proxsmtpd
install -m0644 doc/proxsmtpd.conf %{buildroot}%{_sysconfdir}/proxsmtpd.conf

%post
%_post_service proxsmtpd

%preun
%_preun_service proxsmtpd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README scripts
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/proxsmtpd.conf
%attr(0755,root,root) %{_initrddir}/proxsmtpd
%attr(0755,root,root) %{_sbindir}/proxsmtpd
%attr(0755,root,root) %dir /var/run/proxsmtpd
%{_mandir}/man5/proxsmtpd.conf.5*
%{_mandir}/man8/proxsmtpd.8*
