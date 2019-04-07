import re

punctuation = '!,;:?"\''
def __removePunctuation(text):
    text = re.sub(r'[{}]+'.format(punctuation) ,'' ,text)
    return text.strip()
##########汉字数字转阿拉伯数字###########
common_used_numerals_tmp ={'零':0, '一':1, '二':2, '两':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '十':10, '百':100, '千':1000, '万':10000, '亿':100000000}
def __chinese2digits(uchars_chinese):
      total = 0
      r = 1              #表示单位：个十百千...
      for i in range(len(uchars_chinese) - 1, -1, -1):
        # print(uchars_chinese[i])
        val = common_used_numerals_tmp.get(uchars_chinese[i])
        if val >= 10 and i == 0:  #应对 十三 十四 十*之类
          if val > r:
            r = val
            total = total + val
          else:
            r = r * val
            #total =total + r * x
        elif val >= 10:
          if val > r:
            r = val
          else:
            r = r * val
        else:
          total = total + r * val
      return total


########################################

def __transperToStruc(path):
    structdata = []
    keys = ['name','sex','年龄','年级','班级','优秀科目','班主任','年级排名']
    data = open(path, encoding='utf8').readlines()
    for item in data:
        single = {}
        # 统一标点编码为英文
        item = item.replace('：',':')
        item = item.replace('，',',')
        item = item.replace(' ','')
        item = item.strip()
        if item[-1]==',':
            item = item[:-1]
        # 处理优秀科目间多余的符号
        index1 = item.index("优秀科目:")
        # 依据不同的称呼划分
        if item.find(',班主任')!=-1:
            index2 = item.index(',班主任')
        else:
            index2 = item.index(',老师')
        clas = __removePunctuation(item[(index1+5):index2])

        temp1 = item[:(index1+5)]+clas+item[index2:]
        temp2 = temp1.split(',')

        j=0
        for i in range(len(temp2)):
            if j>len(temp2):
                j=0
            if '班级' in temp2[i] or '班别' in temp2[i]:
                tmpinner=2
                innerindex1 = temp2[i].split(':')[1].index('年')
                if '年级' not in temp2[i].split(':')[1]:
                    tmpinner = 1
                innerindex2 = temp2[i].split(':')[1].find('班',innerindex1)
                single[keys[j]] = temp2[i].split(':')[1][:innerindex1]
                j+=1
                single[keys[j]] = temp2[i].split(':')[1][(innerindex1+tmpinner):(innerindex2)]
            else:
                single[keys[j]] = temp2[i].split(':')[1]
            j+=1
        structdata.append(single)
    return structdata


def __processAge(structdata):
    result = []
    tmp = ['年级','班级','年龄','年级排名']
    tmp1 = {'male':'男','female':'女'}
    for i in structdata:
        if 'male' in i['sex']:
            i['sex']='男'
        if 'female' in i['sex']:
            i['sex']='女'
        if '岁' in i['年龄']:
            i['年龄']=i['年龄'][:-1]
        if '第' in i['年级排名']:
            i['年级排名']=i['年级排名'][1:]
        for index in tmp:
            if i[index].isdigit():
                i[index]=i[index]
            else:
                i[index] = __chinese2digits(i[index])
        result.append(i)
    return result

def __processClass(result):
    dict = {'语':'语文','数':'数学','英':'英语','政':'政治','历':'历史','地':'地理','物':'物理','化':'化学','生':'生物'}

    for item in result:
        se = []
        for i in dict.keys():
            if i in item['优秀科目']:
                se.append(dict[i])
        item['优秀科目'] = se
    return result
""""""

def process_text(path):
    struct_data = __transperToStruc(path)
    result = __processClass(__processAge(struct_data))
    return result

"""
依据平均排名判断班级优劣
"""
def ranking(result):
    best = {}
    count = {}
    ranking = []
    for i in result:
        if i['班级'] in best.keys():
            best[i['班级']]+=int(i['年级排名'])
            count[i['班级']] += 1
        else:
            best[i['班级']] = int(i['年级排名'])
            count[i['班级']] = 1

    ranking = [best[i]/count[i] for i in best.keys()]
    cla = best.keys()
    dic = dict(map(lambda x, y: [x, y], cla, ranking))
    dic1 = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    return dic1


"""
processtext  an API which receives the text file and returns the structured data
ranking an API for analyzing the ranking, returning the best class
"""

