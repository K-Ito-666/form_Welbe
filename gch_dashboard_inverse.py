# -*- coding: utf-8 -*-

from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from bokeh.plotting import figure
import altair as alt
import datetime
import copy
import plotly.figure_factory as ff
import plotly.express as px

labels = ['SELF',
    'OTHER-SPECIFIC',
    'OTHER-COLLECTIVE',
    'NON-HUMAN',
    'NEGATIVE'
    ]

def main():    
    df = pd.read_excel('data/sample_dailyreport.xlsx')
    st.title('3行日記　入力フォーム')

    st.text_area(label='A：3行程度で日記をご記入ください', height=12)
    st.slider("B：今日のあなたの気分をお選びください", 1, 10, 5, 1)
    st.slider('C：今日の，あなたが思うチーム全体の気分をお選びください',1,10,5,1)
    st.selectbox(
        'D：今日，主に業務中に滞在した場所をお選び下さい',
        ('社内の自席', '会議スペース', 'オープンスペース', '自宅', 'その他')
        )
    st.text_input('E：Dでその他を選択した方は場所をご記入ください')
    st.selectbox(
        'F：今日，オフラインで接した人数をお選び下さい',
        ('0人', '1〜3人', '4〜6人', '7〜9人', '10人以上')
        )
    st.selectbox(
        'G：今日，オンラインで接した人数をお選び下さい',
        ('0人', '1〜3人', '4〜6人', '7〜9人', '10人以上')
        )
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
    df_table = copy.copy(df_multi)

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

    # 折れ線グラフ
    st.subheader('Team Well-being')
    bi = alt.Chart(df_binary).mark_line().encode(
        x=alt.X('date:T', title='日付'),
        y=alt.Y('ratio:Q', title='Team Well-being'),
        ).properties(width=400, height=300)

    st.altair_chart(bi,use_container_width = True)

    fig = px.box(df,y='P',x='date')
    fig.show()


if __name__ == '__main__':
    main()