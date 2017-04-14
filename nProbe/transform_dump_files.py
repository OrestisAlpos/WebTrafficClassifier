import os
import sys

debug = False
#outfile = open('./nProbe/dumpedited/edited','w')
outfile = open(sys.argv[2], 'w')

def write_tokens(tokens):
	outfile.write(tokens[0])
	for token in tokens[1:]:
		if token != '':
			outfile.write('|' + token)
	outfile.write('\n')


def getIndexes(line):
	tokens = line.split('|')
	for i in range(len(tokens)):
		if tokens[i] == 'PROTOCOL':
			protocol_idx = i
		if tokens[i] == 'IPV4_SRC_ADDR':
			srcip_idx = i
		if tokens[i] == 'IPV4_DST_ADDR':
			dstip_idx = i
		if tokens[i] == 'L4_SRC_PORT':
			srcport_idx = i
		if tokens[i] == 'L4_DST_PORT':
			dstport_idx = i
		if tokens[i] == 'TCP_FLAGS':
			tcpflags_idx = i
		if tokens[i] == 'ICMP_TYPE':
			icmptype_idx = i
		if tokens[i] == 'TCP_WIN_MIN_IN':
			tcpwin_min_idx = i
		if tokens[i] == 'TCP_WIN_MAX_IN':
			tcpwin_max_idx = i
		if tokens[i] == 'FLOW_START_MILLISECONDS':
			fswitched_idx = i
		if tokens[i] == 'FLOW_END_MILLISECONDS':
			lswitched_idx = i
		if tokens[i] == 'SRC_AS':
			srcas_idx = i
		if tokens[i] == 'DST_AS\n':
			dstas_idx = i

	return (protocol_idx, srcip_idx, dstip_idx, srcport_idx, dstport_idx, tcpflags_idx, icmptype_idx, tcpwin_min_idx, tcpwin_max_idx, fswitched_idx, lswitched_idx, srcas_idx, dstas_idx)



