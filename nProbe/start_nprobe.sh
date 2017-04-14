template="%IN_PKTS %OUT_PKTS %PROTOCOL %IPV4_SRC_ADDR %IPV4_DST_ADDR %L4_SRC_PORT %L4_DST_PORT %TCP_FLAGS %MIN_TTL %MAX_TTL %TCP_WIN_MIN_IN %TCP_WIN_MAX_IN %ICMP_TYPE %NUM_PKTS_UP_TO_128_BYTES %RETRANSMITTED_IN_PKTS %RETRANSMITTED_OUT_PKTS %FLOW_START_MILLISECONDS %FLOW_END_MILLISECONDS %SRC_AS %DST_AS"

active_timeout=30
idle_timeout=15
queue_timeout=15 #unused, default is 30

#pcap_list='/home/orestis/capture/adam/pcap_list'
input_option="$1"
dump_path=$2
filter="$3"

sudo nprobe -V 9 -t ${active_timeout} -d ${idle_timeout} --dump-path ${dump_path} ${input_option} -T "${template}" --dont-drop-privileges -f "${filter}"
