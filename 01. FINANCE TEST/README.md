# 📈 Robinhood-style Stock Dashboard

Streamlit과 Yahoo Finance API를 활용하여 만든 실시간 미국 주식 시세 및 차트 대시보드 웹 애플리케이션입니다.

## ✨ 주요 기능
- **실시간 주가 조회**: 티커 심볼(예: NVDA, TSLA, AAPL 등) 검색 및 인기 종목 빠른 선택
- **로빈후드 테마 디자인**: 가격 상승/하락에 따른 실시간 테마 컬러(초록/빨강) 반영
- **인터랙티브 차트**: 라인 차트 및 캔들스틱 지원, 기간별(1D, 5D, 1M, 6M, 1Y, 5Y) 조회
- **주요 재무 지표**: 시가총액, 52주 최고/최저가, PER, 배당수익률, 기업 개요 제공

## 🚀 로컬 실행 방법

1. 필요 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 앱 실행:
```bash
streamlit run app.py
```

## 🌐 무료 배포 방법 (Streamlit Community Cloud)

1. [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 GitHub 계정으로 로그인합니다.
2. `Create app` 버튼을 클릭합니다.
3. 이 저장소(`stock-dashboard-demo`)를 선택하고 Main file path를 `app.py`로 설정한 뒤 **Deploy**를 클릭합니다.
4. 전 세계 누구나 접속할 수 있는 고유한 무료 URL이 생성됩니다.

