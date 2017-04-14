
sudo rm -rf  /home/orestis/nProbe/dump/dumpSYNATT/*

FILES=~/capture/ddostrace/split_fixed_addr/*
for f in ${FILES}
do
	echo $f > ~/capture/ddostrace/pcap_list
	~/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/ddostrace/pcap_list" /home/orestis/nProbe/dump/dumpSYNATT "ip proto 6"
	sleep 59
done

sudo rm -f /home/orestis/nProbe/dumpedited/editedSYNATT

sudo python3 /home/orestis/nProbe/transform_dump_files.py '/home/orestis/nProbe/dump/dumpSYNATT' '/home/orestis/nProbe/dumpedited/editedSYNATT'

#sudo rm -rf /home/orestis/nProbe/dump/dumpSYNATT/*

