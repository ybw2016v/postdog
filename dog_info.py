#!python3
import re
import time

import requests as r

conf_file = open('./list.conf', 'r')
conf_cont = conf_file.readlines()
conf_file.close()

timefile=open('./time.txt','r')
dog_time=int(timefile.read())
timefile.close()

SKEY=''
tiddog=time.strftime("%Y-%m-%d", time.localtime())

# class ()

dog_re_p = re.compile('"(.*)"')


class pre_dog_info(object):
    name = ''
    JinKai = ''
    ZuoShou = ''
    ZuiDi = ''
    ZuiGao = ''
    Xianjia = ''
    Chengjiao = ''
    RiQi = ''
    Time = ''

    def __init__(self, dog_str, code):
        pre_dog = dog_str.split(',')
        self.Code = code
        self.name = pre_dog[0]
        self.JinKai = pre_dog[1]
        self.ZuoShou = pre_dog[2]
        self.Xianjia = pre_dog[3]
        self.ZuiGao = pre_dog[4]
        self.ZuiDi = pre_dog[5]
        self.Chengjiao = str(float(pre_dog[9])/10000)+'万'
        self.RiQi = pre_dog[30]
        self.Time = pre_dog[31]
        self.ChengBen = '-'
        self.BiLi = '-'

    def cal(self, cb_str):
        self.ChengBen = cb_str
        cb = float(cb_str)
        self.BiLi = '{:.4%}'.format((float(self.Xianjia)-cb)/cb)

    def toStr(self):
        strdog = '**名称**:{0} {1}\n\n现价:**{2}** 昨收:{3} 今开:{4}\n\n最高:{5} 最低:{6} 成交:{7}\n\n成本:{8} 比例 :**{9}**\n\n![分时图](https://image.sinajs.cn/newchart/min/n/{1}.png)\n\n![K线图](https://image.sinajs.cn/newchart/daily/n/{1}.png)\n\n{10} {11} '.format(
            self.name, self.Code, self.Xianjia, self.ZuoShou, self.JinKai, self.ZuiGao, self.ZuiDi, self.Chengjiao, self.ChengBen, self.BiLi, self.RiQi, self.Time)
        return strdog


def get_info(dog_name):
    res_dog = r.get('https://hq.sinajs.cn/list='+dog_name)
    # print(res_dog.text)
    res_dog_p = dog_re_p.findall(res_dog.text)
    return res_dog_p
def send_dog(t,c):
    url='https://sc.ftqq.com/'+SKEY+'.send'
    can={'desp':t,'text':c}
    dog_res=r.post(url,params=can)
    print(dog_res.text)
    pass

# yyu=get_info(conf_cont[0].split(' ')[0])
# ee=pre_dog_info(yyu[0],conf_cont[0].split(' ')[0])
# ee.cal(conf_cont[0].split(' ')[1].strip())
# print(ee.toStr())
# print(conf_cont[1].split(' ')[1])
bitime=0
outstr = ''
for dog_item in conf_cont:
    dog_sp = dog_item.split(' ')
    gdog = get_info(dog_sp[0])
    dog_pa = pre_dog_info(gdog[0], dog_sp[0])
    if len(dog_sp) == 2:
        dog_pa.cal(dog_sp[1].strip())
    bitime=max(int(dog_pa.RiQi.replace('-','')),bitime)
    # print(bitime)
    outstr = outstr+dog_pa.toStr()+'\n\n'
if dog_time<bitime:
    print('需要发送')
    ff=open('./time.txt','w')
    ff.write(str(bitime))
    ff.close()
else:
    print('不需要')
send_dog(outstr,tiddog+'证券汇报')
print(outstr)
