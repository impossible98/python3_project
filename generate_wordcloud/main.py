import os
from collections import Counter

from numpy import array

import jieba
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import ImageColorGenerator, WordCloud

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, 'dist')


def main():
    most_words = generate_wordcloud()
    generate_image(most_words)
    generate_html(most_words)


def generate_wordcloud():
    with open('report19.txt') as f:
        content = f.read()
    word_list = list(jieba.cut(content))
    words_count = Counter(word_list)
    most_words = words_count.most_common(128)
    most_words = [words for words in most_words if words[0]
                  not in ' ，、。“”（）！；的和是在要为以把了对中到有上不等更二从大\n']
    return most_words


def generate_image(most_words):
    dict_words = {}
    for words in most_words:
        dict_words[words[0]] = words[1]
    im = Image.open('party.png')
    wc = WordCloud(
        font_path='zhaozi.ttf',
        background_color='white',
        mask=array(im),
        max_font_size=100,
    )
    wc.generate_from_frequencies(dict_words)
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
    wc.to_file('dist/word_freq.jpg')


def generate_html(most_words):
    words_list = []
    count_list = []
    for word in most_words[:32]:
        words_list.append(word[0])
        count_list.append(word[1])

    option = """
    var option = {
        title: {
            text: '十九大工作报告',
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            data: ['报告词频']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01]
        },
        yAxis: {
            type: 'category',
            data: """ + str(words_list[::-1]) + """
        },
        series: [
            {
                name: '报告词频',
                type: 'bar',
                data: """ + str(count_list[::-1]) + """
            }
        ]
    };
    """

    header = """<html>
    <head>
        <meta charset="utf-8">
        <title>ECharts</title>
        <!-- 引入 echarts.js -->
        <script src="echarts.js"></script>
    </head>
    <body>
        <div id="showhere" style="width:800px; height:600px;"></div> 
        <script> 
        var myChart = echarts.init(document.getElementById('showhere'));
    """

    footer = """
    myChart.setOption(option);
    </script>
    </body>
    </html>
    """

    with open('dist/word_freq.html', 'w') as f:
        f.write(header + option + footer)


if __name__ == '__main__':
    main()
