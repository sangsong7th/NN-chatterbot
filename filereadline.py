import re

r_one=re.compile(r'(.{0,1000}.)\t')
r_two=re.compile(r'\t(.{0,1000}.)')
with open("F:\\python\\chatbotcorpus\\chatterbot.tsv",'r',encoding = 'utf-8') as fp:
	for i in fp.readlines():
		r1=r_one.findall(i)
		r2=r_two.findall(i)


with open("F:\\python\\chatbotcorpus\\chatterbot.cbc",'w',encoding = 'utf-8') as wfp:
	for i in raintset:
		wfp.write(i+'\n')


	
