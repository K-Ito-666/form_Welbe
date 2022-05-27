# -*- coding: utf-8 -*-

from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from bokeh.plotting import figure
import altair as alt
import datetime

labels = ['SELF',
    'OTHER-SPECIFIC',
    'OTHER-COLLECTIVE',
    'NON-HUMAN',
    'NEGATIVE'
    ]

def main():    
    df = pd.read_excel('sample_dailyreport.xlsx')
    st.title('3行日記　入力フォーム')

    st.text_input('3行程度で日記をご記入ください')
    st.radio('今日の気分をお選びください',('Happy','Sad','Surprised'))
    st.text_input('本日，業務中に滞在した場所をご記入ください（読点orカンマ区切り）')
    st.button('SUBMIT')

    date_gch_cnt={}

    for idx,date_list in enumerate(df['date']):
        if date_list.strftime('%m%d') not in date_gch_cnt.keys():
            date_gch_cnt[date_list.strftime('%m%d')]={l:0 for l in labels}

        for label in labels:
            if label == df['pred_label'][idx]:
                date_gch_cnt[date_list.strftime('%m%d')][label] += 1
    
    for d in date_gch_cnt.keys():
        tmp_sum = 0
        for label in labels:
            tmp_sum += date_gch_cnt[d][label]
        for label in labels:
            date_gch_cnt[d][label] = date_gch_cnt[d][label]/tmp_sum

    df_multi = pd.DataFrame.from_dict(date_gch_cnt,orient='index')

    st.write(df_multi)
    df_multi['date'] = df_multi.index
    df_multi = df_multi.drop('NEGATIVE',axis=1)

    df_multi = pd.melt(df_multi,
                    value_name = 'value',
                    id_vars=['date'])

    date_gch_binary={}
    for date_list in date_gch_cnt.keys():
        sum_tmp = 0
        ratio_tmp = 0
        for label in labels:
            sum_tmp += date_gch_cnt[date_list][label]
        ratio_tmp = 1 - (date_gch_cnt[date_list]['NEGATIVE'] / sum_tmp)
        date_gch_binary[date_list] = ratio_tmp

    df_binary = pd.DataFrame()
    df_binary['date'] = date_gch_binary.keys()
    df_binary['ratio'] = date_gch_binary.values()

    df_emo = pd.read_excel('emoticon.xlsx')
    date_happy_rate=[]
    for idx,date_list in enumerate(df_emo['date']):
        happy = df_emo['happy'][idx]
        sad = df_emo['sad'][idx]
        surprise = df_emo['surprise'][idx]
        date_happy_rate.append(round(happy/(happy+sad+surprise),2))
    df_emo['happy_rate']=date_happy_rate

    # 折れ線グラフ
    st.subheader('Team Well-being(NLP-Based)')
    bi = alt.Chart(df_binary).mark_line().encode(
        x=alt.X('date:T', title='日付'),
        y=alt.Y('ratio:Q', title='Team Well-being(NLP-Based)'),
        ).properties(width=400, height=300)

    st.altair_chart(bi,use_container_width = True)

    st.subheader('Emoticon-Based Score')
    bi = alt.Chart(df_emo).mark_line().encode(
        x=alt.X('date:T', title='日付'),
        y=alt.Y('happy_rate:Q', title='Team Well-being'),
        ).properties(width=400, height=300)

    st.altair_chart(bi,use_container_width = True)

    st.subheader('愚痴の割合の推移')
    bi = alt.Chart(df_binary).mark_line().encode(
        x=alt.X('date:T', title='日付'),
        y=alt.Y('ratio:Q', title='愚痴指数'),
        ).properties(width=400, height=300)

    st.altair_chart(bi,use_container_width = True)


    st.subheader('愚痴の対象ごとの割合')
    mul = alt.Chart(df_multi).mark_line().encode(
        x=alt.X('date:T', title='日付'),
        y=alt.Y('value:Q', title='愚痴指数'),
        color=alt.Color('variable:N',title='Target')
        ).properties(width=400, height=300)

    st.altair_chart(mul,use_container_width = True)


    st.subheader('各感情ごとの愚痴の割合')

    binary_category = ['愚痴', 'not 愚痴']
    populations = [20, 14]

    left_column,center_column,right_column = st.columns(3)

    fig_happy = go.Figure(data=[go.Bar(x=binary_category, y=populations)])
    fig_happy.update_layout(
        xaxis = dict(
            tickangle = 0,
            title_text = "Happy",
            title_font = {"size": 20},
            title_standoff = 25),
        yaxis = dict(
            title_standoff = 25),
        margin=dict(
            t=10, b=20, l=30, r=40)
    )

    fig_Surprise = go.Figure(data=[go.Bar(x=binary_category, y=populations)])
    fig_Surprise.update_layout(
        xaxis = dict(
            tickangle = 0,
            title_text = "Surprise",
            title_font = {"size": 20},
            title_standoff = 25,
            ),
        yaxis = dict(
            title_standoff = 25),
        margin=dict(
            t=10, b=20, l=30, r=40)
    )

    fig_Sad = go.Figure(data=[go.Bar(x=binary_category, y=populations)])
    fig_Sad.update_layout(
        xaxis = dict(
            tickangle = 0,
            title_text = "Sad",
            title_font = {"size": 20},
            title_standoff = 25),
        yaxis = dict(
            title_standoff = 25),
        margin=dict(
            t=10, b=20, l=30, r=40)
    )

    left_column.plotly_chart(fig_happy, use_container_width=True)
    center_column.plotly_chart(fig_Surprise, use_container_width=True)
    right_column.plotly_chart(fig_Sad, use_container_width=True)

    '''
    uploaded_file=st.file_uploader("ファイルアップロード", type='png')
    image=Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(img_array,caption = 'サムネイル画像',use_column_width = True)
    '''
    st.write('感情ラベルの画像と，ワードクラウドでの頻出語表示も行いたいところ')

if __name__ == '__main__':
    main()