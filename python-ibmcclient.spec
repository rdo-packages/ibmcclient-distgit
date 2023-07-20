%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order sphinx openstackdocstheme


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
Version:    XXX
Release:    XXX
Summary:    Python library for managing HUAWEI iBMC based servers
License:    Apache-2.0
URL:        https://github.com/IamFive/python-ibmcclient

Source0:    https://github.com/IamFive/python-ibmcclient/archive/%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires: git-core

%description %{_description}


%package -n python3-%{library}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{library} %{_description}


%prep
%autosetup -n %{name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install


# the tests folder is excluded in manifest.in,
# so, no tests will be run here.
# %check
# %{__python3} setup.py test

%files -n python3-%{library}
%license LICENSE.txt
%doc README.rst CHANGELOG.md
%{python3_sitelib}/ibmc_client
%{python3_sitelib}/python_%{library}-*.dist-info
# %exclude %{python3_sitelib}/tests

%changelog
