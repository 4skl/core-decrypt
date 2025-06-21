import sys, os.path, struct, binascii

def hex_padding(s, length):
    if len(s) % length != 0:
        r = (length) - (len(s) % length)
        s = "0" * r + s

    return s


def read_encrypted_key(wallet_filename):
	# Read wallet file directly without Berkeley DB dependency
	with open(wallet_filename, "rb") as wallet_file:
		wallet_file.seek(12)
		if wallet_file.read(8) != b"\x62\x31\x05\x00\x09\x00\x00\x00":  # BDB magic, Btree v9
			print(prog+": ERROR: file is not a Bitcoin Core wallet")
			sys.exit(1)
		
		# Reset to beginning and read entire file
		wallet_file.seek(0)
		wallet_data = wallet_file.read()
		
		# Search for the mkey entry in the wallet data
		mkey_pattern = b"\x04mkey\x01\x00\x00\x00"
		mkey_pos = wallet_data.find(mkey_pattern)
		
		if mkey_pos == -1:
			raise ValueError("Encrypted master key not found in the Bitcoin Core wallet file")
		
		# Skip the key pattern
		data_start = mkey_pos + len(mkey_pattern)
		
		# Try to extract the complete mkey structure
		# Look for enough data to contain: encrypted_key + salt + method + iter_count
		remaining_data = wallet_data[data_start:]
		
		# The wallet format can vary, let's try to find the right structure
		# We need at least 48 + 8 + 4 + 4 = 64 bytes for the complete structure
		if len(remaining_data) < 70:
			raise ValueError("Not enough data after mkey pattern")
				# Try manual extraction instead of struct unpacking
		# Based on the 49-byte data we found
		data_start = mkey_pos + len(mkey_pattern) + 3  # skip pattern + length + format bytes
		mkey_data = wallet_data[data_start:data_start + 49]
		
		if len(mkey_data) != 49:
			raise ValueError("Could not extract 49 bytes of mkey data")
		
		# Extract components manually
		# First 48 bytes contain the encrypted master key (including IV)
		encrypted_master_key = mkey_data[:48]
		
		# Try to find salt and iteration count in nearby data
		# Look after the mkey data for additional fields
		extra_data_start = data_start + 49
		extra_data = wallet_data[extra_data_start:extra_data_start + 16]
		
		# Default values in case we can't find them
		salt = b"\x00" * 8
		method = 0
		iter_count = 10000
		
		# Try to extract salt and iteration count from extra data
		if len(extra_data) >= 12:
			salt = extra_data[:8]
			method, iter_count = struct.unpack("<II", extra_data[8:16])
		elif len(extra_data) >= 8:
			salt = extra_data[:8]		
	if method != 0:
		print(prog+": warning: unexpected Bitcoin Core key derivation method ", str(method))

	iv = binascii.hexlify(encrypted_master_key[16:32])
	ct = binascii.hexlify(encrypted_master_key[-16:])
	iterations = hex_padding('{:x}'.format(iter_count), 8).encode('ascii')

	s = iv + ct + binascii.hexlify(salt) + iterations
	
	return s

######### main

prog = os.path.basename(sys.argv[0])

if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
    print("usage: walletinfo.py WALLET_FILE")
    sys.exit(2)


wallet_filename = os.path.abspath(sys.argv[1])
encrypted_key = read_encrypted_key(wallet_filename)
print(encrypted_key)

    
