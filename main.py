import general_functions as gf


buzzwords_file = 'data/2020年网络用语.txt'
base_positive_file = 'data/正向情感基准词.txt'
base_negative_file = 'data/负向情感基准词.txt'
weibo_file = 'data/weibo_text.txt'

if __name__ == '__main__':

    buzzwords = gf.get_txt_contents(buzzwords_file)
    base_positive_words = gf.get_txt_contents(base_positive_file)
    base_negative_words = gf.get_txt_contents(base_negative_file)
    weibo_texts = gf.get_txt_contents(weibo_file)

    so_pmi = gf.calculate_SO_PMI(buzzwords, base_positive_words, base_negative_words, weibo_texts)

    pos_list, neg_list, neu_list = gf.judgement(so_pmi)

    gf.print_words(pos_list, 0)
    gf.print_words(neg_list, 1)
    gf.print_words(neu_list, 2)
