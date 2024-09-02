# 终端运行程序指令
# streamlit run Home.py

import base64
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="清流案例管理后台", page_icon="✈️", initial_sidebar_state="expanded")


# 图片压缩和解码
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


st.write("## 欢迎使用✈️清流教育Alpha管理后台!")

st.sidebar.success("请选择需要的功能")

st.sidebar.markdown('''<img src='data:image/png;base64,{}' class='img-fluid' width=221 height=47>'''.format(
    img_to_bytes("./source_pictures/logo.png")), unsafe_allow_html=True)

st.sidebar.caption("")
st.sidebar.caption("更多信息请关注“清流留学咨询”微信公众号")
st.sidebar.caption("Developed by 清流教育")
st.sidebar.caption("版权所有©清流教育")

st.markdown(
    """
    **更新于 2024年8月20日**  
      
    🎉 [清流教育](http://qingliuapply.com/) 主打精英陪伴式申请服务，通过吸纳毕业于斯坦福、哈佛、普林斯顿、麻省理工、哥大、剑桥、伦敦政经、帝国理工、港科大、港大、清北复交等国内外顶尖高校的留学精英，为承载留学梦想的广大学子提供**美、英、港、新等国家及地区的硕士**申请服务。
    ### 查看过往录取案例
    - 2024年录取战绩 [美国&英国篇](https://mp.weixin.qq.com/s/2STFt8xRnPWJgRzIoI73Yg) [香港&新加坡篇](https://mp.weixin.qq.com/s/CuRofPHatz7_UcbgZ3IZEA)
    - 2023年录取战绩 [2023Fall香港大学Offer雨](https://mp.weixin.qq.com/s/B3R_J0R0Dq6ZG_ryZu6YDw) [2023Fall圣路易斯华盛顿大学Offer雨](https://mp.weixin.qq.com/s/7LXi-L0bBI7ulyNPqTnaIg)
    - 2022年录取战绩 [美国篇上](https://mp.weixin.qq.com/s/BKEJE2cSODenKhDlshVtlg) [美国篇下](https://mp.weixin.qq.com/s/JGoOVcxqA1Ux0WnVPR-Zog) [英国&香港&新加坡](https://mp.weixin.qq.com/s/yRm91u2VEXZGxXV8YMuTXg)
    ### 想了解更多清流故事吗？
    - 清流专属校友会 [2024年新加坡校友会](https://mp.weixin.qq.com/s/3XsNOAe8bYHLY0LENwWFrA)
    - 学员就读体验 [哥伦比亚大学](https://mp.weixin.qq.com/s/M--UO3nq1NzUAnrMKfoetw) [南洋理工大学](https://mp.weixin.qq.com/s/T-QlUQPKCyRPvgEbn4RC9w)
    ### 当前办公地址
    - 🚩上海：黄浦区淮海中路300号K11大厦4208室
    - 🚩上海：杨浦区政通路177号万达广场C座2010室
    - 🚩北京：海淀区辉煌时代大厦三楼
    - 🚩成都：锦江区下东大街段199号睿东中心B座41楼
"""
)
