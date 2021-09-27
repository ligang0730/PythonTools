#!/bin/sh

var=$1
part=$2
echo $var
echo $part
ifpart=${var:0:1}

if [ ! -d /tmp/cache ]; then
    mkdir -p /tmp/cache 
fi
mount -t ext3 /dev/mmcblk${part}p12 /tmp/cache

#if [[ ${var:1:1} -eq '1' ]];then
#    echo "烧写uboot"
#    dd if=/dev/zero of=/dev/mmcblk${part} bs=1k seek=768 conv=fsync count=129
#    echo 0 > /sys/block/mmcblk${part}boot0/force_ro
#    dd if=/tmp/cache/u-boot.bin of=/dev/mmcblk${part}boot0 bs=512 seek=2
#    echo 1 > /sys/block/mmcblk${part}boot0/force_ro
    #mmc bootpart enable 1 1 /dev/mmcblk1
#	if [ $? != 0 ]; then
#	    echo 0 > Sresult.log
#        exit $?
#    fi
#	rm -rf /tmp/cache/u-boot.bin
#fi

if [[ ${var:2:1} -eq '1' ]];then
    echo "烧写rootfs"
    if [[ ifpart -eq '0' ]];then
        echo y | mkfs.ext3 -j /dev/mmcblk${part}p1
        echo y | mkfs.ext3 -j /dev/mmcblk${part}p2
    fi
    mkdir -p /mnt/mmcblk${part}p1
    mkdir -p /mnt/mmcblk${part}p2
    mount -t ext3 /dev/mmcblk${part}p1 /mnt/mmcblk${part}p1
    mount -t ext3 /dev/mmcblk${part}p2 /mnt/mmcblk${part}p2
	
    tar xvf /tmp/cache/rootfs.tar.bz2 -C /mnt/mmcblk${part}p1
    tar xvf /tmp/cache/rootfs.tar.bz2 -C /mnt/mmcblk${part}p2
	if [ $? != 0 ]; then
	    echo 0 > Sresult.log
        exit $?
    fi
	rm -rf /tmp/cache/rootfs.tar.bz2
fi

if [[ ${var:3:1} -eq '1' ]];then
    echo "烧写platform"
    if [[ ifpart -eq '0' ]];then
        echo y | mkfs.ext3 -j /dev/mmcblk${part}p9
        echo y | mkfs.ext3 -j /dev/mmcblk${part}p10
    fi
    mkdir -p /mnt/mmcblk${part}p9
    mkdir -p /mnt/mmcblk${part}p10
    mount -t ext3 /dev/mmcblk${part}p9 /mnt/mmcblk${part}p9
    mount -t ext3 /dev/mmcblk${part}p10 /mnt/mmcblk${part}p10
	
    tar xvf /tmp/cache/platform.tar.bz2 -C /mnt/mmcblk${part}p9
    tar xvf /tmp/cache/platform.tar.bz2 -C /mnt/mmcblk${part}p10
    if [ $? != 0 ]; then
	    echo 0 > Sresult.log
        exit $?
    fi
	echo "烧写versioninfo"
    if [[ ifpart -eq '0' ]];then
        echo y | mkfs.ext3 -j /dev/mmcblk${part}p6
    fi
    mkdir -p /mnt/mmcblk${part}p6
    mount -t ext3 /dev/mmcblk${part}p6 /mnt/mmcblk${part}p6
	
    tar xvf /tmp/cache/versioninfo.tar.bz2 -C /mnt/mmcblk${part}p6
	if [ $? != 0 ]; then
	    echo 0 > Sresult.log
        exit $?
    fi
	rm -rf /tmp/cache/platform.tar.bz2
	rm -rf /tmp/cache/versioninfo.tar.bz2
fi

if [[ ${var:4:1} -eq '1' ]];then
    echo "烧写config"
    if [[ ifpart -eq '0' ]];then
        echo y | mkfs.ext3 -j /dev/mmcblk${part}p7
        echo y | mkfs.ext3 -j /dev/mmcblk${part}p8
    fi
    mkdir -p /mnt/mmcblk${part}p7
    mkdir -p /mnt/mmcblk${part}p8
    mount -t ext3 /dev/mmcblk${part}p7 /mnt/mmcblk${part}p7
    mount -t ext3 /dev/mmcblk${part}p8 /mnt/mmcblk${part}p8
	
    tar xvf /tmp/cache/config.tar.bz2 -C /mnt/mmcblk${part}p7
    tar xvf /tmp/cache/config.tar.bz2 -C /mnt/mmcblk${part}p8
	if [ $? != 0 ]; then
	    echo 0 > Sresult.log
        exit $?
    fi
	rm -rf /tmp/cache/config.tar.bz2
fi

echo 1 > Sresult.log
