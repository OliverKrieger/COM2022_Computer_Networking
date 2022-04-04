from urllib import request

# bytes allowed
request_size = 8
current_packet_size = 4
total_packet_size = 4

# total size
header_size = request_size + current_packet_size + total_packet_size

#########################################
# Requests
#########################################
# 1 = handshake - message contains buffer size
# 2 = response - message contains response
    # 21 = message response received
# 3 = request - message contains request value
    # 31 = givelist - gives a list of files user has


#########################################
# Funcions
#########################################
