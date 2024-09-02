import base64
import math
from decimal import Decimal
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit_authenticator as stauth

st.set_page_config(page_title="案例分析平台", page_icon="📝", layout="wide", initial_sidebar_state="expanded")

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
        # 设置侧边栏样式
        st.sidebar.markdown('''<img src='data:image/png;base64,{}' class='img-fluid' width=221 height=47>'''.format(
            img_to_bytes("./source_pictures/logo.png")), unsafe_allow_html=True)

        st.sidebar.title("Project Alpha Navigation")
        st.sidebar.caption("Developed by 清流教育")
        st.sidebar.caption("更多留学故事请关注“清流教育”微信公众号")

        # 读取数据
        df = pd.read_excel("./data_test/data_total.xlsx", sheet_name="Sheet1", dtype="str")
        df_character = pd.read_excel("./data_test/argument_and_explanation.xlsx", sheet_name="Sheet1", dtype="str")

        # 为容器添加内嵌页
        tab1, tab2 = st.tabs(["🖼️ 过往案例展示", "🔯 录取维度分析"])

        # 第一个内嵌页内容
        with tab1:
            # 对内嵌页进行分栏
            col1, col2 = st.columns(2)

            # 第一个栏的内容
            with col1:
                # 多选设置申请国家或地区
                options_university_2_district = st.multiselect("请选择申请的国家或地区：",
                                                               ("中国香港", "新加坡", "美国", "英国", "加拿大", "欧洲"),
                                                               ("中国香港", "新加坡", "美国"))

                # 多选设置学校分类
                options_university_1_level = st.multiselect("请选择学校类型：",
                                                            ("985", "211财经", "211", "双非", "中外合办", "美本",
                                                             "加本", "英本", "澳本", "港本", "海本"),
                                                            ("211财经", "211"))

            # 第二个栏的内容
            with col2:
                # 多选设置申请学校分类
                options_university_2_level = st.multiselect("请选择申请学校的类别：",
                                                            ("美国Top30", "美国Top50", "美国其它", "英国G5",
                                                             "英国王曼爱华", "英国其它", "香港前三", "香港四五",
                                                             "新加坡前二", "新加坡其它", "欧洲", "北美其它"),
                                                            ("美国Top30", "香港前三", "新加坡前二"))

                # 滑动条设置标化绩点
                options_gpa_standard = st.slider(label="请选择标准化绩点（4.0满绩）：", min_value=1.0, max_value=4.0,
                                                 value=(3.0, 4.0))

            # 对内嵌页进行分栏
            col3, col4 = st.columns([2, 1])

            # 第三个栏的内容
            with col3:
                # 多选设置申请学校专业
                options_major_2_category = st.multiselect("请选择申请的专业类型：",
                                                          ("管理", "金融", "营销", "信息系统管理", "工业工程与运筹学"),
                                                          ("管理", "金融", "营销"))

            # 第四个栏的内容
            with col4:
                # 选择展示的列
                options_column = st.multiselect("请选择其它要展示的字段：",
                                                ("绩点或分数", "外方学校", "中外合办形式", "雅思或托福", "GRE或GMAT",
                                                 "实习和科研段数", "申请学校类别", "申请专业类别", "奖学金"))
                # 必须展示的列
                list_required = ["学员", "学校", "学校类别", "专业", "标准化绩点", "是否中外合办", "托雅分数",
                                 "G考分数", "地区", "申请学校", "申请专业", "是否提前批"]
                # 汇总成最终展示的列
                list_selected = list(options_column)
                list_column = list_required + list_selected
                list_column = df_character[df_character["chinese_external"].isin(list_column)]["characters"].tolist()

            # # 单选设置所在学校
            # university_1_list = df["university_1"].dropna().drop_duplicates().tolist()
            # university_1_list = [x for x in university_1_list if x not in [None, '']]
            # university_1_list = sorted(university_1_list)
            # option_university_1 = st.selectbox("请选择所在的学校：", tuple(university_1_list))

            # 创建展示数据框
            df_external_case = df

            # 转换读取数据的数据格式
            df_external_case["gpa_standard"] = df_external_case["gpa_standard"].astype(float)
            df_external_case["gpa_standard"] = df_external_case["gpa_standard"].round(2)

            # 逻辑判断控件触发后的数据
            df_external_case = df_external_case[df_external_case["university_2_district"].isin(
                list(options_university_2_district))] if len(options_university_2_district) > 0 else df_external_case

            df_external_case = df_external_case[df_external_case["university_1_level"].isin(
                list(options_university_1_level))] if len(options_university_1_level) > 0 else df_external_case

            df_external_case = df_external_case[df_external_case["university_2_level"].isin(
                list(options_university_2_level))] if len(options_university_2_level) > 0 else df_external_case

            df_external_case = df_external_case[(df_external_case["gpa_standard"] > list(options_gpa_standard)[0]) & (
                    df_external_case["gpa_standard"] < list(options_gpa_standard)[1])] if len(
                options_gpa_standard) > 0 else df_external_case

            df_external_case = df_external_case[df_external_case["major_2_category"].isin(
                list(options_major_2_category))] if len(options_major_2_category) > 0 else df_external_case

            # df_external_case = df_external_case[df_external_case["university_1"] == option_university_1] if len(
            #     list(option_university_1)) > 0 else df_external_case

            # 对展示的列名进行更名
            column_dict = df_character.set_index("characters")["chinese_external"].to_dict()
            df_external_case = df_external_case.loc[:, list_column].rename(columns=column_dict)

            # 对展示的数据框变成字符型
            df_external_case = df_external_case.astype(str)

            # 展示最后的数据框
            st.dataframe(df_external_case, height=500, use_container_width=True,
                         selection_mode="multi-column", hide_index=True)

            # GPA分类还是数值型
            # 专业分类，要不要2级分类
            # 学校档次要不要继续划分
            # 要不要打上“硕士申请”标签

        # 第二个内嵌页内容
        with tab2:
            # 对内嵌页进行分栏
            col5, col6 = st.columns(2)

            # 第一个栏的内容
            with col5:
                # 多选输入申请国家或地区
                input_university_2_level = st.multiselect("请选择希望申请学校类别（包括国家或地区）：",
                                                          ("美国Top30", "美国Top50", "美国其它", "英国G5",
                                                           "英国王曼爱华", "英国其它", "香港前三", "香港四五",
                                                           "新加坡前二", "新加坡其它", "欧洲", "北美其它"),
                                                          ("美国Top30", "香港前三", "新加坡前二"))

            # 第一个栏的内容
            with col6:
                # 多选输入申请的专业类型
                input_major_2_category = st.multiselect("请选择希望申请的专业类型：",
                                                        ("管理", "金融", "营销", "信息系统管理", "工业工程与运筹学"))

            # 对内嵌页进行分栏
            col7, col8 = st.columns([1.5, 4])

            # 第一个栏的内容
            with col7:
                # 创建多条件组合提交的表单
                with st.form(key="input_info_form"):
                    # 多选输入学校分类
                    input_university_1_level = st.selectbox("请选择学校类型：",
                                                            ("985", "211财经", "211", "双非", "中外合办", "美本",
                                                             "加本", "英本", "澳本", "港本", "海本"),
                                                            index=1)

                    # 多选输入专业类型
                    input_major_1_category = st.selectbox("请选择专业类型：",
                                                          ("金融类", "数学类", "国贸", "管理科学与工程"),
                                                          index=0)

                    # 数字框输入绩点
                    input_gpa_standard = st.number_input(label="请输入满绩为4.0的绩点：", min_value=0.00, max_value=4.00,
                                                         value=3.50, placeholder="Type a number", format="%0.2f",
                                                         help="请输入满绩为4.0的绩点，若绩点不是4.0制，请进行转换")

                    # 数字框输入托雅分数
                    input_t_score = st.number_input(label="请输入托雅分数：", min_value=0.0, max_value=120.0, step=0.5,
                                                    value=7.0, placeholder="Type a number", format="%0.1f",
                                                    help="请输入托福或者雅思考试分数")

                    # 数字框输入G考分数
                    input_g_score = st.number_input(label="请输入G考分数：", min_value=0, max_value=1000, step=1,
                                                    value=320, placeholder="Type a number", format="%d",
                                                    help="请输入GRE或GMAT考试分数")

                    # 数字框输入实习和科研段数
                    input_experience_num = st.number_input(label="请输入科研或实习段数：", min_value=0, step=1,
                                                           value=4, placeholder="Type a number", format="%d",
                                                           help="请输入科研或实习段数总数，包括论文、研究助理和实习等")

                    # 设置提交按钮，供触发提交数据
                    submit_button = st.form_submit_button(label="Submit")

            # 创建绘图的数据框
            df_external_plot = df

            # 转换读取数据的数据格式
            df_external_plot["gpa_standard"] = df_external_plot["gpa_standard"].astype(float)
            df_external_plot["gpa_standard"] = df_external_plot["gpa_standard"].round(2)

            df_external_plot["experience_num"] = df_external_plot["experience_num"].astype(int)

            df_external_plot["t_score"] = df_external_plot["t_score"].replace("无语言", "0")
            df_external_plot["t_score"] = df_external_plot["t_score"].astype(float)
            df_external_plot["t_score"] = df_external_plot["t_score"].round(1)

            df_external_plot["g_score"] = df_external_plot["g_score"].replace("无G", "0")
            df_external_plot["g_score"] = df_external_plot["g_score"].astype(int)

            # 逻辑判断控件触发后计算展示数据
            df_external_plot = df_external_plot[df_external_plot["university_2_level"].isin(
                list(input_university_2_level))] if len(input_university_2_level) > 0 else df_external_plot

            df_external_plot = df_external_plot[df_external_plot["major_2_category"].isin(
                list(input_major_2_category))] if len(input_major_2_category) > 0 else df_external_plot

            # 第二个栏的内容
            with col8:
                # 对内嵌页进行分栏
                col8_1, col8_2, col8_3, col8_4 = st.columns(4)

                # 第一个栏的内容
                with col8_1:
                    # 计算数据库中平均绩点
                    data_average_gpa = df_external_plot["gpa_standard"].dropna().mean()
                    data_average_gpa = float(
                        Decimal(data_average_gpa).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))

                    # 生成展示的文本
                    gpa_message = f"""
                                平均录取GPA {data_average_gpa:.2f}\n
                                侧边输入GPA {input_gpa_standard:.2f}
                                """

                    # 显示带有换行的文本
                    st.success(gpa_message)

                # 第二个栏的内容
                with col8_2:
                    # 计算数据库中平均托雅分数
                    if input_t_score == 0.0:
                        data_average_t_score = 0.0

                    elif (input_t_score > 0.0) and (input_t_score < 10.0):
                        data_average_t_score = df_external_plot[df_external_plot["t_test"] == "雅思"][
                            "t_score"].dropna().mean()
                        data_average_t_score = float(
                            Decimal(data_average_t_score).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))

                    elif (input_t_score > 10.0) and (input_t_score <= 120.0):
                        data_average_t_score = df_external_plot[df_external_plot["t_test"] == "托福"][
                            "t_score"].dropna().mean()
                        data_average_t_score = float(
                            Decimal(data_average_t_score).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))

                    # 生成展示的文本
                    t_score_message = f"""
                                    平均录取托雅 {data_average_t_score:.1f}\n
                                    侧边输入托雅 {input_t_score:.1f}
                                    """

                    # 显示带有换行的文本
                    st.warning(t_score_message)

                # 第三个栏的内容
                with col8_3:
                    # 计算数据库中平均G考分数
                    if input_g_score == 0:
                        data_average_g_score = 0

                    elif (input_g_score > 0) and (input_g_score <= 340):
                        data_average_g_score = df_external_plot[df_external_plot["g_test"] == "GRE"][
                            "g_score"].dropna().mean()
                        data_average_g_score = int(
                            Decimal(data_average_g_score).quantize(Decimal("0"), rounding="ROUND_HALF_UP"))

                    elif (input_g_score > 340) and (input_g_score <= 800):
                        data_average_g_score = df_external_plot[df_external_plot["g_test"] == "GMAT"][
                            "g_score"].dropna().mean()
                        data_average_g_score = int(
                            Decimal(data_average_g_score).quantize(Decimal("0"), rounding="ROUND_HALF_UP"))

                    # 生成展示的文本
                    g_score_message = f"""
                                    平均录取G考 {data_average_g_score:d}\n
                                    侧边输入G考 {input_g_score:d}
                                    """

                    # 显示带有换行的文本
                    st.error(g_score_message)

                # 第四个栏的内容
                with col8_4:
                    # 计算数据库中平均经历段数
                    data_average_experience_num = df_external_plot["experience_num"].dropna().mean()
                    data_average_experience_num = int(
                        Decimal(data_average_experience_num).quantize(Decimal("0"), rounding="ROUND_HALF_UP"))

                    # 生成展示的文本
                    experience_num_message = f"""
                                            平均录取经历数 {data_average_experience_num:d}\n
                                            侧边输入经历数 {input_experience_num:d}
                                            """

                    # 显示带有换行的文本
                    st.info(experience_num_message)

                # 显示雷达比较图
                # 创建雷达图的维度和数据
                categories = ["绩点", "托雅", "G考", "学校", "专业", "经历"]
                values_internal = []  # 第一组数据
                values_external = []  # 第二组数据

                # 计算数据库中每个维度的分数
                # 绩点维度 (y=0.7*x^(1/2)+0.3，构造边际递减)
                max_value = df_external_plot["gpa_standard"].dropna().max()
                min_value = df_external_plot["gpa_standard"].dropna().min()

                score_value = (max_value - min_value) / (4.00 - min_value)
                score_value = 0 if score_value <= 0 else score_value
                score_value = math.sqrt(score_value) * 0.7 + 0.3
                score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                values_internal = values_internal + [score_value * 100.00]

                score_value = (input_gpa_standard - min_value) / (4.00 - min_value)
                score_value = 0 if score_value <= 0 else score_value
                score_value = math.sqrt(score_value) * 0.7 + 0.3
                score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                values_external = values_external + [min(score_value * 100.00, 100)]

                # 托雅维度 (y=0.6*x^(1/2)+0.4，构造边际递减)
                if input_t_score == 0.0:
                    values_internal = values_internal + [50]
                    values_external = values_external + [50]

                elif (input_t_score > 0.0) and (input_t_score < 10.0):
                    max_value = df_external_plot[df_external_plot["t_test"] == "雅思"]["t_score"].dropna().max()
                    min_value = df_external_plot[df_external_plot["t_test"] == "雅思"]["t_score"].dropna().min()

                    score_value = (max_value - min_value) / (9.0 - min_value)
                    score_value = 0 if score_value <= 0 else score_value
                    score_value = math.sqrt(score_value) * 0.6 + 0.4
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_internal = values_internal + [score_value * 100.00]

                    score_value = (input_t_score - min_value) / (9.0 - min_value)
                    score_value = 0 if score_value <= 0 else score_value
                    score_value = math.sqrt(score_value) * 0.6 + 0.4
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_external = values_external + [min(score_value * 100.00, 100)]

                elif (input_t_score > 10.0) and (input_t_score <= 120.0):
                    max_value = df_external_plot[df_external_plot["t_test"] == "托福"]["t_score"].dropna().max()
                    min_value = df_external_plot[df_external_plot["t_test"] == "托福"]["t_score"].dropna().min()

                    score_value = (max_value - min_value) / (120.0 - min_value)
                    score_value = 0 if score_value <= 0 else score_value
                    score_value = math.sqrt(score_value) * 0.6 + 0.4
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_internal = values_internal + [score_value * 100.00]

                    score_value = (input_t_score - min_value) / (120.0 - min_value)
                    score_value = 0 if score_value <= 0 else score_value
                    score_value = math.sqrt(score_value) * 0.6 + 0.4
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_external = values_external + [min(score_value * 100.00, 100)]

                # G考维度 (y=0.7*x^(1/2)+0.3，构造边际递减)
                if input_g_score == 0.0:
                    values_internal = values_internal + [50]
                    values_external = values_external + [50]

                elif (input_g_score > 0) and (input_g_score <= 340):
                    max_value = df_external_plot[df_external_plot["g_test"] == "GRE"]["g_score"].dropna().max()
                    min_value = df_external_plot[df_external_plot["g_test"] == "GRE"]["g_score"].dropna().min()

                    score_value = (max_value - min_value) / (340 - min_value)
                    score_value = 0 if score_value <= 0 else score_value
                    score_value = math.sqrt(score_value) * 0.7 + 0.3
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_internal = values_internal + [score_value * 100.00]

                    score_value = (input_g_score - min_value) / (340 - min_value)
                    score_value = 0 if score_value <= 0 else score_value
                    score_value = math.sqrt(score_value) * 0.7 + 0.3
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_external = values_external + [min(score_value * 100.00, 100)]

                elif (input_g_score > 340) and (input_g_score <= 800):
                    max_value = df_external_plot[df_external_plot["g_test"] == "GMAT"]["g_score"].dropna().max()
                    min_value = df_external_plot[df_external_plot["g_test"] == "GMAT"]["g_score"].dropna().min()

                    score_value = (max_value - min_value) / (800 - min_value)
                    score_value = 0 if score_value <= 0 else score_value
                    score_value = math.sqrt(score_value) * 0.7 + 0.3
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_internal = values_internal + [score_value * 100.00]

                    score_value = (input_g_score - min_value) / (800 - min_value)
                    score_value = 0 if score_value <= 0 else score_value
                    score_value = math.sqrt(score_value) * 0.7 + 0.3
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_external = values_external + [min(score_value * 100.00, 100)]

                # 学校维度 (直接赋值)
                values_internal = values_internal + [95]

                if input_university_1_level == "985":
                    score_value = 0.85
                elif input_university_1_level == "211财经":
                    score_value = 0.70
                elif input_university_1_level == "211":
                    score_value = 0.65
                elif input_university_1_level == "双非":
                    score_value = 0.40
                elif input_university_1_level == "中外合办":
                    score_value = 0.80
                elif input_university_1_level == "美本":
                    score_value = 0.90
                elif input_university_1_level == "加本":
                    score_value = 0.75
                elif input_university_1_level == "英本":
                    score_value = 0.70
                elif input_university_1_level == "澳本":
                    score_value = 0.60
                elif input_university_1_level == "港本":
                    score_value = 0.80
                elif input_university_1_level == "海本":
                    score_value = 0.75

                score_value = 0 if score_value <= 0 else score_value
                score_value = math.sqrt(score_value) * 0.8 + 0.2
                score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                values_external = values_external + [min(score_value * 100.00, 100)]

                # 专业维度 (y=0.8*x^2+0.2，构造边际递增)
                major_1_frequency_df = df_external_plot["major_1_category"].value_counts().reset_index()
                major_1_frequency_df.columns = ["major_1_str", "frequency"]
                major_1_frequency_df = major_1_frequency_df.sort_values(by='frequency',
                                                                        ascending=False).reset_index(drop=True)

                score_value = major_1_frequency_df["frequency"].sum() - major_1_frequency_df.loc[0:0, "frequency"] / 2
                score_value = math.pow(score_value, 2) * 0.8 + 0.2
                score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                values_internal = values_internal + [min(score_value * 100.00, 100)]

                target_index = major_1_frequency_df.index[major_1_frequency_df["major_1_str"] ==
                                                          input_major_1_category].tolist()

                if target_index:
                    score_value = major_1_frequency_df.loc[target_index[0] + 1:, "frequency"].sum()
                    score_value = score_value + major_1_frequency_df.loc[target_index[0]:target_index[0],
                                                "frequency"] / 2
                    score_value = math.pow(score_value, 2) * 0.8 + 0.2
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_external = values_external + [min(score_value * 100.00, 100)]

                else:
                    score_value = 0.0
                    score_value = math.pow(score_value, 2) * 0.8 + 0.2
                    score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                    values_external = values_external + [min(score_value * 100.00, 100)]

                # 经历维度 (y=0.8*x^(1/2)+0.2，构造边际递减)
                max_value = df_external_plot["experience_num"].dropna().max()
                min_value = df_external_plot["experience_num"].dropna().min()

                score_value = (max_value - min_value) / (max_value - min_value)
                score_value = 0 if score_value <= 0 else score_value
                score_value = math.sqrt(score_value) * 0.8 + 0.2
                score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                values_internal = values_internal + [score_value * 100]

                score_value = (input_experience_num - min_value) / (max_value - min_value)
                score_value = 0 if score_value <= 0 else score_value
                score_value = math.sqrt(score_value) * 0.8 + 0.2
                score_value = float(Decimal(score_value).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                values_external = values_external + [min(score_value * 100.00, 100)]

                # 对内嵌页进行分栏
                col8_5, col8_6 = st.columns([3, 1])

                # 第五个栏的内容
                with col8_5:
                    # 绘制分析雷达图
                    # 创建雷达图
                    fig = go.Figure()

                    # 添加内部数据库打分
                    fig.add_trace(go.Scatterpolar(r=values_internal, theta=categories, fill="toself",
                                                  name="内部申请信息", line=dict(color="#002fa7"),
                                                  fillcolor="rgba(28, 83, 181, 0.5)"))

                    # 添加学员输入打分
                    fig.add_trace(go.Scatterpolar(r=values_external, theta=categories, fill='toself',
                                                  name="输入申请信息", line=dict(color="#FFA500"),
                                                  fillcolor="rgba(255, 222, 89, 0.5)"))

                    # 更新布局
                    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[50, 100])),
                                      legend=dict(orientation="v", x=0, y=1.2),
                                      margin=dict(l=30, r=0, t=25, b=25),
                                      width=500, height=450, showlegend=True)

                    # 在Streamlit中显示雷达图
                    st.plotly_chart(fig, use_container_width=True)

                # # 第六个栏的内容
                # with col8_6:
                #     # 使用 HTML 和 CSS 创建一个带边框的内容块
                #     st.markdown(
                #         """
                #         <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                #             <h4 style="color: #4CAF50;">带边框的内容</h4>
                #             <p>这是一个示例文本，展示了如何在 Streamlit 中创建带边框的内容块。</p>
                #         </div>
                #         """,
                #         unsafe_allow_html=True
                #     )

    else:
        login()


if __name__ == "__main__":
    main()
