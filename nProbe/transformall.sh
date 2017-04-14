sudo rm -f ./nProbe/dumpedited/editedSYNATT
sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/dumpSYNATT' './nProbe/dumpedited/editedSYNATT'

sudo rm -f ./nProbe/dumpedited/editedPINGATT
sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/dumpPINGATT' './nProbe/dumpedited/editedPINGATT'

sudo rm -f ./nProbe/dumpedited/edited
sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/benign' './nProbe/dumpedited/edited'

sudo rm -f ./nProbe/dumpedited/editedPORTSC
sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/dumpPORTSC' './nProbe/dumpedited/editedPORTSC'

sudo rm -f ./nProbe/dumpedited/editedUDPATT
for port in 20 21 22 53 80 443 8080 400 8008 56521
do
	sudo rm -f ./nProbe/dumpedited/edited${port}UDPATT
        sudo python3 ./nProbe/transform_dump_files.py ./nProbe/dump/dumpUDPATT/${port}UDPATT ./nProbe/dumpedited/edited${port}UDPATT
