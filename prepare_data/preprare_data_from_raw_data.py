import random

def insert_random_strings_between_spaces(main_string, insert_strings):
    # Tách chuỗi A thành các từ dựa trên dấu cách và gán nhãn là 'original' cho từng từ
    words = [(word, 'original') for word in main_string.split()]
    
    # Chọn số lượng chuỗi sẽ được chèn ngẫu nhiên (từ 1 đến 3)
    num_inserts = random.randint(1, 4)
    # Chọn ngẫu nhiên các chuỗi sẽ được chèn từ danh sách B
    strings_to_insert = random.sample(insert_strings, num_inserts)
    
    for insert_str in strings_to_insert:
        # Tách chuỗi insert_str thành các từ riêng biệt
        insert_words = insert_str.split()
        # Chọn vị trí ngẫu nhiên để chèn chuỗi
        position = random.randint(0, len(words))
        # Chèn từng từ của chuỗi vào vị trí đã chọn và gán nhãn là 'inserted' cho từng từ được thêm vào
        for word in insert_words:
            words.insert(position, (word, 'inserted'))
            position += 1
    
    # Gộp các từ và chuỗi chèn lại thành một chuỗi hoàn chỉnh
    new_string = ' '.join(word[0] for word in words)
    return new_string, words

def clean_up_spaces(main_string):
    # Loại bỏ các dấu cách thừa
    return ' '.join(main_string.split())


def prepare_sentences_and_sub_strings(data):
    sub_strings = []
    sentences = data.split('.')
    for s in sentences:
        for ss in s.split(','):
            if len(ss) < 2:
                continue
            if len(ss) > MAX_SS_LEN:
                list_ss = ss.split(' ')
                sub_strings.append(" ".join(list_ss[:len(list_ss)//2]))
                sub_strings.append(" ".join(list_ss[len(list_ss)//2:]))
            else:
                sub_strings.append(ss)
    return sentences, sub_strings

with open('english_raw_remove_link.txt','r',encoding="utf-8") as f_in_e:
    en_data = f_in_e.read()
    en_data= en_data.replace('-',' ')
    en_data.replace('\n',' ')
    en_data = clean_up_spaces(en_data)
with open('vietnamese_raw.txt','r',encoding="utf-8") as f_in_v:
    vi_data = f_in_v.read()
    vi_data = vi_data.replace('-',' ')
    vi_data = vi_data.replace('\n',' ')
    vi_data = clean_up_spaces(vi_data)

# bỏ số 
for c in "0123456789":
    en_data = en_data.replace(c, '')

# loại bỏ kí tự lạ
for c in "$%&\"()*+–—/;[]‘“”…{|}·<>_~©ª;¯´»½п¿\^`=@":
    en_data = en_data.replace(c, '')
    vi_data = vi_data.replace(c, '')

# loại bỏ kí tự lạ
for c in "?!:#":
    en_data = en_data.replace(c, '.')
    vi_data = vi_data.replace(c, '.')

alphabet = list(en_data)
alphabet.extend(list(vi_data))
alphabet = list(set(alphabet))
alphabet.sort()
print("".join(alphabet))




MAX_SS_LEN = 20

# print(prepare_sentences_and_sub_strings("xin chào các bạn, mình là trần cao sơn. mình đang test cái củ lìn này. Hy vọng rằng, mọi thứ đéo lỗi."))

SAMPLE_SIZE = 100000

# def insert_random_strings_between_spaces(main_string, insert_strings):
#     # Tách chuỗi A thành các từ dựa trên dấu cách
#     words = main_string.split(' ')
    
#     # Chọn số lượng chuỗi sẽ được chèn ngẫu nhiên (từ 1 đến 3)
#     num_inserts = random.randint(1, 3)
#     # Chọn ngẫu nhiên các chuỗi sẽ được chèn từ danh sách B
#     strings_to_insert = random.sample(insert_strings, num_inserts)
    
#     for insert_str in strings_to_insert:
#         # Chọn vị trí ngẫu nhiên để chèn chuỗi
#         position = random.randint(0, len(words) - 1)
#         # Chèn chuỗi vào vị trí đã chọn
#         words.insert(position + 1, insert_str)
    
#     # Gộp các từ và chuỗi chèn lại thành một chuỗi hoàn chỉnh
#     new_string = ' '.join(words)
#     return new_string


# sentences, sub_strings = prepare_sentences_and_sub_strings("xin chào các bạn, mình là trần cao sơn. mình đang test cái củ lìn này. Hy vọng rằng, mọi thứ đéo lỗi.")

# print(sentences[0], sub_strings)


# new_string, words = insert_random_strings_between_spaces(sentences[0], sub_strings)
# print(clean_up_spaces(new_string))
# print(words)



vi_sentences, vi_sub_strings = prepare_sentences_and_sub_strings(vi_data)
en_sentences, en_sub_strings = prepare_sentences_and_sub_strings(en_data)

with open('output.txt','w',encoding="utf-8") as f_out:
    # for _ in range(int(SAMPLE_SIZE/len(vi_sentences))):
    count = 0
    # while count < SAMPLE_SIZE:
    for s in vi_sentences:
        if len(s) < 10:
            continue
        new_string, words = insert_random_strings_between_spaces(s, en_sub_strings)
        if len(new_string) > 199:
            continue
        labels = " ".join(['vi'  if i[1] == 'original' else 'en' for i in words ])
        # print(len(new_string))
        f_out.write(f'{clean_up_spaces(new_string)}\t{labels}\n')
        # count += 1