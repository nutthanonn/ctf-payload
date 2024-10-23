import codecs
import base64
import argparse

def rot13(s):
    return codecs.encode(s, 'rot_13')

def rot47(s):
    return codecs.encode(s, 'rot_47')

def base16_decode(s):
    return base64.b16decode(s)

def base32_decode(s):
    return base64.b32decode(s)

def base64_decode(s):
    return base64.b64decode(s)

def base85_decode(s):   
    return base64.b85decode(s)

def oct_decode(s):
    return bytes.fromhex(oct(int(s, 8))[2:]).decode('utf-8')

def hex_decode(s):
    return bytes.fromhex(s).decode('utf-8')

def reverse(s):
    return s[::-1]

algorithm = {
    'base16': base16_decode,
    'base32': base32_decode,
    'base64': base64_decode,
    'base85': base85_decode,
    'oct': oct_decode,
    'hex': hex_decode,
    
    'reverse': reverse,
    'rot13': rot13,
    'rot47': rot47
}

memo = {}
all_path = []

def dynamic_recursive(s, path='', prev_algo=''):
    global all_path
    
    if s in memo:
        return memo[s]
    
    for key, value in algorithm.items():
        if prev_algo == key and key in ['rot13', 'rot47', 'reverse']:
            continue
        
        try:
            decoded = value(s)
            if isinstance(decoded, bytes):
                decoded = decoded.decode('utf-8')
            new_path = f"{path} -> {key}"
            
            if prefix in decoded:
                all_path.append(new_path)
                print(f"Found: {decoded}")
                return decoded
            
            dynamic_recursive(decoded, new_path, key)
            memo[s] = decoded
        except:
            pass
    
    return s


arg = argparse.ArgumentParser()
arg.add_argument("-c", "--cipher", required=True)
arg.add_argument("-p", "--prefix", required=True)

cipher = arg.parse_args().cipher
prefix = arg.parse_args().prefix

if __name__ == '__main__':
    dynamic_recursive(cipher)
    print("Path: ", min(all_path, key=len))