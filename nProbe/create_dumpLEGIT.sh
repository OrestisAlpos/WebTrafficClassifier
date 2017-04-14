sudo rm -rf ~/capture/adam/split/*
editcap -c 500000 ~/capture/adam/original/newcapture.pcap ~/capture/adam/split/capture.pcap

sudo rm -rf ~/nProbe/dump/benign/*

FILES=~/capture/adam/split/*
for f in ${FILES}
do
	echo $f > ~/capture/adam/pcap_list
	~/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/adam/pcap_list" './nProbe/dump/benign' ''
	sleep 59
done

#sudo rm -rf ~/capture/adam/split/*

sudo rm -f ~nProbe/dumpedited/edited

sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/benign' './nProbe/dumpedited/edited'
