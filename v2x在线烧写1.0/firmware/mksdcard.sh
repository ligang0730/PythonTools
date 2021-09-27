#!/bin/sh

var=$1
part=$2
echo $var
echo $part
node=/dev/mmcblk${part}

if [[ ${var:0:1} -eq '1' ]];then
umount /tmp/cache
sleep 2
echo "正在分区"
# partition size in MB
BOOT_ROM_START=0
BOOT_ROM_SIZE=10
# p1
FW_A_START=`expr ${BOOT_ROM_START} + ${BOOT_ROM_SIZE}`
FW_A_SIZE=400
# p2
FW_B_START=`expr ${FW_A_START} + ${FW_A_SIZE}`
FW_B_SIZE=400
# p3
ROOTFS_A_START=`expr ${FW_B_START} + ${FW_B_SIZE}`
ROOTFS_A_SIZE=4
# p4
EXTEND_START=818
# p5
ROOTFS_B_START=`expr ${EXTEND_START}`
ROOTFS_B_SIZE=4
# p6
VER_INFO_START=`expr ${ROOTFS_B_START} + ${ROOTFS_B_SIZE}`
VER_INFO_SIZE=4
# p7
CONFIG_A_START=`expr ${VER_INFO_START} + ${VER_INFO_SIZE}`
CONFIG_A_SIZE=8
# p8
CONFIG_B_START=`expr ${CONFIG_A_START} + ${CONFIG_A_SIZE}`
CONFIG_B_SIZE=8
# p9
PLATFORM_A_START=`expr ${CONFIG_B_START} + ${CONFIG_B_SIZE}`
PLATFORM_A_SIZE=512
# p10
PLATFORM_B_START=`expr ${PLATFORM_A_START} + ${PLATFORM_A_SIZE}`
PLATFORM_B_SIZE=512
# p11
CUST_START=`expr ${PLATFORM_B_START} + ${PLATFORM_B_SIZE}`
CUST_SIZE=4
# p12
CACHE_START=`expr ${CUST_START} + ${CUST_SIZE}`
#CACHE_SIZE=512
# p13
#RESERVE_START=`expr ${CACHE_START} + ${CACHE_SIZE}`

TOTAL_SIZE=`sfdisk -s ${node}`
TOTAL_SIZE_MB=`expr ${total_size} / 1024`
EXTEND_SIZE=`expr ${TOTAL_SIZE_MB} - ${EXTEND_START}`


# call sfdisk to create partition table
# destroy the partition table

dd if=/dev/zero of=${node} bs=1024 count=1

sfdisk --force -uM ${node} << EOF
${FW_A_START},${FW_A_SIZE},83
${FW_B_START},${FW_B_SIZE},83
${ROOTFS_A_START},${ROOTFS_A_SIZE},83
${EXTEND_START},${EXTEND_SIZE},5
${ROOTFS_B_START},${ROOTFS_B_SIZE},83
${VER_INFO_START},${VER_INFO_SIZE},83
${CONFIG_A_START},${CONFIG_A_SIZE},83
${CONFIG_B_START},${CONFIG_B_SIZE},83
${PLATFORM_A_START},${PLATFORM_A_SIZE},83
${PLATFORM_B_START},${PLATFORM_B_SIZE},83
${CUST_START},${CUST_SIZE},83
${CACHE_START},${CACHE_SIZE},83
EOF

sleep 1

echo y | mkfs.ext3 -j ${node}p1
echo y | mkfs.ext3 -j ${node}p2
#echo y | mkfs.ext3 -j ${node}p3
#echo y | mkfs.ext3 -j ${node}p5
echo y | mkfs.ext3 -j ${node}p6
echo y | mkfs.ext3 -j ${node}p7
echo y | mkfs.ext3 -j ${node}p8
echo y | mkfs.ext3 -j ${node}p9
echo y | mkfs.ext3 -j ${node}p10
echo y | mkfs.ext3 -j ${node}p12

if [ ! -d /tmp/cache ]; then
    mkdir -p /tmp/cache
fi
mount -t ext3 ${node}p12 /tmp/cache
echo 1 > Fresult.log

fi
