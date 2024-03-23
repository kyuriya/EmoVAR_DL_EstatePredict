# 🏠 뉴스의 감성분석과 VAR 모형을 이용한 딥러닝 기반 부동산 가격 예측 🏠
------------------------------------------
## 프로젝트 개요
### 연구 목적
1. 외부 경기 변동에 의한 부동산 가격
- 외부경기 변동에 의해 부동산 가격의 변화 양상을 파악하고 그 상호작용을 분석

2. 기존의 연구결과 대비 모델 성능 향상
- 선행연구로 진행되었던 신은경,김은미,and 홍태호. "뉴스의 감성분석과 전문가 지식을 이용한 딥러닝 기반의 부동산 가격 예측." 인터넷전자상거래연구 22.3 (2022): 61-73.를 발전시키기 위해 VAR 모형 추정값을 추가적으로 활용하여 매매가격 예측 모델을 구축
- 또한 이를통해 이전 연구 결과와 비교하며 모델 성능 향상을 목표로 설정
### 모델링 프로세스
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/6aa11818-d67f-4590-a1f4-970744c59c5a">

## 매매 가격 예측 모형 구축
### 모형선택 이유

<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/c09a7c64-6316-4a33-9216-6795323d2c33">

### VAR 모형 추정 프로세스
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/2610a43c-555e-4565-9b47-c35f60f55302">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/80031af9-f14c-49fd-bcf0-09803085aec9">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/ac077451-445c-416b-a8c2-bffd8ae867b1">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/3672c28e-3860-47e8-9509-60529fc47749">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/a30e05c1-8bca-4799-bf87-6ec5617c9201">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/ce22c81f-5521-4954-ba72-fe17cfadaf84">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/aa7d593c-4eb3-40ed-aa53-792e796ff7bd">


### 부동산 뉴스 감성분석 프로세스
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/8a465794-6242-486d-a1e6-22bd1c5fd361">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/959d6566-4cec-4f52-9e80-1505b6112e75">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/c240fcfe-5530-479e-ae5b-655330712940">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/7d5731f9-29f7-4473-9155-a22151569083">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/03af3e0c-09ab-4cf1-ac86-a6328e107c1f">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/3b208e40-8d83-42fb-9965-5afadcf163c4">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/d53b3806-7a8b-4ddf-8826-cda89b066ce2">

### 딥러닝 기반 예측 모형
- LSTM / GRU / AdaBoost + GRU 앙상블 모형로 총 3가지 딥러닝 모형 활용하여 매매가격 예측 진행
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/8765ce7c-3270-42eb-b954-5e2b4a40af68">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/d7888659-9835-4c2b-ace4-b690ac47ac3e">
<img width="1087" alt="image" src="https://github.com/kyuriya/EmoVAR_DL_EstatePredict/assets/164462761/cc4fcf80-5c8e-4c6e-825e-2c4cb485a584">


## 결론 및 향후 보완점



