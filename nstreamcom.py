def parse(data):
    if isinstance(data, bytearray):
        if len(data) < 7:
            return None
        if len(data) != data[1] + 6:
            return None
        return ( int.from_bytes(data[2:4], 'little'), data[4: 4 + data[1]], data[1] )
    elif isinstance(data, tuple):
        byte_stream = bytearray()
        byte_stream.extend([ 1, data[2] ])
        byte_stream.extend(data[0].to_bytes(2, 'little'))
        byte_stream.extend(data[1])
        byte_stream.extend([ 13, 10 ])
        return byte_stream
    return None