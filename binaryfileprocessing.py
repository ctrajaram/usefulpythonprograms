import struct as s


def read_process_binary_file(binary_file_name):
    """
        Reads and processes a binary file according to a specific file structure.

        The binary file is expected to have a header that includes a 4 byte string ABCD,
        1 byte version, and a 4-byte integer indicating the number of records.

        Each record is expected to have a byte indicating the record type, a 4-byte
        Unix timestamp, an 8-byte user ID, and for certain record types namely cash or check, an 8-byte
        floating point number representing cash or check amount.

        This function reads the file, interprets the bytes according to this structure,
        and calculates total cash and check amounts. It also calculates the balance (checks - cashs)
        for a given user id

        Args:
            binary_file_name (str): The name of the binary file to be read and processed.

        Returns:
            total check amount: NNNN.NN
            total cash amount: NNNNN.NN
            pay started N
            pay ended N
            balance for user 123456789=N.N
    """
    user_id_to_find_check = 0.0
    user_id_to_find_cash = 0.0
    user_id_to_find_balance = 2456938384156277127
    cash_total = 0.0
    check_total = 0.0
    autopay_started = 0
    autopay_ended = 0
    with open(binary_file_name, 'rb') as f:  # opening the binary file in read mode
        binary = f.read(4)  # read and unpack the magic string as binary string
        string = binary.decode('utf-8')  # Change the binary string to UTF-8 format for string comparisons
        s.unpack('>B', f.read(1))[0]  # unpack the version
        num_records = s.unpack('>I', f.read(4))[0]  # read and unpack the number of records 'I' stands for unsigned int (uint32), 4 bytes
        if string == 'ABCD':  # Validating the magic string to ensure we are parsing the correct file format
            for _ in range(num_records):
                # read and unpack the record type [0] is used to read the first element from a one element tuple from unpack
                record_type = s.unpack('>B', f.read(1))[0]
                # read and unpack the Unix timestamp
                timestamp = s.unpack('>I', f.read(4))[0]
                # read and unpack the user ID
                user_id = s.unpack('>Q', f.read(8))[0]  # 'Q' stands for uint64 8 bytes
                # read and unpack the cost and keep track of total check or total cash if record type is cash or check and if autopay then keep track of startautopay and endautopay
                if record_type == 0x03:  # cash
                    cost = s.unpack('>d', f.read(8))[0]
                    cash_total += cost
                    if user_id == user_id_to_find_balance:  # obtaining the total check amount for user id 2456938384156277127
                        user_id_to_find_cash += cost
                elif record_type == 0x04:  # check
                    cost = s.unpack('>d', f.read(8))[0]
                    check_total += cost
                    if user_id == user_id_to_find_balance:
                        user_id_to_find_check += cost  # obtaining the total cash amount for user id 2456938384156277127
                elif record_type == 0x05:  # pay started
                    autopay_started += 1
                elif record_type == 0x06:  # pay ended
                    autopay_ended += 1
    print(f"total check amount: {check_total:.2f}")
    print(f"total cash amount: {cash_total:.2f}")
    print(f'pay started {autopay_started}')
    print(f'pay ended {autopay_ended}')
    print(f'balance for user {user_id_to_find_balance}={user_id_to_find_check - user_id_to_find_cash}')


# Call the function passing the file
read_process_binary_file('binaryfile.dat')
