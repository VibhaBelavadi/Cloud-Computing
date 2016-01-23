#!/bin/bash/
#Install ganglia web interface

wget http://sourceforge.net/projects/ganglia-web/3.5.10/ganglia-web-3.5.10.tar.gz
tar -xvf ganglia-web-3.5.10.tar.gz
cd ganglia-web-3.5.10/
vi Makefile
make install
