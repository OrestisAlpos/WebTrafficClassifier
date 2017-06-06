sudo rm -rf ~/capture/adam/split/newcapture1/*
editcap -c 1000000 ~/capture/adam/original/newcapture1.pcap ~/capture/adam/split/newcapture1/capture.pcap

sudo rm -rf ~/net/final_test/dump/*
sudo rm -f ~/net/final_test/dumpedited/*

file_count=0
FILES=~/capture/adam/split/newcapture1/*
for f in ${FILES}
do
	((file_count = file_count + 1))
	echo $f > ~/capture/adam/pcap_list
	~/net/nProbe/start_nprobe.sh "--pcap-file-list /home/orestis/capture/adam/pcap_list" './dump/' ''	
	if [ "${file_count}" -eq "20" ]; then
		break 	
	fi
	sleep 59
done

sudo python3 ~/net/nProbe/transform_dump_files.py '/home/orestis/net/final_test/dump' '/home/orestis/net/final_test/dumpedited/editedLEGIT'
