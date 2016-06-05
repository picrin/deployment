%define MAJOR %(echo $MAJOR)
%define MINOR %(echo $MINOR)
%define PATCH %(echo $PATCH)
Name:           websitego
Version:        %{MAJOR}.%{MINOR}
Release:        %{PATCH}
Summary:        Simple website in go

License:        GPL
URL:            example.com

Requires:  golang >= 1.0.0
BuildRequires:  golang >= 1.0.0

%description
A simple website in go

%files
/usr/bin/websitego	
/usr/lib/systemd/system/websitego.service

