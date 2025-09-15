from pathlib import Path
import zwoasi
library_path = Path(__file__).parent.parent / '_system_data' / 'ASICamera2' / 'ASICamera2.dll'
print('Initialising with files at ' + str(library_path.resolve()))
try:
    zwoasi.init(str(library_path.resolve()))
except zwoasi.ZWO_Error as e:
    if not str(e) == 'Library already initialized':
        raise
print('Library initialised, checking if identity is available')