from Python2Pseudocode.Preprocessor import *
from Python2Pseudocode.Pseudocode import *
import pyperclip as clipboard
import sys



def main():
    args = sys.argv[1::]

    try:
        f = open(args[0], 'r', encoding='utf-8')
    except:
        exit('wrong path')

    try:
        if args[1] == 'procedural': mode = Preprocessor.CONVERT_MODS['FUNCTIONAL_TO_PROCEDURAL']
        else: mode = Preprocessor.CONVERT_MODS['NO_CONVERT']
        
        
    except:
        mode = Preprocessor.CONVERT_MODS['NO_CONVERT']


    p = Preprocessor(f, mode)
    pscode = Pseudocode()

    serealized = p.get_serealized_code()
    clipboard.copy(pscode.build(p.find_all_veribles(), serealized))
    f.close()
    print('Pseudocode has been copied')


if __name__ == "__main__":
    main()
