from matplotlib.figure import Figure
from numpy import NaN
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from PIL import Image
import random
import pandas as pd


def readCSV():
    path = r'C:\Users\fathu\Downloads\data (17).csv'
    df = pd.read_csv(path)
    df.replace("", NaN, inplace=True)
    df.dropna(inplace=True)
    return df


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(90, 100)


def WORDCLOUD(df):
    file = " ".join(str(v) for v in df['clean text'])
    
    WC = WordCloud(
        font_path='scripts/static/bootstrap/font/AdobeCleanLight.otf',
        collocations=False,
        max_words=len(df),
        width=560,
        height=315,
        background_color="rgba(255, 255, 255, 0)", mode="RGBA"
    ).generate(file).recolor(color_func=grey_color_func, random_state=3)
    

    img = io.BytesIO()
    WC.to_image().save(img, 'PNG')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    
    
    return img_base64
    
    
