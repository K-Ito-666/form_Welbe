#from asyncio.windows_events import NULL
#from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import altair as alt
import datetime
import copy
import plotly.figure_factory as ff
import plotly.express as px

mood=["幸せではない","やや幸せではない","ふつう","やや幸せ","幸せ"]
happy_score = [,0,1,2,3,4,5,6,7,8,9,10]

st.title('個と場のWell-being日記')
diary = st.text_area(label='A：3行程度で日記をご記入ください（仕事に無関係でも構いません）', height=12)
with st.expander("クリックで日記の入力例を表示します"):
    st.caption('入力例1：今日仕事忙しすぎて朝しか食べてなくてさっき帰ってきたけど、こんな時間だし食べなくていっか。食べて太るよりは我慢して痩せた方が絶対いいし。いい方法ではないかもしれないけど痩せたい！')
    st.caption('入力例2：珍しく上司から褒められた。あんまり褒めるところ見たことがない上司だから嬉しいけどヘンな感じ（笑）。たまにこういうことがあると頑張ろうって気になります。')
    st.caption('入力例3：リモートワークの日だったけど、自分の空間でひたすら仕事できるっていうのは私には向いてる気がする。もう毎日リモートワークにしてほしい。')
    st.caption('入力例4：今日は忙しすぎて死んだなー。これからやっと事務仕事。忙しくさせてもらってることに感謝。だけどさすがに堪えてる。たまには癒しがほしいっす。')
    st.caption('入力例5：会社から帰る途中の場所にめちゃめちゃお気に入りのご飯屋さんを見つけた。なんてことない定食屋さんだけど、雰囲気含めて全部がツボ。そのうち誰か連れていきたい')
    st.caption('入力例6：旦那は気楽に1人で外出出来ていいなー。決して娘と一緒に居るのが嫌な訳じゃないけど…たまには1人で買い物行きたいなー')
    st.caption('入力例7：最近毎日雨降ってる気がする。洗濯物干せないとかはまだいいけど、何より傘持ったまま朝から満員電車に乗るのが辛すぎる。')

my_happy = st.radio("B：あなたは今日一日幸せでしたか？（0点:とても不幸／10点：とても幸せ）",options=happy_score,horizontal=True)
group_happy = st.radio('C：チーム全体としては，今日一日幸せだったと思いますか？（0点:とても不幸／10点：とても幸せ）',options=happy_score,horizontal=True)
location = st.selectbox(
    'D：業務中，主に滞在した場所をお選び下さい',
    ('社内の自席', '会議スペース', 'オープンスペース', '自宅', 'その他')
    )
location_other = st.text_input('E：Dでその他を選択した方は場所をご記入ください')

if st.button('SUBMIT') == True:
  st.write(diary,my_happy,group_happy,location,location_other)

df = pd.read_excel('data/sample_dailyreport.xlsx')
st.subheader('Team Well-being Timeline')
line = alt.Chart(df).mark_line(
    color='red'
).encode(
    x=alt.X('date:T',axis=alt.Axis(format="%m月%d日",labelFontSize=14, ticks=False, titleFontSize=18,title='日付')),
    y=alt.Y('mean(P):Q',axis=alt.Axis(titleFontSize=18, title='Team Well-being'))
).properties(
    width=650,
    height=400,
    )


points = alt.Chart(df).mark_point().encode(
    x=alt.X('date:T'),
    y=alt.Y('P:Q')
    ).properties(
        width=650,
        height=400
        )

st.write(points+line)
