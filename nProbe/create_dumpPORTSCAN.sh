
sudo rm -rf  ./nProbe/dump/dumpPORTSC/*

FILES=~/capture/port_scanning/fixed_addr/*
for f in ${FILES}
do
	echo $f > ~/capture/port_scanning/pcap_list
	~/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/port_scanning/pcap_list" ./nProbe/dump/dumpPORTSC ""
	sleep 59
done

sudo rm -f ./nProbe/dumpedited/editedPORTSC

sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/dumpPORTSC' './nProbe/dumpedited/editedPORTSC'

#sudo rm -rf ./nProbe/dump/dumpPORTSC/*
