from Preprocessor import *
from Pseudocode import *
import sys



def main():

    try:
        f = open(input('path: '), 'r', encoding='utf-8')
    except:
        exit('wrong path')

    try:
        if input('mode: ') == 'procedural': mode = Preprocessor.CONVERT_MODS['FUNCTIONAL_TO_PROCEDURAL']
        else: mode = Preprocessor.CONVERT_MODS['NO_CONVERT']
        
        
    except:
        mode = Preprocessor.CONVERT_MODS['NO_CONVERT']


    p = Preprocessor(f, mode)
    pscode = Pseudocode()

    serealized = p.get_serealized_code()
    build = pscode.build(p.find_all_veribles(), serealized)
    f.close()
	
    f = open('pseudocode.txt', 'w+', encoding='utf-8')
    f.write(build)
    f.close()
    print('Pseudocode has been written in', f'{sys.path[0]}/pseudocode.txt')


if __name__ == "__main__":
    main()
