import pandas as pd
x1 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/2020년/2020_뉴스데이터_명사_라벨링.csv')
x2 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/2021년/2021_뉴스데이터_명사_라벨링.csv')
x3 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/2022년/2022_뉴스데이터_명사_라벨링.csv')
x4 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/2023년/2023_뉴스데이터_명사_라벨링.csv')
total_news = pd.concat([x1,x2,x3,x4],axis = 0)

# 각 단어가 담긴 빈 감성사전 생성
vocab= {}
cnt = 0
for i in total_news['filtered_nouns']:
  i = i.split(" ")
  for j in range(len(i)):
    if i[j] in vocab or len(i[j])<=1:
      cnt = cnt +1
      pass
    else:
      vocab[i[j]] = 0
# print(vocab)

#총 데이터셋의 0,1 라벨링 개수 파악 #0(down) ->32584 , 1(up) ->46228

up = 29486
down = 20514
up_ratio = up/(up+down)
down_ratio = down/(up+down)

import collections
for i,w in enumerate(total_news['filtered_nouns']):
  w = w.split(' ')
  if total_news.iloc[i]['updown']==1:
    for j in range(len(w)):
      noun = w[j]
      if len(noun) <=1:
        continue
      vocab[noun] = vocab[noun] + down_ratio

  else:
    for j in range(len(w)):
      noun = w[j]
      if len(noun)<=1:
        continue
      vocab[noun] = vocab[noun] - up_ratio

#위에서 구축된 감성사전 활용하여 감성지수 계산      
sent_dictionary = vocab

total = []
for i,w  in enumerate(total_news['filtered_nouns']):
    sent_score = 0
    w= w.split(' ')
    for j in w:
        if(len(j)<=1):
          continue
        elif(j not in sent_dictionary):
          continue
        else:
          sent_score = sent_score + sent_dictionary[j]
    total.append(sent_score/len(w))

#'sent_score'컬럼에 감성지수 저장
total_news['sent_score'] = total

total_news.to_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/2019_2023_부동산뉴스_감성지수.csv',encoding='utf-8',index=False)
