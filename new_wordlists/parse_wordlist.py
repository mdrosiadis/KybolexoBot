words = []

str_trans = {'Ά':'Α', 'Έ':'Ε', 'Ό':'Ο', 'Ή':'Η', 'Ί':'Ι',
             'Ύ':'Υ', 'Ώ':'Ω', 'Ϊ':'Ι', 'Ϋ':'Υ', 'Ϋ́':'Υ', 'Ϊ́':'Ι'}
with open("el_GR.dic", encoding="iso-8859-7") as f:
    f.readline()
    for line in f:
        line = line.upper().strip()
        for f, t in str_trans.items():
            line = line.replace(f, t)

        words.append(line)


out_str = '\n'.join(words)
with open("extended_wordlist.txt", 'w') as f:
    f.write(out_str)
    f.write('\n')


