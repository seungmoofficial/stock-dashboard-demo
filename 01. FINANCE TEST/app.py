import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Stock View | Robinhood Style",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Robinhood Theme)
st.markdown("""
<style>
    /* Metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
    }
    .quick-chip {
        display: inline-block;
        padding: 4px 12px;
        margin: 4px;
        background-color: #f0f2f6;
        border-radius: 16px;
        cursor: pointer;
    }
    .stat-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📈 Stock Explorer")
st.sidebar.markdown("로빈후드 스타일 실시간 주식 대시보드")

# Quick ticker selection
popular_tickers = ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL", "AMZN"]
selected_quick = st.sidebar.selectbox("인기 종목 바로가기", ["직접 입력"] + popular_tickers)

if selected_quick != "직접 입력":
    default_ticker = selected_quick
else:
    default_ticker = "NVDA"

ticker_input = st.sidebar.text_input("티커 심볼 입력 (예: TSLA, AAPL)", value=default_ticker).strip().upper()

# Period selection
period_dict = {
    "1일 (1D)": ("1d", "5m"),
    "5일 (5D)": ("5d", "15m"),
    "1개월 (1M)": ("1mo", "1d"),
    "6개월 (6M)": ("6mo", "1d"),
    "1년 (1Y)": ("1y", "1d"),
    "5년 (5Y)": ("5y", "1wk"),
}
selected_period_label = st.sidebar.radio("조회 기간", list(period_dict.keys()), index=2)
period, interval = period_dict[selected_period_label]

chart_type = st.sidebar.radio("차트 종류", ["라인 차트 (Line)", "캔들스틱 (Candlestick)"])

# Fetch Stock Data
@st.cache_data(ttl=60)
def load_stock_data(symbol, p, i):
    try:
        t = yf.Ticker(symbol)
        history = t.history(period=p, interval=i)
        info = t.info
        return history, info, None
    except Exception as e:
        return None, None, str(e)

if not ticker_input:
    st.warning("티커 심볼을 입력해 주세요.")
    st.stop()

with st.spinner(f"'{ticker_input}' 데이터를 불러오는 중..."):
    history_df, info_data, error = load_stock_data(ticker_input, period, interval)

if error or history_df is None or history_df.empty:
    st.error(f"'{ticker_input}' 종목 데이터를 찾을 수 없습니다. 올바른 티커 심볼인지 확인해 주세요.")
    st.stop()

# Basic Info Extraction
company_name = info_data.get("shortName") or info_data.get("longName") or ticker_input
currency = info_data.get("currency", "USD")
currency_symbol = "$" if currency == "USD" else currency + " "

current_price = history_df["Close"].iloc[-1]
first_price = history_df["Open"].iloc[0]
price_diff = current_price - first_price
pct_change = (price_diff / first_price) * 100 if first_price != 0 else 0

# Colors (Robinhood: Green for up, Red for down)
is_positive = price_diff >= 0
theme_color = "#00C805" if is_positive else "#FF5000"
color_name = "green" if is_positive else "red"

# Header Section
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"{company_name} ({ticker_input})")
    sign = "+" if price_diff >= 0 else ""
    st.metric(
        label="현재 가격",
        value=f"{currency_symbol}{current_price:,.2f}",
        delta=f"{sign}{currency_symbol}{price_diff:,.2f} ({sign}{pct_change:.2f}%)"
    )

# Interactive Chart
fig = go.Figure()

if chart_type == "캔들스틱 (Candlestick)" and len(history_df) > 1:
    fig.add_trace(go.Candlestick(
        x=history_df.index,
        open=history_df['Open'],
        high=history_df['High'],
        low=history_df['Low'],
        close=history_df['Close'],
        increasing_line_color='#00C805',
        decreasing_line_color='#FF5000',
        name="주가"
    ))
else:
    fig.add_trace(go.Scatter(
        x=history_df.index,
        y=history_df['Close'],
        mode='lines',
        line=dict(color=theme_color, width=2.5),
        name="주가",
        fill='tozeroy',
        fillcolor=f"rgba({'0, 200, 5' if is_positive else '255, 80, 0'}, 0.08)"
    ))

fig.update_layout(
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis_rangeslider_visible=False,
    height=420,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    hovermode="x unified",
    xaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)"),
    yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.1)", tickprefix=currency_symbol)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Key Statistics & Company Summary
col_stats, col_about = st.columns([1, 1])

def format_number(num):
    if not num or num == "N/A":
        return "N/A"
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    if num >= 1e9:
        return f"${num/1e9:.2f}B"
    if num >= 1e6:
        return f"${num/1e6:.2f}M"
    return f"{num:,.2f}"

with col_stats:
    st.markdown("### 📊 주요 통계 (Key Statistics)")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("**시가 총액:**", format_number(info_data.get("marketCap")))
        st.write("**52주 최고가:**", f"{currency_symbol}{info_data.get('fiftyTwoWeekHigh', 0):,.2f}")
        st.write("**52주 최저가:**", f"{currency_symbol}{info_data.get('fiftyTwoWeekLow', 0):,.2f}")
    with c2:
        pe_ratio = info_data.get("trailingPE")
        st.write("**PER (P/E Ratio):**", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
        div_yield = info_data.get("dividendYield")
        st.write("**배당 수익률:**", f"{div_yield*100:.2f}%" if div_yield else "N/A")
        st.write("**거래량:**", f"{history_df['Volume'].iloc[-1]:,}" if 'Volume' in history_df else "N/A")

with col_about:
    st.markdown(f"### 🏢 기업 소개 (About {company_name})")
    sector = info_data.get("sector", "N/A")
    industry = info_data.get("industry", "N/A")
    st.caption(f"**섹터:** {sector} | **산업:** {industry}")
    
    summary = info_data.get("longBusinessSummary", "상세 소개 정보가 없습니다.")
    if len(summary) > 400:
        st.write(summary[:400] + "...")
    else:
        st.write(summary)

st.caption("💡 Data powered by Yahoo Finance API | Built with Streamlit")

