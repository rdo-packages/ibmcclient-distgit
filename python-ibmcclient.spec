%{!?upstream_version: %global upstream_version %{version}%{?milestone}}


%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global library ibmcclient
%global _description \
python-ibmcclient is a Python library to communicate with HUAWEI `iBMC`\
based systems.\
\
The goal of the library is to be extremely simple, small, have as few\
dependencies as possible and be very conservative when dealing with BMCs\
by access HTTP REST API provided by HUAWEI `iBMC` based systems.\
\
Currently, the scope of the library has been limited to supporting\
OpenStack Ironic ibmc driver.\


Name:       python-%{library}
Version:    0.2.4
Release:    1%{?dist}
Summary:    Python library for managing HUAWEI iBMC based servers.
License:    Apache 2.0
URL:        https://github.com/IamFive/python-ibmcclient

Source0:    https://github.com/IamFive/python-ibmcclient/archive/%{upstream_version}.tar.gz

BuildArch:  noarch

%description %{_description}

%global _summary %{summary}

%package -n python2-%{library}
Summary:    %{_summary}
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# Unittest requirements
BuildRequires:  python2-requests
BuildRequires:  python2-mock
BuildRequires:  python2-responses

Requires: python2-requests
Requires: python2-six

%description -n python2-%{library} %{_description}


%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    %{_summary}
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# Unittest requirements
BuildRequires:  python3-requests
BuildRequires:  python3-mock
BuildRequires:  python3-responses

%description -n python3-%{library} %{_description}
%endif # with_python3


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf %{name}.egg-info


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif


%files -n python2-%{library}
%license LICENSE.txt 
%doc README.rst CHANGELOG.md
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%{python3_sitelib}/tests

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE.txt 
%doc README.rst CHANGELOG.md
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%{python3_sitelib}/tests
%endif

%changelog

* Thu May 28 2020 Qianbiao.NG <Qianbiao.NG@turnbig.net> - 0.2.4-1
- Repackage for openEuler OS
