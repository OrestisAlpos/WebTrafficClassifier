
sudo rm -rf ./nProbe/dump/dumpUDPATT/*

for port in 20 21 22 53 80 443 8080 400 8008 56521 20 21 22 53 80 443 8080 400 8008 56521 20 21 22 53 80 443 8080 400 8008 56521 
do
	mkdir ./nProbe/dump/dumpUDPATT/${port}UDPATT
	~/nProbe/start_nprobe.sh '-i vboxnet0' ./nProbe/dump/dumpUDPATT/${port}UDPATT '' &
	nprobe_pid=$!
	for i in {1..12}
	do
		sudo python /home/orestis/scripts/udp_flood_attack.py "${port}" &
		pids[${i}]=$!
	done
	for pid in ${pids[*]}
	do
		wait ${pid}
	done
	echo | sudo killall -SIGINT nprobe
	sleep 5

done


sudo rm -rf ./nProbe/dumpedited/editedUDPATT

for port in 20 21 22 53 80 443 8080 400 8008 56521
do
	sudo python3 ./nProbe/transform_dump_files.py './nProbe/dump/dumpUDPATT/'${port}'UDPATT' './nProbe/dumpedited/edited$'{port}'UDPATT'
done


#sudo rm -rf ./nProbe/dump/dumpUDPATT/*
