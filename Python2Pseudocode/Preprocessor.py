import re



class Preprocessor:
    CONVERT_MODS = { 'FUNCTIONAL_TO_PROCEDURAL': 1, 'NO_CONVERT' : 0 }

    def __init__(self, file , convert_mode) -> None:
        self._file = file
        self._parse()
        self._global_curent_pos = 0
        self._convert_mode = convert_mode
        
        if convert_mode == 1: self._functional_to_procedural()


    _parsed_code = []

    def get_serealized_code(self):
        return self._get_serealized_code(self._parsed_code)

    def _parse(self) -> None:
        for i in self._file:
            if i.strip() != '\n' and '#' not in i and i != '\n' and i !='': self._parsed_code.append(i)

    def _get_serealized_code(self, code):
        levels = []
        i = 0

        while i < len(code):
            item = code[i]

            if self._is_control_structure(item):
                end = self._find_end_of_body(code, i)
                levels.append({item.strip(): self._get_serealized_code(code[i+1:end+1])})
                i = end
            else:
                levels.append(item.strip())
            
            i+=1

        return levels
            
    
    def _find_end_of_body(self, code, position):
        last_level = self._get_level_of_line(code[position])
        end = position

        for i in code[position+1::]:
            if self._get_level_of_line(i) > last_level: end+=1
            else: break 

        return end
        
    def _get_body(self, pos):
        last_level = self._get_level_of_line(self._parsed_code[pos])
        body = []

        for i in self._parsed_code[1::]:
            if self._get_level_of_line(i) > last_level: body.append(i)
            else: break 
        
        return body

    def _get_level_of_line(self, line) -> int:
        return line.count('    ')

    def _increase_level_of_line(self, line, increase) -> str:
        level = self._get_level_of_line(line)
        return line.replace('    ' * level, '    ' * (level+increase))

    def find_all_veribles(self, code = []) -> list:
        if code == []: code = self._parsed_code
        m = []

        for str in code:
            if str.strip() != 'True' and str.strip() != 'False':
                m += re.findall(r'(\w+)\.? ?= ?', str)
                m += re.findall(r'for (\w+)\.?', str)
                m += re.findall(r'while (\w+)\.?', str)
                m += re.findall(r'for (\w+)', str)
                m += re.findall(r'in +(\w+)\.?',str)
                if '(' in str:
                    m += re.findall(r'[a-zA-Z_]+', str[str.index('(')+1:str.index(')')])

        if 'and' in m: m.remove('and')
        if 'len' in m: m.remove('len')
        return list(set(m))

    def _functional_to_procedural(self) -> None:
        functions = {}
        functions_args_names = {}

        #find all functions 
        for i in self._parsed_code:
            if 'def ' in i:
                name = self._get_function_name(i)
                body = self._get_body(self._parsed_code.index(i))
                
                #del body and fun struct
                self._parsed_code.remove(i)
                for j in body:
                    self._parsed_code.remove(j)
                
                #saving fun body and args, change ver names
                functions[name] = self._add_pref_to_ver(body, f'_{name}')
                functions_args_names[name] = self._get_fun_args(i)


        #add procedural implementation
        functions_names = list(functions.keys())

        for fun in functions_names:
            code_fragment = []
            for line in self._parsed_code:
                line_level = self._get_level_of_line(line)
                if fun in line:
                    line_args = self._get_fun_args(line, fun)
                    for arg in functions_args_names[fun]:
                        arg_index = functions_args_names[fun].index(arg)
                        code_fragment.append(f'{arg}_{fun} = {line_args[arg_index]}\n')
                    body = functions[fun]
                    for b in body:
                        cur_level = self._get_level_of_line(b)
                        paste_index = body.index(b)
                        if 'return ' in b: body[paste_index] = body[paste_index].replace('return ', f'result_{fun} =')
                        body[paste_index] = self._increase_level_of_line(body[paste_index], - 1  )
                    regex = re.compile( fun + '?\([a-zA-Z_0-9\,\'\[\]\{\}\. ]+\)')
                    code_fragment += body
                    code_fragment.append(re.sub(regex, f'result_{fun}', line))
                self._paste_in_parsed_code(self._parsed_code.index(line), code_fragment)
            
        
    
    def _add_pref_to_ver(self, code, pref):
        all_veribles = self.find_all_veribles(code)
        new_code = []
        
        for line in code:
            new_line = ''
            rg = r' |=|\-|\+|\*|\/|:|,|\(|\)|\.|\[|\]'
            count = 0
            splits = re.findall(rg, line)
            
            
            for sub_line in re.split(rg, line):
                sub_line = sub_line.replace('\n', '')

                for ver in all_veribles:
                    if ver == sub_line.strip() and not self._is_control_structure(sub_line):
                        if ':' in sub_line:
                            sub_line_without_spec_sym = sub_line.replace(':','')
                            new_line += sub_line_without_spec_sym.replace(sub_line_without_spec_sym, sub_line_without_spec_sym+pref+':')
                        if '(' in sub_line or ')' in sub_line or ',' in sub_line: continue
                        else:
                            new_line += sub_line.replace(sub_line, sub_line+pref)
                        break
                else: new_line += sub_line
                if count <= len(splits)-1: new_line += splits[count]
                count += 1

                
            new_code.append(new_line + '\n')
            
        
        return new_code

    def _paste_in_parsed_code(self, pos, l):
        self._parsed_code = self._parsed_code[0:pos] + l + self._parsed_code[pos+1::]


    def _get_function_name(self, line) -> str:
        line = re.sub(r'def |\:', '', line)
        output = ''
        for i in line:
            if i != '(': output+=i
            else: break
        
        return output

    def _get_fun_args(self, line, fun_name = '') -> list:
        line = line[line.index(f'{fun_name}(')+len(fun_name) + 1:line.index(')')] + ','
        args = []
        last_arg = ''
        for i in line:
            if i == ',' and len(last_arg) > 0:
                last_arg = last_arg.strip()
                if (last_arg.count('[') + last_arg.count(']'))  % 2 == 0 and (last_arg.count('{') + last_arg.count('}'))  % 2  == 0:
                    args.append(last_arg)
                    last_arg = ''
                else: last_arg+= i 
            else: last_arg+= i 
        return args



    def _is_control_structure(self, line) -> bool:
        line = line.strip()

        return line[0:2] == 'if' or line[0:3] == 'for' or line[0:5] == 'while' or line[0:4] == 'else' or line[0:3] == 'def'

    