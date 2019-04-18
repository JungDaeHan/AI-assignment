from konlpy.tag import Okt
import math

okt = Okt()
pos=[]
neg=[]

def manipulate():
    f = "/home/uchihe/2018_CSE4007_2013011640/assignment2/ratings_train.txt"
    with open(f) as data:
        data.readline()
        text = [[i for i in line.split('\t')] for line in data.readlines()]

    for i in text:
        manu = okt.pos(i[1])
        
        if i[2] == '0\n':
            for a in manu:
                if a[1] == "Adjective" or "Adverb" or "Foreign" or "Noun" or "Verb" or "Number" : 
                    pos.append(str(a[0]))
        else:
            for a in manu:
                if a[1] == "Adjective" or "Adverb" or "Foreign" or "Noun" or "Verb" or "Number" : 
                    neg.append(str(a[0]))

def naive_bayes_classifier(pos,pos_set,neg,neg_set,all_cnt,pos_cnt,neg_cnt):
    f = "/home/uchihe/2018_CSE4007_2013011640/assignment2/ratings_test.txt"
    r = open("ratings_result.txt", 'w')
    r.write("id\tdocument\tlabel\n")

    with open(f) as data:
        data.readline()
        text = [[i for i in line.split("\t")] for line in data.readlines()]

    for i in text:
        prob_pos = 0
        prob_neg = 0
        a = okt.pos(i[1])
        
        for j in a:
            if j[0] not in pos_set:
                prob_pos += math.log(1/(pos_cnt+all_cnt))
            elif j[1] == "Adjective" or "Adverb" or "Foreign" or "Noun" or "Verb" or "Number":
                tmp = pos_set.index(j[0])
                prob_pos += pos[tmp][1]
        prob_pos += math.log(0.5)
        
        for j in a:
            if j[0] not in neg_set:
                prob_neg += math.log(1/(neg_cnt+all_cnt))
            elif j[1] == "Adjective" or "Adverb" or "Foreign" or "Noun" or "Verb" or "Number":
                tmp = neg_set.index(j[0])
                prob_neg += neg[tmp][1]
        prob_neg += math.log(0.5)

        r.write(i[0])
        r.write("\t")
        r.write(i[1])
        r.write("\t")
        
        if prob_pos < prob_neg:
            r.write("1")
        else:
            r.write("0")

        r.write("\n")

manipulate()

pos_set = list(set(pos))
neg_set = list(set(neg))

all_cnt = len(pos_set) + len(neg_set)
pos_cnt = len(pos)
neg_cnt = len(neg)

pos_tuple = []
neg_tuple = []

for i in pos_set:
    pos_tuple.append((i,math.log((pos.count(i)+1)/(pos_cnt + all_cnt))))
for i in neg_set:
    neg_tuple.append((i,math.log((neg.count(i)+1)/(neg_cnt + all_cnt))))

print(all_cnt)
print(pos_cnt)
print(neg_cnt)

naive_bayes_classifier(pos_tuple,pos_set,neg_tuple,neg_set,all_cnt,pos_cnt,neg_cnt)


