import re


class Pseudocode:

    def build(self, verible_list, py_tree) -> str:
        return 'begin;\n\n' + '/' + ','.join(verible_list) + '/;\n\n' + self._py2pseudocode(py_tree) + '\nend;'
    
    def _py2pseudocode(self, py_tree) -> str:
        #add {} to bodies
        pseudocode = ''
        for i in py_tree:
            if type(i) == dict:
                key = self._get_dict_key_by_index(i)
                pseudocode += '\n' + self._get_c_styled(key) + '{\n' + self._py2pseudocode(i[key]) + '}' + '\n\n'
            else:
                pseudocode += self._get_c_styled(i) + '\n'

        return pseudocode

    def _get_c_styled(self, line) -> str:
        #clear type-changing operators, input, print 
        line = line.replace('*', '×')
        line = line.replace('/', '÷')
        line = re.sub('input ?\( ?.* ?\)', '', line)
        line = re.sub('print ?\( ?(.*) ?\)', '/ \g<1> /', line)
        line = re.sub('(int|float|str|bool|tuple|list|dict|set) ?\( ?(.*?) ?\)', '\g<2>', line) #IT MUST BE LAST!!!!
        
        
        #dont write line if it useless
        if '=' in line:
            sub_line = line[line.index('=')+1::]
            if sub_line.count(' ') == len(sub_line): return ''

        #escape special symbs
        spec_symb = re.findall(r'(\[|\]|\{|\})', line)
        for symb in spec_symb: line = line.replace(symb, '\\' + symb)


        #control structs to c-style
        if line[0:2] == 'if':
            return 'if(' + re.sub(r'if |\:', '', line) + ')'
        elif line[0:4] == 'else':
            return 'else'
        elif line[0:4] == 'elif':
            return 'else if(' + re.sub(r'elif |\:', '', line) + ')'
        elif line[0:3] == 'for':
            return 'while(' + re.sub(r'for |\:', '', line) + ')'
        elif line[0:5] == 'while':
            return 'while(' + re.sub(r'while |\:', '', line) + ')'
        elif line[0:3] == 'def':
            return 'function ' + re.sub(r'def |\:', '', line)
        else:
            if 'return ' in line:
                return line
            else:
                if line.strip() == '': return line
                else: return f'{line};\n'

    def _get_dict_key_by_index(self, dict, index = 0) -> str:
        return list(dict.keys())[index]