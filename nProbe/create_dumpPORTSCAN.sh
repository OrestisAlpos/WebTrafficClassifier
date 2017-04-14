
sudo rm -rf  /home/orestis/nProbe/dump/dumpPORTSC/*

FILES=~/capture/port_scanning/fixed_addr/*
for f in ${FILES}
do
	echo $f > ~/capture/port_scanning/pcap_list
	~/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/port_scanning/pcap_list" /home/orestis/nProbe/dump/dumpPORTSC ""
	sleep 59
done

sudo rm -f /home/orestis/nProbe/dumpedited/editedPORTSC

sudo python3 /home/orestis/nProbe/transform_dump_files.py '/home/orestis/nProbe/dump/dumpPORTSC' '/home/orestis/nProbe/dumpedited/editedPORTSC'

#sudo rm -rf /home/orestis/nProbe/dump/dumpPORTSC/*
