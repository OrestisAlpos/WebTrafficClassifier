sudo rm -f /home/orestis/nProbe/dumpedited/editedSYNATT
sudo python3 /home/orestis/nProbe/transform_dump_files.py '/home/orestis/nProbe/dump/dumpSYNATT' '/home/orestis/nProbe/dumpedited/editedSYNATT'

sudo rm -f /home/orestis/nProbe/dumpedited/editedPINGATT
sudo python3 /home/orestis/nProbe/transform_dump_files.py '/home/orestis/nProbe/dump/dumpPINGATT' '/home/orestis/nProbe/dumpedited/editedPINGATT'

sudo rm -f /home/orestis/nProbe/dumpedited/edited
sudo python3 /home/orestis/nProbe/transform_dump_files.py '/home/orestis/nProbe/dump/benign' '/home/orestis/nProbe/dumpedited/edited'

sudo rm -f /home/orestis/nProbe/dumpedited/editedPORTSC
sudo python3 /home/orestis/nProbe/transform_dump_files.py '/home/orestis/nProbe/dump/dumpPORTSC' '/home/orestis/nProbe/dumpedited/editedPORTSC'

sudo rm -f /home/orestis/nProbe/dumpedited/editedUDPATT
for port in 20 21 22 53 80 443 8080 400 8008 56521
do
	sudo rm -f /home/orestis/nProbe/dumpedited/edited${port}UDPATT
        sudo python3 /home/orestis/nProbe/transform_dump_files.py /home/orestis/nProbe/dump/dumpUDPATT/${port}UDPATT /home/orestis/nProbe/dumpedited/edited${port}UDPATT
