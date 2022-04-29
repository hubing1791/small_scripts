# 把完整md切割分到每个小problem.md里
import os
import re

paths = [

]

md_paths = [
]


# 寻找题目对应的完整路径
def find_file(num_str: str):
    if num_str == '':
        return ''
    for path in paths:
        path_1_list = os.listdir(path)
        for path_1 in path_1_list:
            if re.match(num_str, path_1):
                file_path = path + '/' + path_1 + "/problem.md"
                return file_path
    return ''


# 切分并写入
def split_md():
    for md_path in md_paths:
        need_write = []
        md_article = open(md_path, 'r', encoding='utf-8')
        for line in md_article.readlines():
            # print(line)
            need_write.append(line)
            # 两个三级标题之间就对应一个题解
            if line[:3] == '###':
                str_in_num = need_write[0]
                num_str = re.findall(r'(\d+)', str_in_num)

                # 三级标题后未必都是题目，还是要进一步判断
                if num_str:
                    num_str = num_str[0]
                    full_path = find_file(num_str)
                    if full_path != '':
                        write_handle = open(full_path, 'w', encoding='utf-8')
                        for need_line in need_write[:-1]:
                            write_handle.write(need_line)
                        write_handle.close()
                # 重置下需要写入的内容
                need_write = [line]


if __name__ == '__main__':
    split_md()
    # print(find_file('21'))
