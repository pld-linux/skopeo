Summary:	Inspect container images and repositories on registries
Name:		skopeo
Version:	1.5.2
Release:	0.1
License:	Apache v2.0
Source0:	https://github.com/containers/skopeo/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1def68cb407fd310058e2c1558d2bc43
URL:		https://github.com/containers/skopeo
BuildRequires:	btrfs-progs-devel
BuildRequires:	device-mapper-devel
BuildRequires:	git-core
BuildRequires:	glib2-devel
BuildRequires:	golang >= 1.16.6
BuildRequires:	gpgme-devel
BuildRequires:	libassuan-devel
BuildRequires:	ostree-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%global import_path github.com/containers/skopeo
%define gobuild(o:) GO111MODULE=off go build -buildmode pie -compiler gc -tags="${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now'" -a -v -x %{?**};

%description
Command line utility to inspect images and repositories directly on
Docker registries without the need to pull them

%prep
%autosetup -Sgit -n %{name}-%{version}

sed -i 's;install-binary: bin/%{name};install-binary:;' Makefile
sed -i 's;install-docs: docs;install-docs:;' Makefile

mkdir -p src/github.com/containers
ln -s ../../../ src/%{import_path}

mkdir -p vendor/src
for v in vendor/*; do
	if test ${v} = vendor/src; then continue; fi
	if test -d ${v}; then
		mv ${v} vendor/src/
	fi
done

mkdir -p bin

%build
export GOPATH=$(pwd):$(pwd)/vendor
%gobuild -o bin/%{name} ./cmd/%{name}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    install-binary install-completions

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%attr(755,root,root) %{_bindir}/%{name}
%{bash_compdir}/%{name}
