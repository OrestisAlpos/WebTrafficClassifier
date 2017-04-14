
sudo rm -rf  ./nProbe/dump/dumpPINGATT/*

FILES=~/capture/ddostrace/split_fixed_addr/*
for f in ${FILES}
do
	echo $f > ~/capture/ddostrace/pcap_list
	~/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/ddostrace/pcap_list" ./nProbe/dump/dumpPINGATT "ip proto 1"
	sleep 59
done

sudo rm -f ./nProbe/dumpedited/editedPINGATT

sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/dumpPINGATT' './nProbe/dumpedited/editedPINGATT'

#sudo rm -rf ./nProbe/dump/dumpPINGATT/*