title_writen = False
#rootDir='./nProbe/dump'
rootDir=str(sys.argv[1])
for dirName, subdirList, fileList in os.walk(rootDir):
	for fname in fileList:
		file_data = open(dirName + '/' + fname, 'r')
		print(dirName + '/' + fname)
		line = file_data.readline()	#title line
		(protocol_idx, srcip_idx, dstip_idx, srcport_idx, dstport_idx, tcpflags_idx, icmptype_idx, tcpwin_min_idx, tcpwin_max_idx, fswitched_idx, lswitched_idx, srcas_idx, dstas_idx) = getIndexes(line)
		tokens = line.split('|')
		tokens[protocol_idx] = 'IS_TCP|IS_UDP|IS_ICMP|IS_ICMP6'
		tokens[srcip_idx] = ''
		tokens[dstip_idx] = ''
		tokens[srcport_idx] = 'SRCPORT17|SRCPORT18|SRCPORT_FTPDATA|SRCPORT_FTP|SRCPORT_SSH|SRCPORT_TELNET|SRCPORT24|SRCPORT_SMTP|SRCPORT35|SRCPORT42|SRCPORT_DNS|SRCPORT67|SRCPORT68|SRCPORT_TFTP|SRCPORT80|SRCPORT88|SRCPORT101|SRCPORT109|SRCPORT110|SRCPORT_SFTP|SRCPORT118|SRCPORT_NTP|SRCPORT156|SRCPORT_SNMP|SRCPORT_BGP|SRCPORT443|SRCPORT_RAND'
		tokens[dstport_idx] = 'DSTPORT17|DSTPORT18|DSTPORT_FTPDATA|DSTPORT_FTP|DSTPORT_SSH|DSTPORT_TELNET|DSTPORT24|DSTPORT_SMTP|DSTPORT35|DSTPORT42|DSTPORT_DNS|DSTPORT67|DSTPORT68|DSTPORT_TFTP|DSTPORT80|DSTPORT88|DSTPORT101|DSTPORT109|DSTPORT110|DSTPORT_SFTP|DSTPORT118|DSTPORT_NTP|DSTPORT156|DSTPORT_SNMP|DSTPORT_BGP|DSTPORT443|DSTPORT_RAND'
		tokens[tcpflags_idx] = 'SYN|ACK|PSH|URG|FIN|RST'
		tokens[icmptype_idx] = 'ICMP_TYPE0|ICMP_TYPE3|ICMP_TYPE5|ICMP_TYPE8|ICMP_TYPE11'
		tokens[fswitched_idx] = 'DURATION'
		tokens[lswitched_idx] = ''
		tokens[tcpwin_min_idx] = ''
		tokens[tcpwin_max_idx] = ''		
		tokens[dstas_idx] = 'DST_AS'
		if debug:
			print(tokens)
		if not title_writen:
			write_tokens(tokens)
			title_writen = True

		while True:
			line = file_data.readline()
			if not line:
				break
			tokens = line.split('|')
			tokens[protocol_idx] = str(int(tokens[protocol_idx]=='6')) +'|'+ str(int(tokens[protocol_idx]=='17')) +'|'+ str(int(tokens[protocol_idx]=='1')) +'|'+ str(int(tokens[protocol_idx]=='58')) 
			tokens[srcip_idx] = ''
			tokens[dstip_idx] = ''
			tokens[srcport_idx] = str(int(tokens[srcport_idx]=='17')) +'|'+ str(int(tokens[srcport_idx]=='18')) +'|'+ str(int(tokens[srcport_idx]=='20')) +'|'+ str(int(tokens[srcport_idx]=='21')) +'|'+ str(int(tokens[srcport_idx]=='22')) +'|'+ str(int(tokens[srcport_idx]=='23')) +'|'+ str(int(tokens[srcport_idx]=='24')) +'|'+ str(int(tokens[srcport_idx]=='25')) +'|'+ str(int(tokens[srcport_idx]=='35')) +'|'+ str(int(tokens[srcport_idx]=='42')) +'|'+ str(int(tokens[srcport_idx]=='53')) +'|'+ str(int(tokens[srcport_idx]=='67')) +'|'+ str(int(tokens[srcport_idx]=='68')) +'|'+ str(int(tokens[srcport_idx]=='69')) +'|'+ str(int(tokens[srcport_idx]=='80')) +'|'+ str(int(tokens[srcport_idx]=='88')) +'|'+ str(int(tokens[srcport_idx]=='101')) +'|'+ str(int(tokens[srcport_idx]=='109')) +'|'+ str(int(tokens[srcport_idx]=='110')) +'|'+ str(int(tokens[srcport_idx]=='115')) +'|'+ str(int(tokens[srcport_idx]=='118')) +'|'+ str(int(tokens[srcport_idx]=='123')) +'|'+ str(int(tokens[srcport_idx]=='156')) +'|'+ str(int(tokens[srcport_idx]=='161')) +'|'+ str(int(tokens[srcport_idx]=='179')) +'|'+ str(int(tokens[srcport_idx]=='443')) +'|'+ str(int(int(tokens[srcport_idx]) > 1023))
			tokens[dstport_idx] = str(int(tokens[dstport_idx]=='17')) +'|'+ str(int(tokens[dstport_idx]=='18')) +'|'+ str(int(tokens[dstport_idx]=='20')) +'|'+ str(int(tokens[dstport_idx]=='21')) +'|'+ str(int(tokens[dstport_idx]=='22')) +'|'+ str(int(tokens[dstport_idx]=='23')) +'|'+ str(int(tokens[dstport_idx]=='24')) +'|'+ str(int(tokens[dstport_idx]=='25')) +'|'+ str(int(tokens[dstport_idx]=='35')) +'|'+ str(int(tokens[dstport_idx]=='42')) +'|'+ str(int(tokens[dstport_idx]=='53')) +'|'+ str(int(tokens[dstport_idx]=='67')) +'|'+ str(int(tokens[dstport_idx]=='68')) +'|'+ str(int(tokens[dstport_idx]=='69')) +'|'+ str(int(tokens[dstport_idx]=='80')) +'|'+ str(int(tokens[dstport_idx]=='88')) +'|'+ str(int(tokens[dstport_idx]=='101')) +'|'+ str(int(tokens[dstport_idx]=='109')) +'|'+ str(int(tokens[dstport_idx]=='110')) +'|'+ str(int(tokens[dstport_idx]=='115')) +'|'+ str(int(tokens[dstport_idx]=='118')) +'|'+ str(int(tokens[dstport_idx]=='123')) +'|'+ str(int(tokens[dstport_idx]=='156')) +'|'+ str(int(tokens[dstport_idx]=='161')) +'|'+ str(int(tokens[dstport_idx]=='179')) +'|'+ str(int(tokens[dstport_idx]=='443')) +'|'+ str(int(int(tokens[dstport_idx]) > 1023))
			tokens[tcpflags_idx] = str(int(int(tokens[tcpflags_idx])&0b000010==2)) +'|'+ str(int(int(tokens[tcpflags_idx])&0b010000==16)) +'|'+ str(int(int(tokens[tcpflags_idx])&0b001000==8)) +'|'+ str(int(int(tokens[tcpflags_idx])&0b100000==32)) +'|'+ str(int(int(tokens[tcpflags_idx])&0b000001==1)) +'|'+ str(int(int(tokens[tcpflags_idx])&0b000100==4))
			icmp_type = (int(tokens[icmptype_idx]) & 0xff00) // 256
			tokens[icmptype_idx] = str(int(icmp_type==0) & int(tokens[protocol_idx]=='1')) +'|'+ str(int(icmp_type==3)) +'|'+ str(int(icmp_type==5)) +'|'+ str(int(icmp_type==8)) +'|'+ str(int(icmp_type==11))
			tokens[fswitched_idx] = str(int(tokens[lswitched_idx]) - int(tokens[fswitched_idx]))
			tokens[lswitched_idx] = ''
			tokens[tcpwin_min_idx] = ''
			tokens[tcpwin_max_idx] = ''		
			tokens[srcas_idx] = str(int(tokens[srcas_idx]=='3323'))
			tokens[dstas_idx] = str(int(tokens[dstas_idx]=='3323\n'))
			if debug:			
				print(tokens)
				input("")
			write_tokens(tokens)

outfile.close()
