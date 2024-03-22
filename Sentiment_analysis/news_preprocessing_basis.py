import pandas as pd
import re

#크롤링한 네이버 뉴스 파일 불러오기
df_2301 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/데이터셋/2023년/네이버뉴스_202301.csv')
df_2307 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/데이터셋/2023년/네이버뉴스_202307.csv')

#크롤링 중 발생한 널값 제거
print(df_2301.isnull().sum())
print(df_2307.isnull().sum())
df_2301 = df_2301.dropna().reset_index().drop(columns='index')
df_2307= df_2307.dropna().reset_index().drop(columns='index')
print(df_2301.isnull().sum())
print(df_2307.isnull().sum())

#불필요한 컬럼 제거 및 날짜 순으로 뉴스 데이터 정렬 함수
def DelCol_SortDate(df):
  df=df[['main','filtered_date']]
  df =df.sort_values(by='filtered_date').reset_index(drop=True)
  return df

df_2301 = DelCol_SortDate(df_2301)
df_2307 = DelCol_SortDate(df_2307)


#불필요한 문자 및 기호 삭제 함수
def del_char(df):
  
  cleaned_art = pd.DataFrame({'text':{}})
  
  # 문자와 숫자를 제외한 모든 특수 문자 및 공백을 제거
  for i in range(len(df)):
    #뉴스 본문 컬럼명 수정: 'main' -> 'text'
    cleaned_art.loc[i,'text'] = re.sub(r'[^A-Za-z0-9가-힣\s]', '', df.loc[i,'main'])
    #뉴스 게시일 컬럼명 수정: 'filtered_date' -> 'date'
    cleaned_art.loc[i,'date'] = df.loc[i,'filtered_date']
  return cleaned_art

df_2301 = del_char(df_2301)
df_2307 = del_char(df_2307)

#1년 단위로 전처리된 뉴스 데이터셋 병합
news_df2023 = pd.concat([df_2301,df_2307],ignore_index=True,axis=0)

#명사만 추출하기 위해 Okt 형태소 분석기 활용
from konlpy.tag import Okt
# Okt 형태소 분석기 객체 생성
okt = Okt()
def extract_nouns(text):
    nouns = okt.nouns(text)
    filtered_nouns = [noun for noun in nouns if len(noun) >= 2]  # 길이가 2 이상인 명사만 추출
    return filtered_nouns

# '문장' 컬럼에 있는 각 텍스트에 대해 명사 추출 함수 적용
news_df2023['noun'] = news_df2023['text'].apply(extract_nouns)

#명사 추출이 리스트 형태로 되며 생긴 '[,]와 같은 기호 추가 제거
for q in range(len(news_df2023)):
  d = news_df2023['noun'][q]
  d = d.replace(",","")
  d= d.replace("'",'')
  d= d.replace("[",'')
  d= d.replace("]",'')

  #명사만 존재하는 nouns 컬럼에 저장 
  news_df2023.loc[q,'nouns'] = d

#1차 전처리된 뉴스데이터 csv파일로 저장
news_df2023.to_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/데이터셋/2023년/news_df2023.csv',encoding='utf-8',index=False)
