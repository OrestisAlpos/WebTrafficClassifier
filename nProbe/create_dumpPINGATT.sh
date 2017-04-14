
sudo rm -rf  /home/orestis/nProbe/dump/dumpPINGATT/*

FILES=~/capture/ddostrace/split_fixed_addr/*
for f in ${FILES}
do
	echo $f > ~/capture/ddostrace/pcap_list
	~/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/ddostrace/pcap_list" /home/orestis/nProbe/dump/dumpPINGATT "ip proto 1"
	sleep 59
done

sudo rm -f /home/orestis/nProbe/dumpedited/editedPINGATT

sudo python3 /home/orestis/nProbe/transform_dump_files.py '/home/orestis/nProbe/dump/dumpPINGATT' '/home/orestis/nProbe/dumpedited/editedPINGATT'

#sudo rm -rf /home/orestis/nProbe/dump/dumpPINGATT/*
