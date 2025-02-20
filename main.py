import os
import logging

# 设置日志记录格式
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

root_dir = 'input'

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        file_to_open = str(
            'input\\'+file_path
            .replace(root_dir, '')
            .replace('\\', '')
        )
        file_to_save_to = str(
            'output\\'+file_path
            .replace(root_dir, '')
            .replace('\\', '')
            .replace('.java', '.proto')
            .replace('OuterClass', '')
        )
        dir_to_save_to = file_path.replace('input', 'output')
        with open(file_to_open) as f, open(file_to_save_to, 'w') as o:
            lines = f.readlines()
            stripped_lines = [line.lstrip() for line in lines]
            lines_set = set(stripped_lines)
            keys = ['uint32', 'uint64', 'string', 'int32', 'bool', 'bytes', 'double']
            shit = file_to_save_to.replace('.proto', '').replace('output\\', '')
            o.write(f'syntax = "proto3";\n\noption java_package = "emu.grasscutter.net.proto";\n\n')
            def doimport():
                try:
                    for line in lines_set:
                        if "<code>" in line:
                            if not any(key in line for key in keys):
                                someshit = (str(line)
                                    .replace('     * <code>', '')
                                    .replace('.', '')
                                    .replace('</code>', '')
                                    .replace('* <code>', '')
                                    .replace('&lt;', ' <')
                                    .replace('&gt;', '>')
                                    .replace(' = ', '')
                                    .replace(';', '')[:-1]
                                    .replace('0', '')
                                    .replace('1', '')
                                    .replace('2', '')
                                    .replace('3', '')
                                    .replace('4', '')
                                    .replace('5', '')
                                    .replace('6', '')
                                    .replace('7', '')
                                    .replace('8', '')
                                    .replace('9', '')
                                )
                                somewords = someshit.split()
                                second_word_from_right = somewords[-2]
                                o.write('import "'+second_word_from_right+'.proto";\n')
                except IndexError as e:
                    error_msg = f"索引错误：{e}\n"
                    error_msg += f"文件路径：{file_to_open}\n"
                    for i, line in enumerate(lines_set):
                        if '<code>' in line:
                            error_msg += f"出错行号：{i+1}\n"
                            error_msg += line + '\n'
                    logging.error(error_msg)
                
            doimport()
            o.write(f'\nmessage {shit} '+"{\n")
            for line in lines_set:
                if "<code>" in line:
                    o.write("  "+line
                        .replace('     * <code>', '')
                        .replace('.', '')
                        .replace('</code>', '')
                        .replace('* <code>', '')
                        .replace('&lt;', ' <')
                        .replace('&gt;', '>')
                    )
            o.write('}')
