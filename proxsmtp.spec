%define	rname	proxsmtp
%define	name	%{rname}d

Summary:	ProxSMTP: An SMTP Filter
Name:		%{name}
Version:	1.8
Release:	4
License:	BSD
Group:		System/Servers
URL:		https://memberwebs.com/nielsen/software/proxsmtp/
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


%changelog
* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8-3mdv2011.0
+ Revision: 627817
- don't force the usage of automake1.7

* Tue Sep 15 2009 Thierry Vignaud <tv@mandriva.org> 1.8-2mdv2010.0
+ Revision: 441960
- rebuild

* Thu Oct 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1.8-1mdv2009.1
+ Revision: 294370
- 1.8

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 1.6-4mdv2009.0
+ Revision: 259296
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.6-3mdv2009.0
+ Revision: 247224
- rebuild
- fix no-buildroot-tag

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 1.6-1mdv2008.1
+ Revision: 131620
- kill re-definition of %%buildroot on Pixel's request


* Fri Jan 26 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6-1mdv2007.0
+ Revision: 113820
- Import proxsmtpd

* Fri Jan 26 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6-1mdv2007.1
- 1.6

* Sun Dec 25 2005 Oden Eriksson <oeriksson@mandriva.com> 1.3-1mdk
- 1.3

* Fri Nov 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.6-1mdk
- initial mandrake package

