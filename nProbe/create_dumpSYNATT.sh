
sudo rm -rf  ./nProbe/dump/dumpSYNATT/*

FILES=~/capture/ddostrace/split_fixed_addr/*
for f in ${FILES}
do
	echo $f > ~/capture/ddostrace/pcap_list
	~/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/ddostrace/pcap_list" ./nProbe/dump/dumpSYNATT "ip proto 6"
	sleep 59
done

sudo rm -f ./nProbe/dumpedited/editedSYNATT

sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/dumpSYNATT' './nProbe/dumpedited/editedSYNATT'

#sudo rm -rf ./nProbe/dump/dumpSYNATT/*

