import hashlib
from typing import Dict, List, Tuple

def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

# v1 hashfiles, stable 
#def hash_files(file_data: List[Tuple[str, bytes]]) -> Dict[str, str]:
#return {name: hash_bytes(data) for name, data in file_data}

# v2 hashfiles, in testing
# pass listdirectly, alteration pending in call file
def hash_files(list_namebytes):
    return {name: hash_bytes(data) for name, data in list_namebytes}