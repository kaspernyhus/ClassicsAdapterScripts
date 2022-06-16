def parse_log_data(data_raw):
    # print(data_raw)
    # print("Data packet length:", len(data_raw)-1)

    if len(data_raw) < 2:
        print("ERROR: packet length < 2")
        return 0
    if data_raw[0] != 0xA5:
        print("ERROR: Start byte NOT detected")
        return 0
    if len(data_raw)-1 != data_raw[1]:
        print("ERROR: data missing", len(data_raw)-1, "/", data_raw[1])
        return 0

    else:
        index = 2

        log_type_raw = data_raw[index]
        log_type = "ID" if log_type_raw == 0 else "Data"
        index += 1
        # print("log_type:", log_type)

        log_id = data_raw[index]
        index += 1
        # print("log_id:", log_id)

        timestamp_raw = data_raw[index:index+4]
        timestamp = int.from_bytes(timestamp_raw, "little")
        index += 4
        # print("Timestamp:", timestamp)

        data_len = data_raw[index]
        index += 1
        # print("data_len:", data_len)

        data = data_raw[index:index+data_len]
        # for byte in data:
        #     print(hex(byte))

        if log_type == 'Data':
            data = int.from_bytes(data, "little")
            # print("data:", data)
        elif log_type == 'ID':
            data = data.decode()[:-1]
            # print("data:", data)
        else:
            data = "Log type error"

        return {'id': log_id, 'type': log_type, 'timestamp': timestamp, 'data': data}


def get_data(parsed_data):
    if parsed_data['type'] == "Data":
        return {'timestamp': parsed_data['timestamp'], 'data': parsed_data['data']}
