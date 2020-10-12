import sopmi

type_list = ["正向", "负向", "中性"]


def get_txt_contents(file_name):
    """
    获取txt内容, 并转换为列表

    :param file_name: txt文件
    :return contents_list: 文件的内容的列表
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        contents = f.read()
        contents_list = contents.split('\n')

    return contents_list


def calculate_SO_PMI(buzzwords, base_positive_words, base_negative_words, weibo_texts):
    """
    计算SO-PMI的中间调用的方法

    :param buzzwords: 流行语列表
    :param base_positive_words: 正向基准词列表
    :param base_negative_words: 负向基准词列表
    :param weibo_texts: 微博列表
    :return so_pmi: so-pmi值
    """
    # {word: probability}
    p_buzzwords = sopmi.get_probability(buzzwords, weibo_texts)
    print("P(buzzword)计算完毕")

    p_base_positive = sopmi.get_probability(base_positive_words, weibo_texts)
    print("P(pos_word)计算完毕")

    p_base_negative = sopmi.get_probability(base_negative_words, weibo_texts)
    print("P(neg_word)计算完毕")

    # print(p_buzzwords)
    # print(p_base_positive)
    # print(p_base_negative)
    print("开始计算联合概率")

    # {buzzword: {base_word: probability}}
    jp_buzzword_pos = sopmi.get_joint_probability(buzzwords, base_positive_words, weibo_texts)
    print("P(buzzword, Pword)计算完毕")

    jp_buzzword_neg = sopmi.get_joint_probability(buzzwords, base_negative_words, weibo_texts)
    print("P(buzzword, Nword)计算完毕")

    # print(jp_buzzword_pos)
    # print(jp_buzzword_neg)
    print("开始计算SO-PMI")

    so_pmi = sopmi.get_so_pmi(p_buzzwords, p_base_positive, p_base_negative, jp_buzzword_pos, jp_buzzword_neg)
    print("SO-PMI计算完毕\n")

    return so_pmi


def judgement(so_pmi):
    """
    判断词语情感极性

    :param so_pmi: so-pmi值
    :return pos_list: 正向流行词列表
    :return neg_list: 负向流行词列表
    :return neu_list: 中性流行词列表
    """
    pos_list = []
    neg_list = []
    neu_list = []
    for buzzword in so_pmi.keys():
        if so_pmi[buzzword] > 0:
            pos_list.append(buzzword)
        elif so_pmi[buzzword] == 0:
            neu_list.append(buzzword)
        else:
            neg_list.append(buzzword)

    return pos_list, neg_list, neu_list


def print_words(words_list, type):
    """
    打印词典

    :param words_list: 词语列表
    :param type: 词语类型, 0: 正向; 1: 负向; 2: 中性
    :return:
    """
    if not words_list:
        print("没有识别出{0}流行语".format(type_list[type]))
        print()
    else:
        print("{0}流行语有:".format(type_list[type]))
        for word in words_list:
            print(word, end=', ')

        print("\n")
