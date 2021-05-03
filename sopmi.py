import re
from math import log


def get_probability(word_list, weibo_list):
    """
    获得概率, P(word)

    :param word_list: 词语列表(包括流行词语, 正向情感基准词, 负向情感基准词)
    :param weibo_list: 微博列表
    :return p_word_dict: 词语与概率构成的词典, {word: probability}
    """
    p_word_dict = {}
    length = len(weibo_list)
    for word in word_list:
        count = 0
        for weibo in weibo_list:
            if re.search(word, weibo):
                count += 1
        p_word_dict[word] = count / length

    return p_word_dict


def get_joint_probability(buzzwords, base_word_list, weibo_list):
    """
    获得联合概率, P(buzzword, baseword)

    :param buzzwords: 流行语列表
    :param base_word_list: 基准词列表
    :param weibo_list: 微博列表
    :return jp_word: 联合概率词典, {buzzword: {baseword: probability}}
    """
    jp_word = {}
    length = len(weibo_list)
    for buzzword in buzzwords:
        jp_word[buzzword] = {}
        for base_word in base_word_list:
            count = 0
            for weibo in weibo_list:
                if re.search(buzzword, weibo) and re.search(base_word, weibo):
                    count += 1

            jp_word[buzzword][base_word] = count / length

    return jp_word


def get_so_pmi(p_buzzwords, p_base_positive, p_base_negative, jp_buzzword_pos, jp_buzzword_neg):
    """
    计算so-pmi值

    :param p_buzzwords: 流行词出现概率的字典
    :param p_base_positive: 正向基准词出现概率的字典
    :param p_base_negative: 负向基准词出现概率的字典
    :param jp_buzzword_pos: 流行语与正向基准词的联合概率字典
    :param jp_buzzword_neg: 流行语与负向基准词的联合概率字典
    :return so_pmi: so-pmi值, {buzzword: so-pmi}
    """
    # {buzzword: so-pmi}
    so_pmi = {}
    for buzzword in p_buzzwords.keys():
        pos_pmi = 0
        neg_pmi = 0

        # 加1平滑
        for pos in p_base_positive.keys():
            pos_pmi += log((jp_buzzword_pos[buzzword][pos] + 1) /
                           (p_base_positive[pos] * p_buzzwords[buzzword] + 1), 2)

        for neg in p_base_negative.keys():
            neg_pmi += log((jp_buzzword_neg[buzzword][neg] + 1) /
                           (p_base_negative[neg] * p_buzzwords[buzzword] + 1), 2)

        so_pmi[buzzword] = pos_pmi - neg_pmi

    return so_pmi
