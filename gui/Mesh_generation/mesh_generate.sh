#!/bin/bash
#放到系统中后需要改
currentpath=$1
procs=$2
echo 开始生成blockMesh...
source /home/export/online3/amd_share/OpenFOAM_x86/OpenFOAM-4.x-version-4.1/etc/bashrc
export LD_LIBRARY_PATH=/home/export/online3/amd_share/OpenFOAM_x86/ThirdParty-3.0.0/platforms/linux64Icc/boost-system/lib:/home/export/online3/amd_share/OpenFOAM_x86/ThirdParty-3.0.0/platforms/linux64Icc/CGAL-4.7/lib:/home/export/online3/amd_share/OpenFOAM_x86/ThirdParty-3.0.0/platforms/linux64Icc/gperftools-svn/lib:/home/export/online3/amd_share/OpenFOAM_x86/ThirdParty-3.0.0/platforms/linux64Icc/ParaView-4.4.0/lib/paraview-4.4:/home/export/online3/amd_share/OpenFOAM_x86/OpenFOAM-3.0.0/platforms/linux64IccDPInt64Opt/lib/mpi:/home/export/online3/amd_share/OpenFOAM_x86/ThirdParty-3.0.0/platforms/linux64IccDPInt64Opt/lib/mpi:/usr/sw-cluster/mpi2/lib:/home/export/base/nsccwuxi_amd/amd_app/OpenFOAM/amd_app-3.0.0/platforms/linux64IccDPInt64Opt/lib:/home/export/online3/amd_share/OpenFOAM_x86/site/3.0.0/platforms/linux64IccDPInt64Opt/lib:/home/export/online3/amd_share/OpenFOAM_x86/OpenFOAM-3.0.0/platforms/linux64IccDPInt64Opt/lib:/home/export/online3/amd_share/OpenFOAM_x86/ThirdParty-3.0.0/platforms/linux64IccDPInt64Opt/lib:/home/export/online3/amd_share/OpenFOAM_x86/OpenFOAM-3.0.0/platforms/linux64IccDPInt64Opt/lib/dummy:/usr/sw-cluster/intel/composer_xe_2013_sp1.4.211/compiler/lib/intel64:/usr/sw-cluster/intel/composer_xe_2013_sp1.4.211/mpirt/lib/intel64:/usr/sw-cluster/intel/composer_xe_2013_sp1.4.211/mkl/lib/intel64:/usr/sw-cluster/intel/composer_xe_2013_sp1.3.174/compiler/lib/intel64:/usr/sw-cluster/intel/composer_xe_2013_sp1.3.174/mpirt/lib/intel64:/usr/sw-cluster/intel/composer_xe_2013_sp1.3.174/ipp/../compiler/lib/intel64:/usr/sw-cluster/intel/composer_xe_2013_sp1.3.174/ipp/lib/intel64:/usr/sw-cluster/intel/composer_xe_2013_sp1.3.174/mkl/lib/intel64:/usr/sw-cluster/intel/composer_xe_2013_sp1.3.174/tbb/lib/intel64/gcc4.4:/usr/sw-cluster/slurm-16.05.3/lib
# export PATH=/home/leo/OpenFOAM/ThirdParty-8/platforms/linux64Gcc/gperftools-svn/bin:/home/leo/OpenFOAM/leo-8/platforms/linux64GccDPInt32Opt/bin:/home/leo/OpenFOAM/site/8/platforms/linux64GccDPInt32Opt/bin:/home/leo/OpenFOAM/OpenFOAM-8/platforms/linux64GccDPInt32Opt/bin:/home/leo/OpenFOAM/OpenFOAM-8/bin:/home/leo/OpenFOAM/OpenFOAM-8/wmake:/home/leo/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
# export LD_LIBRARY_PATH=/home/leo/OpenFOAM/ThirdParty-8/platforms/linux64Gcc/gperftools-svn/lib:/home/leo/OpenFOAM/OpenFOAM-8/platforms/linux64GccDPInt32Opt/lib/openmpi-system:/home/leo/OpenFOAM/ThirdParty-8/platforms/linux64GccDPInt32/lib/openmpi-system:/usr/lib/x86_64-linux-gnu/openmpi/lib:/home/leo/OpenFOAM/leo-8/platforms/linux64GccDPInt32Opt/lib:/home/leo/OpenFOAM/site/8/platforms/linux64GccDPInt32Opt/lib:/home/leo/OpenFOAM/OpenFOAM-8/platforms/linux64GccDPInt32Opt/lib:/home/leo/OpenFOAM/ThirdParty-8/platforms/linux64GccDPInt32/lib:/home/leo/OpenFOAM/OpenFOAM-8/platforms/linux64GccDPInt32Opt/lib/dummy
cd $currentpath
/usr/sw-mpp/bin/bsub -I -q q_x86_share -n 1 blockMesh | tee blockmesh.log
echo blockMesh生成完毕
echo 开始生成.emesh...
/usr/sw-mpp/bin/bsub -I -q q_x86_share -n 1 surfaceFeatureExtract
echo .emesh生成完毕
echo 开始生成snappyHexMesh...
if [ $procs -eq 1 ]; then
/usr/sw-mpp/bin/bsub -I -q q_x86_share -n $procs snappyHexMesh | tee snappyHexMesh.log
else
/usr/sw-mpp/bin/bsub -I -q q_x86_share -n $procs snappyHexMesh -parallel | tee snappyHexMesh.log 
fi
echo snappyHexMesh生成完毕
