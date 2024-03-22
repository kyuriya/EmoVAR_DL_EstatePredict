#6개월 단위로 네이버 부동산 카테고리 뉴스 크롤링
import requests
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import pandas as pd
import random

def ex_tag(sid=101, page=None, date=None):
    # 특정 날짜의 뉴스 링크를 추출하는 함수
    news_url = f'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=260&sid1={sid}&date={date}&page={page}'
    html = requests.get(news_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")
    a_tag = soup.find_all("a")

    tag_lst = []
    for a in a_tag:
        if "href" in a.attrs and (f"sid={sid}" in a["href"]) and ("article" in a["href"]):
            if a["href"].startswith("http"):  # 이미 전체 URL 형식인 경우
                full_url = a["href"]
            else:  # 상대 URL인 경우
                full_url = "https://news.naver.com" + a["href"]
            tag_lst.append(full_url)
    return tag_lst


def re_tag(sid, date):
    # 지정된 날짜의 모든 페이지의 뉴스 링크 수집
    re_lst = []
    for i in tqdm(range(4)):  # 4 페이지까지 탐색
        lst = ex_tag(sid, i+1, date)
        re_lst.extend(lst)

    # 중복 제거
    re_set = set(re_lst)
    re_lst = list(re_set)
    return re_lst

def art_crawl(url):
    # 기사 데이터 크롤링 함수
    art_dic = {}
    title_selector = "#title_area > span"
    date_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div:nth-child(1) > span"
    main_selector = "#dic_area"

    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"})
    soup = BeautifulSoup(html.text, "lxml")

    date = soup.select(date_selector)
    date_str = "".join([d.text for d in date])

    main = soup.select(main_selector)
    main_str = "".join([m.text.strip() for m in main])

    art_dic["date"] = date_str
    art_dic["main"] = main_str
    return art_dic

def collect_news(sid, start_date, end_date):
    # 지정된 기간 동안의 뉴스 수집
    date_range = pd.date_range(start=start_date, end=end_date)
    news = {}
    for date in tqdm(date_range):
        date_str = date.strftime("%Y%m%d")
        news[date_str] = re_tag(sid, date_str)
    return news

# 기사 데이터 수집 및 데이터프레임 생성
sid = 101  # 카테고리 섹션 ID
start_date = '20230701' #YYYYMMDD 형식으로 입력
end_date = '20231231'

all_news = collect_news(sid, start_date, end_date)

# 기사 내용 크롤링 및 데이터프레임 생성
artdic_lst = []
for date, links in all_news.items():
    for link in tqdm(links):
        art_dic = art_crawl(link)
        artdic_lst.append(art_dic)

art_df = pd.DataFrame(artdic_lst)


#수집기간 벗어난 기사 전처리
def filter_dataframe_by_date_range(df, date_column, start_date, end_date):
    """
    주어진 DataFrame에서 지정된 날짜 범위 내의 행만 남기고 나머지는 삭제합니다.

    Args:
        df (pandas.DataFrame): 날짜 정보가 포함된 DataFrame.
        date_column (str): 날짜 정보가 있는 열의 이름.
        start_date (str): 시작 날짜 (예: '20240101').
        end_date (str): 종료 날짜 (예: '20240102').

    Returns:
        pandas.DataFrame: 날짜 범위 내의 행만 남긴 DataFrame.
    """
    # 새로운 컬럼에 원래 'date' 컬럼 복사
    for s in range(len(df)):
      df.loc[s,'filtered_date'] =df.loc[s,'date'].replace('.', ' ')[:10]
    # 'date_column'을 datetime 형식으로 변환
    df['filtered_date'] = pd.to_datetime(df['filtered_date'], format='%Y %m %d', errors='coerce')

    # start_date와 end_date를 datetime 형식으로 변환
    start_date = pd.to_datetime(start_date, format='%Y%m%d')
    end_date = pd.to_datetime(end_date, format='%Y%m%d')

    # 범위를 벗어나는 행의 인덱스 찾기
    indices_to_delete1 = df[(df['filtered_date'] < start_date) ].index
    indices_to_delete2 = df[(df['filtered_date'] > end_date)].index
    # 해당 인덱스에 해당하는 행 삭제
    df = df.drop(indices_to_delete1)
    df = df.drop(indices_to_delete2)
    # 'filtered_date' 컬럼 삭제
    # df = df.drop('filtered_date', axis=1) #추후 데이터 전처리에 사용하여 본 프로젝트에서는 제거하지 않음

    return df
#수집 기간 벗어난 뉴스가 제거된 뉴스 데이터
filtered_df = filter_dataframe_by_date_range(art_df, 'date', start_date, end_date)

#수집시작 기간을 파일명으로 사용
xlsx_file_name = '네이버뉴스_{}.csv'.format(start_date[:6])

#수집한 데이터 중 랜덤으로 10000 건 추출
random_sample = filtered_df.sample(n=10000, random_state=random.seed())

#최종 뉴스 데이터셋을 csv로 저장
random_sample.to_csv(xlsx_file_name, index=False, encoding='utf-8')


