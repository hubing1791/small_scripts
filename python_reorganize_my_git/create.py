# 之前用来创建文件的脚本，整理库格式的时候用了下
# 也许之后还用得上
import os

paths = [
]
for path in paths:
    path_1_lists = os.listdir(path)
    for path_1_list in path_1_lists:
        path_2 = path + '/' + path_1_list
        path_2_lists = os.listdir(path_2)
        if "problem.md" not in path_2_lists:
            f = open(path_2 + '/problem.md', "a+",encoding='utf-8')
            f.write("### 正在重新整理排版刷题记录，目前这个目录下problem.md还没更新，需要看的话内容在博客，本人git库就有，或者访问www.notyou.top")
