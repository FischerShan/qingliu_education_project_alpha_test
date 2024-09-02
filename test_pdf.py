import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import tempfile

# 准备数据框
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [24, 27, 22, 32],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']}
df = pd.DataFrame(data)

# 显示数据框
st.write("### 数据框展示")
st.dataframe(df)


# 函数：生成带水印的PDF
def create_pdf_with_watermark(dataframe, watermark_path):
    # 创建临时文件
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')

    # 使用reportlab生成PDF
    c = canvas.Canvas(tmp_file.name, pagesize=letter)
    width, height = letter

    # 设置字体和字体大小
    c.setFont("Helvetica", 10)

    # 添加水印图片
    watermark = ImageReader(watermark_path)
    c.drawImage(watermark, width - 150, height - 150, mask='auto', preserveAspectRatio=True)

    # 在PDF中添加表格内容
    textobject = c.beginText(50, height - 100)
    textobject.setTextOrigin(50, height - 50)
    for col in dataframe.columns:
        textobject.textLine(f"{col:<10}")

    for index, row in dataframe.iterrows():
        line = " ".join([f"{str(x):<10}" for x in row])
        textobject.textLine(line)

    c.drawText(textobject)
    c.showPage()
    c.save()

    return tmp_file.name


# 上传水印图片
uploaded_file = st.file_uploader("上传水印图片", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # 按钮：点击生成PDF
    if st.button("下载为PDF"):
        pdf_path = create_pdf_with_watermark(df, uploaded_file)
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="下载PDF文件",
                data=file,
                file_name="dataframe_with_watermark.pdf",
                mime="application/pdf"
            )
