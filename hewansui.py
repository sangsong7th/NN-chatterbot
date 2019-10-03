import jieba
import jieba.posseg as psg
import re



def cixing_biaozhu(cixing_flag,cixingmap):#如果有词性不在词性表内就加入，反则跳过
	flag=0#词性有重复的标注flag
	for i in cixingmap.keys():
		if cixing_flag!=i:#如果比对过程中 不等与 就pass
			pass

		if cixing_flag==i:#如果有相同的就置为一 并break
			flag=1
			break
	if flag == 0:
		cixingmap[cixing_flag]=len(cixingmap)+1
	return cixingmap



				

cixingmap={}
with open("F:\\python\\chatbotcorpus\\xiaohuangji.tsv",'r',encoding = 'utf-8') as fp:#这个是打开训练数据文件 构建词性表
	for i in fp.readlines():
		for j in psg.cut(i):
			print(j.word,j.flag)
			cixingmap=cixing_biaozhu(j.flag,cixingmap)
			print(cixingmap)
flag=1		
with open("F:\\python\\chatbotcorpus\\cixing_biaozhu",'w',encoding = 'utf-8') as fp:#词性表构建完成 后写入
	for i in cixingmap.keys():
		fp.write(i+'\t'+str(flag)+'\n')
		flag=flag+1

