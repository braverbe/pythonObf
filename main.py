import os
import base64
from sys import argv
import re



# configuration
OFFSET = 10
VARIABLE_NAME = 'qwe' * 42


def bytecode_obfuscate(content):
    b64_content = base64.b64encode(content.encode()).decode()
    index = 0
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(b64_content) / OFFSET) + 1):
        _str = ''
        for char in b64_content[index:index + OFFSET]:
            byte = str(hex(ord(char)))[2:]
            if len(byte) < 2:
                byte = '0' + byte
            _str += '\\x' + str(byte)
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    old_code = code
    code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({VARIABLE_NAME}))'
    code += '\n'
    code += old_code
    return code

def add_fake_functions(content, myfile):
    with open(myfile, 'r', encoding='utf-8', errors='ignore') as file:
        file_content = file.read()
    with open(content, 'r', encoding='utf-8', errors='ignore') as file:
        file_content += '\n'
        file_content += file.read()
    return file_content



def changeFunctionNames(myFile):
    functionNames = []
    returnFile = ''
    KEY = 1
    with open(myFile, 'r', encoding='utf-8', errors='ignore') as file:
        file_content = file.readlines()

        for string in file_content:
            returnFile+=string
            if (string.find('def')!= -1):
                # print(string.split()[1][:-3])
                # print(string.split()[1].split('(')[0])
                functionNames.append(string.split()[1].split('(')[0])

#Замена названий функций
    for functionName in functionNames:
        for el in re.split('\n|\t| |:', returnFile):
            if functionName in el:

                # print(functionName, el)
                asd = el.find(functionName)
                # print(asd)
                # print(functionName[asd:])
                # print(functionName[:-1])
                el = functionName.replace(functionName[asd:], functionName[asd:]+"_edited")
                # print(functionName, el)
                # print('---')
                returnFile = returnFile.replace(functionName, el)
                # print(1)
                break;
    # print(returnFile)
        # returnFile.replace('test', 'asdasdasd')

    # print(returnFile)
    # with open(myFile, 'w', encoding='utf-8', errors='ignore') as file:
    #     file.write(returnFile)
    return returnFile

#Добавление мёртвого кода
def add_code(myFile):
    old_file_content = []
    new_file_content = []

    with open(myFile, 'r', encoding='utf-8', errors='ignore') as file:
        old_file_content = file.readlines()
    # print(old_file_content)

    dead_code_start = ['import random\n', 'import math\n', '\n', 'x = random.randint(0, 10)\n', '#print(x)\n', 'if(math.pow(math.sin(x),2)+math.pow(math.cos(x),2)>0.99):\n']
    dead_code_end = ['else:\n', '    print(math.pow(math.sin(x),2)+math.pow(math.cos(x),2))\n', '    print("cucumber")\n']
    for str in dead_code_start:
        new_file_content.append(str)

    for string in old_file_content:
        string = '    ' + string
        new_file_content.append(string)

    for str in dead_code_end:
        new_file_content.append(str)
    # print(new_file_content)
    return new_file_content

add_code('example.py')
def main():
    try:
        path = argv[0]
        if not os.path.exists(path):
            print('[-] File not found')
            exit()

        if not os.path.isfile(path) or not path.endswith('.py'):
            print('[-] Invalid file')
            exit()

        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            file_content = file.read()

        #TODO change variables and functions, write wrong comments, add fake code

        # changeFunctionNames('C:\\Users\\jackt\\PycharmProjects\\pythonObf\\example.py')


        file_content = add_fake_functions('concat_text.py', 'C:\\Users\\jackt\\PycharmProjects\\pythonObf\\example.py')
        # print(file_content)
        with open('example (obfuscated).py', 'w', encoding='utf-8', errors='ignore') as file:
            file.write(file_content)

        obfuscated_content = changeFunctionNames('C:\\Users\\jackt\\PycharmProjects\\pythonObf\\example (obfuscated).py')
        # obfuscated_content = add_fake_functions('concat_text.py', 'C:\\Users\\jackt\\PycharmProjects\\pythonObf\\example (obfuscated).py')

        file_content = add_code('example (obfuscated).py')
        #
        f = open("example (obfuscated).py", "w")
        f.truncate()
        f.close()
        #
        # with open('example (obfuscated).py', 'w', encoding='utf-8', errors='ignore') as file:
        #     for string in file_content:
        #         file.write(string)
        #
        # print(file_content)

        # obfuscating to byte code
        obfuscated_content = bytecode_obfuscate(obfuscated_content)

        with open(f'{path.split(".")[0]} (obfuscated).py', 'w') as file:
            file.write(obfuscated_content)

        print('[+] Script has been obfuscated')
    except:
        print(f'Usage: py {argv[0]} <file>')


if __name__ == '__main__':
    main()
