#2차 전처리로 불용어 제거
#부동산 도메인의 불용어 리스트가 따로 정의되지 않았기에 기본적 불용어, 직접 정의한 불용어 csv 파일등 총 3개 활용
import pandas as pd

#1차 전처리된 뉴스 데이터 불러오기
news2023 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/데이터셋/2023년/news_df2023.csv')

#불용어 파일 불러오기
stopword1 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/데이터셋/stopword1.csv', delimiter='\t',header=None)
stopword2 = pd.read_csv('/content/stop_word2.csv',header=None)
stopword3 = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/파인드알파/데이터셋/stopword3.csv',header=None)

#모든 불용어 목록 파일 병합
stop_word = pd.concat([stopword1,stopword2],ignore_index=True,axis=0)
stop_word = pd.concat([stop_word,stopword3],ignore_index=True,axis=0)
stop_word=pd.DataFrame(stop_word)

#word로 컬럼명 변경
stop_word.rename(columns='word', inplace=True)

for q in range(len(stop_word)):
  stop_word.loc[q,'word'] = stop_word.loc[q,0].replace(',','')
stop_word= pd.DataFrame(stop_word['word'])

#불용어 제거
# 불용어의 word 컬럼 헤더에 공백이나 특수 문자가 포함된 것 같으니, 첫 번째 컬럼을 명시적으로 사용
stop_words_set = set(stop_word.iloc[:, 0].str.strip())  # Stripping any whitespace

# 문자열에서 불용어를 필터링하는 함수 정의
def filter_stop_words(nouns_str):
    # 문자열을 단어로 분리
    words = nouns_str.split()
    # 불용어 제거
    filtered_words = [word for word in words if word not in stop_words_set]
    # 단어를 다시 문자열로 결합
    return ' '.join(filtered_words)

# 'nouns' 컬럼에 함수 적용하고 필터링된 명사로 새 컬럼 생성
news2023['filtered_nouns'] = news2023['nouns'].apply(filter_stop_words)

#  새 컬럼을 확인하기 위해 DataFrame을 표시
news2023 = news2023[['date', 'filtered_nouns']]
news2023


