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


#사용가능한 리소스 한계로 각 년도의 월별로 동일한 비율로 랜덤 추출해서 총 50000건으로 데이터 개수 맞춤

def filter_data_by_month(df, date_column, target_count=50000):
    # date_column을 datetime으로 파싱
    df[date_column] = pd.to_datetime(df[date_column])

    # 데이터를 연도와 달별로 그룹화
    grouped = df.groupby([df[date_column].dt.year, df[date_column].dt.month])

    # 목표 수에 맞춰 각 그룹별 샘플 수 계산
    samples_per_group = target_count // len(grouped)
    remaining_samples = target_count % len(grouped)  # 나머지 처리용

    # 샘플링된 데이터를 저장할 빈 DataFrame 초기화
    sampled_df = pd.DataFrame()

    # 나누어 떨어지지 않아 50000개를 정확히 못 맞출 경우 처리를 위한 추가 샘플 필요
    extra_samples_needed = remaining_samples

    for name, group in grouped:
        # 원하는 샘플 수보다 그룹이 작으면 전체 그룹을 취함
        if len(group) <= samples_per_group:
            sampled_df = pd.concat([sampled_df, group])
            # samples_per_group보다 적은 샘플을 취했다면 나중에 추가 샘플을 더 가져와야 함
            extra_samples_needed += (samples_per_group - len(group))
        else:
            # 추가 샘플을 분배할 필요가 있다면 일부 그룹에 1을 더함
            if extra_samples_needed > 0:
                sampled_group = group.sample(n=samples_per_group + 1)
                extra_samples_needed -= 1
            else:
                sampled_group = group.sample(n=samples_per_group)
            sampled_df = pd.concat([sampled_df, sampled_group])

    return sampled_df

filtered_news = filter_data_by_month(total_news, 'date')


filtered_news.to_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/2020_2023_부동산뉴스_감성지수.csv',encoding='utf-8',index=False)
