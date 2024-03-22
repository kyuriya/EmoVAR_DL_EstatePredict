import pandas as pd
import numpy as np

news_df2023 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/2023년/2023_부동산뉴스_불용어제거.csv')

#주별 아파트 매매 가격지수 증감률
price_vol = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/주간 아파트 매매가격지수증감률_20240114.xlsx')
all_vol= price_vol.iloc[0,:] #전국 범위
all_vol=all_vol.reset_index()
all_vol.columns.values[0] = 'date'
all_vol.columns.values[1] = 'rate'
all_vol = all_vol.iloc[1:,:]

#원하는 날짜 범위에 따라 필터링
#2023년 데이터이므로  아래와 같이 날짜 설정
all_vol2023 = all_vol[all_vol['date']<'2024-01-10']
all_vol2023 = all_vol2023[all_vol2023['date']>='2023-01-01']
all_vol2023 = all_vol2023.reset_index(drop=True)


news_df2023['date']= news_df2023['date'].astype(str)
# 해당 뉴스 게시일에 해당하는 매매 가격지수 증감률 채우기
for l in range(len(news_df2023)):
    for x in range(1, len(all_vol2023)):
        if news_df2023.loc[l, 'date'] <= all_vol2023.loc[x, 'date']:
            news_df2023.loc[l, 'rate'] = all_vol2023.loc[x, 'rate']
            break  # 가장 가까운 이전 날짜를 찾았으면 루프 종료

#가격지수 증감률에 따른 가격 상승 및 하강 라벨링
#해당년도의 전체 증감률의 평균보다 크면 상승이자 1, 작으면 하강이자 0
for q in range(len(news_df2023)):
  if news_df2023.loc[q,'rate']>=np.mean(news_df2023['rate'].mean()):
    news_df2023.loc[q,'updown'] = 1
  else:
    news_df2023.loc[q,'updown'] = 0

#클래스별 개수 확인(클래스 불균형 발생하는지)
print(news_df2023[news_df2023['updown']==0].count())
print(news_df2023[news_df2023['updown']==1].count())

#'rate'컬럼 제거
news_df2023_label = news_df2023[['date','filtered_nouns','updown']]

#라벨링된 데이터 저장
news_df2023_label.to_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/2023 final project/데이터셋/2023년/2023_뉴스데이터_명사_라벨링.csv',encoding='utf-8',index=False)

