sudo rm -rf ~/capture/adam/split/*
editcap -c 500000 ~/capture/adam/original/newcapture.pcap ~/capture/adam/split/capture.pcap

sudo rm -rf ~/nProbe/dump/benign/*

FILES=~/capture/adam/split/*
for f in ${FILES}
do
	echo $f > ~/capture/adam/pcap_list
	~/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/adam/pcap_list" '/home/orestis/nProbe/dump/benign' ''
	sleep 59
done

#sudo rm -rf ~/capture/adam/split/*

sudo rm -f ~nProbe/dumpedited/edited

sudo python3 /home/orestis/nProbe/transform_dump_files.py '/home/orestis/nProbe/dump/benign' '/home/orestis/nProbe/dumpedited/edited'
