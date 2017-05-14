import os
import numpy as np
import datetime
import glob
import random

class Reader:
	

	def __init__(self, fp_logfile, debug_mode):
		self.debug_mode = debug_mode
			
		file_count = 0
		x_train = []
		y_train = []
		x_test = []
		y_test = []	
	
		rootDir = './nProbe/dumpedited'
	
		lineBuff = ""
		lineBuff_lenprv = -1
		c = 0
	
		for dirName, subdirList, fileList in os.walk(rootDir):
			for fname in fileList:
				file_count += 1
				file_data = open(dirName + '/' + fname, 'r')
				file_data.readline() #read away the first line (title)
				classType = "LEGIT"	#0	
				if dirName.endswith("PINGATT") or fname.endswith("PINGATT"):
					classType = "PINGATT"	#1	
				elif dirName.endswith("SYNATT") or fname.endswith("SYNATT"):
					classType = "SYNATT"	#2
				elif dirName.endswith("UDPATT") or fname.endswith("UDPATT"):
					classType = "UDPATT"	#3
				elif dirName.endswith("PORTSC") or fname.endswith("PORTSC"):
					classType = "PORTSC"	#4
				while True:
					c = (c + 1) % 4 # Write every 4th packet to the test array, all the others to the train array	
					line = file_data.readline()
					if not line:
						break
					if (c != 0):
						lineBuff = [np.uint16(s) for s in line.replace('.','|').split('|')]
						if lineBuff_lenprv != -1 and len(lineBuff) != lineBuff_lenprv:
							print("error with input data")
							exit(0)
						else:
							lineBuff_lenprv = len(lineBuff)
						x_train.append(lineBuff)
						if classType=="LEGIT":
							y_train.append(0)
						elif classType=="PINGATT":
							y_train.append(1)
						elif classType=="SYNATT":
							y_train.append(2)
						elif classType=="UDPATT":
							y_train.append(3)
						elif classType=="PORTSC":
							y_train.append(4)
					else:
						lineBuff = [np.uint16(s) for s in line.replace('.','|').split('|')]
						if lineBuff_lenprv != -1 and len(lineBuff) != lineBuff_lenprv:
							print("error with input data")
							exit(0)
						else:
							lineBuff_lenprv = len(lineBuff)
						x_test.append(lineBuff)
						if classType=="LEGIT":
							y_test.append(0)
						elif classType=="PINGATT":
							y_test.append(1)
						elif classType=="SYNATT":
							y_test.append(2)
						elif classType=="UDPATT":
							y_test.append(3)
						elif classType=="PORTSC":
							y_test.append(4)

				file_data.close()
		
		self.x_train = np.array(x_train)
		self.y_train = np.array(y_train)
		self.x_test = np.array(x_test)
		self.y_test = np.array(y_test)
	
		self.x_trainNorm = self.normalize(self.x_train)
		self.x_testNorm = self.normalize(self.x_test)
		
		assert (self.x_train.shape[1] == self.x_test.shape[1]), "THERE WAS AN ERROR IN THE CODE READING THE DATA"
		assert (self.x_train.shape[0] == self.y_train.shape[0]), "THERE WAS AN ERROR IN THE CODE READING THE DATA"
		assert (self.x_test.shape[0] == self.y_test.shape[0]), "THERE WAS AN ERROR IN THE CODE READING THE DATA"

		if self.debug_mode:		
			st = str(datetime.datetime.now()) + ': Finished formating the input arrays.\nOpened ' + str(file_count) + ' files.\nSizes are: x_train=' + str(self.x_train.shape) +' y_train=' + str(self.y_train.shape) + ' x_test=' + str(self.x_test.shape) + ' y_test=' + str(self.y_test.shape)
			print(st)
			fp_logfile.write(st + '\n')
			print('DATA PREVIEW:\n')
			self.previewData()



	@staticmethod
	def write_it(x, y, fp, label):
		line = fp.readline()
		#assert(not not line, "ERROR")
		lineBuff = [np.uint16(s) for s in line.replace('.','|').split('|')]
		x.append(lineBuff)
		y.append(label)

	

	@staticmethod
	def getDataset(DataSetType):
		# DataSetType:	1: Legitimate + Ping Flood	
		#				2: Legitimate + SYN FLOOD
		#				3: Legitimate + UDP FLOOD
		#				4: Legitimate + PORTSCAN
		#				5: Legitimate + PORTSCAN + SYN FLOOD
		x_train = []
		y_train = []
		x_test = []
		y_test = []

		LegitFile = './nProbe/dumpedited/edited'
		PingAttFile = './nProbe/dumpedited/editedPINGATT'
		SYNATTFile = './nProbe/dumpedited/editedSYNATT'
		UDPATTFile = './nProbe/dumpedited/editedUDPATT'
		PortScanFile = './nProbe/dumpedited/editedPORTSC'
		
		if DataSetType == 0:
			fp_leg = open(LegitFile, 'r')
			fp_leg.readline() #read away the first line (title)
			fp_attPING = open(PingAttFile, 'r')
			fp_attPING.readline() #read away the first line (title)
			fp_attSYN = open(SYNATTFile, 'r')
			fp_attSYN.readline()
			fp_attUDP = open(UDPATTFile, 'r')
			fp_attUDP.readline()
			fp_attPORTSC = open(PortScanFile, 'r')
			fp_attPORTSC.readline()
			#Train Dataset: 10 legitimate and 10 attack samples, loop 3,000 times. 
			for i in range(3000):
				for j in range(random.choice([10,20,50,100])):
					Reader.write_it(x_train, y_train, fp_leg, 0)
				for j in range(random.choice([2,5,10,20])):
					Reader.write_it(x_train, y_train, fp_attPING, 1)
				for j in range(random.choice([2,5,10,20])):
					Reader.write_it(x_train, y_train, fp_attSYN, 2)
				for j in range(random.choice([2,5,10,20])):
					Reader.write_it(x_train, y_train, fp_attUDP, 3)
				for j in range(random.choice([2,5,10,20])):
					Reader.write_it(x_train, y_train, fp_attPORTSC, 4)
			#Test Dataset: 10 legitimate and 10 attack samples, loop 900 times.
			for i in range(900):
				for j in range(random.choice([10,20,50,100])):
					Reader.write_it(x_test, y_test, fp_leg, 0)
				for j in range(random.choice([2,5,10,20])):
					Reader.write_it(x_test, y_test, fp_attPING, 1)
				for j in range(random.choice([2,5,10,20])):
					Reader.write_it(x_test, y_test, fp_attSYN, 2)
				for j in range(random.choice([2,5,10,20])):
					Reader.write_it(x_test, y_test, fp_attUDP, 3)
				for j in range(random.choice([2,5,10,20])):
					Reader.write_it(x_test, y_test, fp_attPORTSC, 4)

		elif DataSetType == 1 or DataSetType == 2 or DataSetType == 3:
			fp_leg = open(LegitFile, 'r')
			fp_leg.readline() #read away the first line (title)
			fp_att = open(SYNATTFile, 'r')
			if DataSetType == 3:
				fp_att.close()
				fp_att = open(UDPATTFile, 'r')
			elif DataSetType == 1:
				fp_att.close()
				fp_att = open(PingAttFile, 'r')
			fp_att.readline() #read away the first line (title)
			#Train Dataset: 10 legitimate and 10 attack samples, loop 30,000 times. 
			#TOT 300,000 leg, 300,000 att.
			for i in range(3000):	############ CORRECTION: TOTAL 30,000 legitimate, 30,000 attack
				for j in range(10):
					Reader.write_it(x_train, y_train, fp_leg, 0)
				for j in range(10):
					Reader.write_it(x_train, y_train, fp_att, 1)
			#Test Dataset: 10 legitimate and 10 attack samples, loop 9000 times.
			#TOT 90,000 leg, 90,000 att			
			for i in range(9000):
				for j in range(10):
					Reader.write_it(x_test, y_test, fp_leg, 0)
				for j in range(10):
					Reader.write_it(x_test, y_test, fp_att, 1)

		elif DataSetType == 4:
			fp_leg = open(LegitFile, 'r')
			fp_leg.readline() #read away the first line (title)
			fp_att = open(PortScanFile, 'r')
			fp_att.readline() #read away the first line (title)
			#Train Dataset: 50 legitimate and 10 attack samples, loop 6000 times. 
			#TOT 300,000 leg, 60,000 att.
			for i in range(6000):
				for j in range(50):
					Reader.write_it(x_train, y_train, fp_leg, 0)
				for j in range(10):
					Reader.write_it(x_train, y_train, fp_att, 1)
			#Test Dataset: First 30000 leg. Then 1 legitimate and 10 attack samples, loop 2800 times. Then 30000 leg.
			#TOT 62,800 leg, 28,000 att		
			for i in range(30000):
				Reader.write_it(x_test, y_test, fp_leg, 0)
	
			for i in range(2800):
				for j in range(1):
					Reader.write_it(x_test, y_test, fp_leg, 0)
				for j in range(10):
					Reader.write_it(x_test, y_test, fp_att, 1)
			for i in range(30000):
				Reader.write_it(x_test, y_test, fp_leg, 0)

		elif DataSetType == 5:
			fp_leg = open(LegitFile, 'r')
			fp_leg.readline() #read away the first line (title)
			fp_attPORTSC = open(PortScanFile, 'r')
			fp_attPORTSC.readline() #read away the first line (title)
			fp_attSYN = open(SYNATTFile, 'r')
			fp_attSYN.readline() #read away the first line (title)
			#Train Dataset: 50 legitimate and 10 SYN attack and 10 PORSTC attack samples, loop 6000 times. 
			#TOT 300,000 leg, 60,000 SYN att, 60,000 PORTSC att.
			for i in range(6000):
				for j in range(50):
					Reader.write_it(x_train, y_train, fp_leg, 0)
				for j in range(10):
					Reader.write_it(x_train, y_train, fp_attSYN, 1) 
				for j in range(10):
					Reader.write_it(x_train, y_train, fp_attPORTSC, 2)
			#Test Dataset: First 30000 leg. Then 1 legitimate and 10 SYN attack and 10 PORTSC attack samples, loop 2800 times.
			#Then 30,000 SYN attack, then 30,000 leg.
			#TOT 62,800 leg, 58,000 SYN att, 28,000 PORTSC att		
			for i in range(30000):
				Reader.write_it(x_test, y_test, fp_leg, 0)
	
			for i in range(2800):
				for j in range(1):
					Reader.write_it(x_test, y_test, fp_leg, 0)
				for j in range(10):
					Reader.write_it(x_test, y_test, fp_attSYN, 1)
				for j in range(10):
					Reader.write_it(x_test, y_test, fp_attPORTSC, 2)
			for j in range(30000):
					Reader.write_it(x_test, y_test, fp_attSYN, 1)
			for i in range(30000):
				Reader.write_it(x_test, y_test, fp_leg, 0)
		
		elif DataSetType == 6: #Παραλλαγή του 2
			fp_leg = open(LegitFile, 'r')
			fp_leg.readline() #read away the first line (title)
			fp_att = open(SYNATTFile, 'r')
			fp_att.readline() #read away the first line (title)
			#Train Dataset:
			for i in range(10000):
				for j in range(random.choice([1,5,10,20])):
					Reader.write_it(x_train, y_train, fp_leg, 0)
				for j in range(random.choice([1,5,10,20])):
					Reader.write_it(x_train, y_train, fp_att, 1)
			#Test Dataset:
			for i in range(9000):
				for j in range(random.choice([1,5,10,20])):
					Reader.write_it(x_test, y_test, fp_leg, 0)
				for j in range(random.choice([1,5,10,20])):
					Reader.write_it(x_test, y_test, fp_att, 1)		



		x_train = np.array(x_train)
		y_train = np.array(y_train)
		x_test = np.array(x_test)
		y_test = np.array(y_test)

		x_trainNorm = Reader.Normalize(x_train)
		x_testNorm = Reader.Normalize(x_test)

		assert (x_train.shape[1] == x_test.shape[1]), "THERE WAS AN ERROR IN THE CODE READING THE DATA"
		assert (x_train.shape[0] == y_train.shape[0]), "THERE WAS AN ERROR IN THE CODE READING THE DATA"
		assert (x_test.shape[0] == y_test.shape[0]), "THERE WAS AN ERROR IN THE CODE READING THE DATA"
		st = 'Finished formating the input arrays. Sizes are: x_train=' + str(x_train.shape) +' y_train=' + str(y_train.shape) + ' x_test=' + str(x_test.shape) + ' y_test=' + str(y_test.shape)
		print(st)

		return (x_trainNorm, y_train),(x_testNorm, y_test)



	def previewData(self):				
		#st = ' y_train:' + str(self.y_train) + ' y_test:' + str(self.y_test)
		#print(st)
		print('x_train\n')
		for i in range(5):
			print('Sample ' + str(i) + ': ')
			list = [self.x_train[i,j] for j in range(self.x_train.shape[1])]
			print(list)
			list = [self.x_trainNorm[i,j] for j in range(self.x_trainNorm.shape[1])]
			print(list)
			print('y_train: ' + str(self.y_train[i]))


	def getData(self):
		return (self.x_train, self.y_train),(self.x_test, self.y_test)


	def getDataNormalized(self):
		return (self.x_trainNorm, self.y_train),(self.x_testNorm, self.y_test)


	def normalize(self, dataArray):
		minima = np.array(np.amin(dataArray, axis = 0))
		maxima = np.array(np.amax(dataArray, axis = 0))
		rang = maxima - minima
		rang[rang==0] = 1
		return (dataArray - minima) / rang

	@staticmethod
	def Normalize(dataArray):
		minima = np.array(np.amin(dataArray, axis = 0))
		maxima = np.array(np.amax(dataArray, axis = 0))
		rang = maxima - minima
		rang[rang==0] = 1
		return (dataArray - minima) / rang
	

	@staticmethod
	def getInputShape():
		length = 0
		rootDir='./nProbe/dumpedited'
		for dirName, subdirList, fileList in os.walk(rootDir):
			for fname in fileList:
				file_data = open(dirName + '/' + fname, 'r')
				line = file_data.readline()
				if not line: break
				line = file_data.readline()
				if not line: break
				length = len(line.replace('.','|').split('|'))
				break
		return length

