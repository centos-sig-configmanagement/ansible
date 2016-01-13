#!/bin/sh

if test -d ansible-temp ; then
  pushd ansible-temp
  git checkout devel
  git pull --rebase
  popd
else
  git clone https://github.com/ansible/ansible.git ansible-temp
fi

pushd ansible-temp
if test -n "$1" ; then
  git checkout "$1"
fi
popd
tar -cJvf ansible-unittests.tar.xz -C ansible-temp/ test/units
