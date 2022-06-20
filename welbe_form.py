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

import json
import streamlit_authenticator as stauth

mood=["幸せではない","やや幸せではない","ふつう","やや幸せ","幸せ"]
happy_score = ['選択して下さい（0〜10点）',0,1,2,3,4,5,6,7,8,9,10]
today = datetime.date.today()
day_list=[]
diary_list=[]

def main():
    day = st.date_input('対象の日付を入力して下さい',today)
    diary = st.text_area(label='A：3行程度で日記をご記入ください（仕事に無関係でも構いません）',height=12)
    with st.expander("クリックで日記の入力例を表示します"):
        st.caption('入力例1：今日仕事忙しすぎて朝しか食べてなくてさっき帰ってきたけど、こんな時間だし食べなくていっか。食べて太るよりは我慢して痩せた方が絶対いいし。いい方法ではないかもしれないけど痩せたい！')
        st.caption('入力例2：珍しく上司から褒められた。あんまり褒めるところ見たことがない上司だから嬉しいけどヘンな感じ（笑）。たまにこういうことがあると頑張ろうって気になります。')
        st.caption('入力例3：リモートワークの日だったけど、自分の空間でひたすら仕事できるっていうのは私には向いてる気がする。もう毎日リモートワークにしてほしい。')
        st.caption('入力例4：今日は忙しすぎて死んだなー。これからやっと事務仕事。忙しくさせてもらってることに感謝。だけどさすがに堪えてる。たまには癒しがほしいっす。')
        st.caption('入力例5：会社から帰る途中の場所にめちゃめちゃお気に入りのご飯屋さんを見つけた。なんてことない定食屋さんだけど、雰囲気含めて全部がツボ。そのうち誰か連れていきたい')
        st.caption('入力例6：旦那は気楽に1人で外出出来ていいなー。決して娘と一緒に居るのが嫌な訳じゃないけど…たまには1人で買い物行きたいなー')
        st.caption('入力例7：最近毎日雨降ってる気がする。洗濯物干せないとかはまだいいけど、何より傘持ったまま朝から満員電車に乗るのが辛すぎる。')

    #my_happy = st.radio("B：あなたは今日一日幸せでしたか？（0点:とても不幸／10点：とても幸せ）",options=happy_score,horizontal=True)
    my_happy = st.selectbox("B：あなたは今日一日幸せでしたか？（0点:とても不幸／10点：とても幸せ）",options=happy_score)
    group_happy = st.selectbox('C：チーム全体としては，今日一日幸せだったと思いますか？（0点:とても不幸／10点：とても幸せ）',options=happy_score)
    location = st.selectbox(
        'D：業務中，主に滞在した場所をお選び下さい',
        options=('選択して下さい','社内の自席', '会議スペース', 'オープンスペース', '自宅', 'その他')
        )
    location_other = st.text_input('E：Dでその他を選択した方は，差し支えない範囲で場所をご記入ください')

    if st.button('SUBMIT') == True:
        st.write('入力完了しました！')
        f=open('data/dailyreport.json','r')
        j_r = json.load(f)
        if str(day) not in j_r.keys():
            j_r[str(day)]={'text':{},'my_happy':{},'group_happy':{},'location':{},'location_other':{}}
        j_r[str(day)]['text'][name]=diary
        j_r[str(day)]['my_happy'][name]=my_happy
        j_r[str(day)]['group_happy'][name]=group_happy
        j_r[str(day)]['location'][name]=location
        j_r[str(day)]['location_other'][name]=location_other
        
        with open('data/dailyreport.json','w') as j_w:
            json.dump(j_r,j_w)

    with open('data/dailyreport.json','r') as j_r2:
        dictDB = json.load(j_r2)
        for days in dictDB.keys():
            if name in dictDB[days]['text'].keys():
                day_list.append(days)
                diary_list.append(dictDB[days]['text'][name])
    df_diary = pd.DataFrame()
    df_diary['day']=day_list
    df_diary['text']=diary_list
    df_diary = df_diary.sort_values(by=['day'],ascending=False)

    with st.expander("クリックであなたの過去の日記を表示します"):
        st.table(data=df_diary)


    with open('data/dailyreport.json','r') as j_r_saved:
        dict_diaryDB = json.load(j_r_saved)

    happy_day_list=[]
    happy_list=[]
    for days in dict_diaryDB.keys():
        for my_happy_scores in dict_diaryDB[days]['my_happy'].values():
            if type(my_happy_scores) != str:
                happy_day_list.append(days)
                happy_list.append(my_happy_scores)

    df_saved_happy = pd.DataFrame()
    df_saved_happy['date']=happy_day_list
    df_saved_happy['happy_score']=happy_list


    st.subheader('Team Well-being Timeline')
    line = alt.Chart(df_saved_happy).mark_line(
        color='red'
    ).encode(
        x=alt.X('date:T',axis=alt.Axis(format="%m月%d日",labelFontSize=14, ticks=False, titleFontSize=18,title='日付')),
        y=alt.Y('mean(happy_score):Q',axis=alt.Axis(titleFontSize=18, title='Team Well-being'))
    ).properties(
        width=650,
        height=400,
        )

    points = alt.Chart(df_saved_happy).mark_point().encode(
        x=alt.X('date:T'),
        y=alt.Y('happy_score:Q')
        ).properties(
            width=650,
            height=400
            )

    st.write(points+line)


# ユーザ情報。引数
names = ['admin','001','002','003','004'] 
usernames = ['admin','001','002','003','004']  # 入力フォームに入力された値と合致するか確認される
passwords = ['admin','001','002','003','004']  # 入力フォームに入力された値と合致するか確認される

# パスワードをハッシュ化。 リスト等、イテラブルなオブジェクトである必要がある
hashed_passwords = stauth.Hasher(passwords).generate()

# cookie_expiry_daysでクッキーの有効期限を設定可能。
#認証情報の保持期間を設定でき値を0とするとアクセス毎に認証を要求する
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=1)

# ログインメソッドで入力フォームを配置
st.title('個と場のWell-being日記')
name, authentication_status, username = authenticator.login('Login', 'main')

# 返り値、authenticaton_statusの状態で処理を場合分け
if authentication_status:
    # logoutメソッドでaurhenciationの値をNoneにする
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (name))
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

