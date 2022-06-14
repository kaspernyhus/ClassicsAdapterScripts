def parse_log_data(data_raw):
    if data_raw[0] != 0xA5:
        print("ERROR: Start byte NOT detected")
        return -1
    else:
        index = 1
        total_len = data_raw[index]
        index += 1
        # print("total_len:", total_len)
        log_id = data_raw[index]
        index += 1
        log_tag_length = data_raw[index]
        index += 1
        # print("log_tag_length:", log_tag_length)
        log_tag = data_raw[index:index+log_tag_length-1]
        tag = log_tag.decode()
        index += log_tag_length
        # print("Log ID:", log_id)
        # print("Log tag:", log_tag.decode())
        timestamp = data_raw[index:index+4]
        timestamp = int.from_bytes(timestamp, "little")
        # print("Timestamp:", timestamp)
        index += 4
        data_len = data_raw[index]
        index += 1
        # print("data_len:", data_len)
        data = data_raw[index:index+data_len]
        # for byte in data:
        #     print(hex(byte))
        data = int.from_bytes(data, "little")
        # print("data:", data)

        return {'id': log_id, 'tag': tag, 'timestamp': timestamp, 'data': data}