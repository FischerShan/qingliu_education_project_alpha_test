import streamlit as st
import streamlit_authenticator as stauth

import numpy as np
import pandas as pd
import base64
from pathlib import Path

st.set_page_config(page_title="数据管理平台", page_icon="💾", layout="wide", initial_sidebar_state="expanded")

# 用户数据
names = ['Vince', 'Admin']
usernames = ['vince', 'admin']
passwords = ['123', '123']

# 加密密码
hashed_passwords = stauth.Hasher(passwords).generate()

# 创建凭证字典
credentials = {
    'usernames': {
        usernames[i]: {'name': names[i], 'password': hashed_passwords[i]}
        for i in range(len(usernames))
    }
}

# 创建认证对象
authenticator = stauth.Authenticate(credentials, 'cookie_name', 'signature_key', cookie_expiry_days=0)


# 图片压缩和解码
def img_to_bytes(img_path):

    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


# 用户登录逻辑
def login():

    if 'authentication_status' not in st.session_state:

        st.session_state.authentication_status = None

    if st.session_state.authentication_status is None:

        name, authentication_status, username = authenticator.login(key='Login', location='main')

        # 处理登录结果
        if authentication_status:

            st.session_state.authentication_status = True
            st.session_state.username = username
            st.session_state.name = name

        elif authentication_status == False:

            st.error('Username/password is incorrect')

        elif authentication_status == None:

            st.warning('Please enter your username and password')


# 主程序逻辑
def main():

    # 显示主界面
    if st.session_state.authentication_status:

        st.sidebar.markdown('''<img src='data:image/png;base64,{}' class='img-fluid' width=221 height=47>'''.format(
            img_to_bytes("./source_pictures/logo.png")), unsafe_allow_html=True)

        st.sidebar.caption("")
        st.sidebar.caption("更多信息请关注“清流留学咨询”微信公众号")
        st.sidebar.caption("Developed by 清流教育")
        st.sidebar.caption("版权所有©清流教育")

    else:
        login()


if __name__ == "__main__":
    main()