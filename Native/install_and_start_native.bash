#!/bin/bash
#sudo lsa
cd ~
wget -c http://feliperoman.com.br/mestrado/Native/start_simulator.bash
chmod 777 start_simulator.bash
wget -c http://feliperoman.com.br/mestrado/Native/configure_native.bash
chmod 777 configure_native.bash
cd catkin_ws
source devel/setup.bash
cd src
pwd
wget -c http://feliperoman.com.br/mestrado/Native/rbx2.tar
pwd
tar -xvf rbx2.tar
rm rbx2.tar
cd ~
./configure_native.bash
./start_simulator.bash
