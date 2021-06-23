import pandas as pd
import os
import json
from utils import parser
import re
import csv as CSV
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import numpy as np


tree_path = './data/Wired_NoC_unique_NOCS_DAC_DATE_ISCA_HiImpact_HPCA.txt'

nocs_path = './data/nocs'
nocs_path_format = './data/nocs/{}'
dac_path = './data/dac.csv'

stopwords_path = './data/stopwords-en.txt'
keywords_path = './data/nocs-topic-by-teacher'
keywords_path_format = './data/nocs-topic-by-teacher/{}'
dac_keywords_path = './data/dac-topic-by-teacher.csv'

exception = ['solution', 'algorithm', 'objective', 'level', 'technology', 'technique']


traning_data_files = [
	'./data/nocs/',
	'./data/dac.csv',
	# './data/date.csv',
	# './data/hpca.csv',
	# './data/hiImpact.csv',
	# './data/isca.csv'
]

training_standard_keywords_files = [
	'./data/nocs-topic-by-teacher/',
	'./data/dac-topic-by-teacher.csv',
	# './data/date-topic-by-teacher.csv',
	# './data/hpca-topic-by-teacher.csv',
	# './data/hiImpact-topic-by-teacher.csv',
	# './data/isca-topic-by-teacher.csv'
]


with open('./data/dictionary.json', encoding='utf-8') as f:
	dictionary = json.loads(f.read().lower())

with open(stopwords_path, encoding='utf-8') as f:
	stopwords = f.read().split()

subject_topic = parser.parse_topic(tree_path)
degree = {}


def dfs(node, deg):
	deg[node.topic] = deg.get(node.topic, 0) + len(node.children)
	for child in node.children:
		deg[child.topic] = 1
		dfs(child, deg)


def get_raw_data(files: list or str, has_year: bool=False):
	''' 获取titles， abstracts，full_texts

	:param files:
	:return:
	'''
	if type(files) == str:
		files = [files]

	years = []
	titles = []
	abstracts = []
	full_texts = []
	for file in files:
		# 是csv文件
		if os.path.isfile(file):
			csv = pd.read_csv(file)
			if has_year:
				years.extend(csv['year'].tolist())
			else:
				years.extend(['' for i in range(len(csv['title']))])
			titles.extend(csv['title'].tolist())
			abstracts.extend(csv['abstract'].tolist())
			full_texts.extend(csv['full_text'].tolist())
		# :是文件夹
		else:
			sub_files = os.listdir(file)
			for sub_file in sub_files:
				sub_file = os.path.join(file, sub_file)
				csv = pd.read_csv(sub_file)
				if has_year:
					years.extend(csv['year'].tolist())
				else:
					years.extend(['' for i in range(len(csv['title']))])
				titles.extend(csv['title'].tolist())
				abstracts.extend(csv['abstract'].tolist())
				full_texts.extend(csv['full_text'].tolist())

	return years, titles, abstracts, full_texts


def get_standard_keywords(files: list or str):
	''' 获取手打的标签

	:param files:
	:return:
	'''
	if not files:
		return {}

	if type(files) == str:
		files = [files]

	keywords = {}
	for file in files:
		# 是csv文件
		if os.path.isfile(file):
			csv = pd.read_csv(file)
			for title, kw in zip(csv['title'].tolist(), csv['topic_by_teacher'].tolist()):
				kw = str(kw).lower()
				if kw == 'nan':
					continue
				kw_list = [s.strip().split('-->') for s in re.split(r'[,，]', kw)]
				keywords[title] = list(set(sum(kw_list, [])))

		# 是文件夹
		else:
			sub_files = os.listdir(file)
			for sub_file in sub_files:
				sub_file = os.path.join(file, sub_file)
				csv = pd.read_csv(sub_file)
				for title, kw in zip(csv['title'].tolist(), csv['topic_by_teacher'].tolist()):
					kw = str(kw).lower()
					if kw == 'nan':
						continue
					kw_list = [s.strip().split('-->') for s in re.split(r'[,，]', kw)]
					keywords[title] = list(set(sum(kw_list, [])))

	return keywords


def count_word(dst, src):
	''' 统计词频

	:param dst:
	:param src:
	:return:
	'''
	return len(re.findall(f'\\b{dst}\\b', str(src), re.IGNORECASE))


def vectorizer(words, keywords, title, occ_t, occ_a):
	''' 转换成词向量

	:param words:
	:param keywords:
	:param title:
	:param occ_t:
	:param occ_a:
	:return:
	'''
	x, y = [], []
	for w in words:
		feature = dict()

		if w[0] in keywords.get(title, []):
			y.append(1)
		else:
			y.append(0)
		feature['tf'] = w[1]
		# feature['degree'] = degree[w[0]]

		# FIXME 暂时处理
		feature['degree'] = degree.get(w[0], 0)

		feature['length'] = len(w[0].split(' '))
		# feature['first_pos'] = first[w[0]]
		feature['occ_t'] = occ_t.get(w[0], False)
		feature['occ_a'] = occ_a.get(w[0], False)
		x.append(feature)
	return x, y


# title匹配字符模式
pattern = re.compile(r'\b\w+\b')


def compare_title(title, title1, pattern):
	title, title1 = [''.join(pattern.findall(x)).lower() for x in [title, title1]]

	#FIXME 应该使用相等而不是包含
	# return result_title.find(title) == 0
	return title1 == title


def find_title(title, titles, pattern):
	for t in titles:
		if compare_title(title, t, pattern):
			return t

	return None


def get_trainer(training_data_files: list or str, traning_data_files: list or str):
	''' 训练器

	:param training_data_files:
	:param training_standard_keywords_files:
	:return:
	'''
	years, titles, abstracts, full_texts = get_raw_data(training_data_files)
	training_keywords = get_standard_keywords(training_standard_keywords_files)

	X_train = []
	y_train = []
	num = 0
	idf = {}
	for title, abstract, text in zip(titles, abstracts, full_texts):
		title_in_standard_file = find_title(title, training_keywords.keys(), pattern)
		if not title_in_standard_file:
			continue

		# if title not in training_keywords.keys():
		#     continue

		if not type(text) == str:
			text = ''

		num += 1
		counter = {}
		first = {}
		occ_title = {}
		occ_abs = {}
		for subject in subjects:
			count = count_word(subject, text)
			pos = text.find(subject)
			first[subject] = pos if pos != -1 else float('inf')
			occ_title[subject] = count_word(subject, title) > 0
			occ_abs[subject] = count_word(subject, abstract) > 0
			if subject in dictionary:
				for word in dictionary[subject]:
					count += count_word(word, text)
					occ_title[subject] = count_word(word, title) > 0
					occ_abs[subject] = count_word(word, abstract) > 0
					pos = text.find(word)
					if pos != -1:
						first[subject] = min(first.get(subject), pos)
			counter[subject] = count
		for key, value in counter.items():
			if value > 0:
				idf[key] = idf.get(key, 0) + 1
		res = sorted(counter.items(), key=lambda x: x[1], reverse=True)
		res = list(filter(lambda x: x[1] > 30, res))
		_x, _y = vectorizer(res, training_keywords, title, occ_title, occ_abs)
		X_train.extend(_x)
		y_train.extend(_y)

	encoder = DictVectorizer()
	encoder.fit(X_train)
	X_train = encoder.transform(X_train).toarray()

	clf = SVC(class_weight='balanced', kernel='rbf', C=5.0)
	clf.fit(X_train, y_train)
	y_pred = clf.predict(X_train)
	target_names = ['no', 'yes']
	print(classification_report(y_train, y_pred, target_names=target_names))
	return clf, encoder


dfs(subject_topic, degree)

with open(tree_path) as f:
	subjects = [s.strip() for s in f.read().lower().split('\n') if s.strip() != '']
subjects = set(subjects[1:])


idf = {}
with open('./data/idf') as f:
	for line in f.readlines():
		w, v = line.strip().split(',')
		idf[w] = float(v)


# 利用nocs打好的标签生成训练器
# clf, encoder = get_trainer([nocs_path, dac_path], [keywords_path, dac_keywords_path])
clf, encoder = get_trainer(traning_data_files, training_standard_keywords_files)


def get_results(output_file: str, raw_data_files: list or str, standard_keywords_files: list or str=None):
	# years, titles, abstracts, full_texts = get_raw_data(raw_data_files, True)
	years, titles, abstracts, full_texts = get_raw_data(raw_data_files, False)
	standard_keywords = get_standard_keywords(standard_keywords_files)

	# 在需要打标签的论文title中出现的关键词全部保留
	keywords_in_title = {}
	for title in titles:
		keywords_in_title[title] = []
		for subject in subjects:
			if count_word(subject, title) > 0:
				keywords_in_title[title].append(subject)
			else:
				if subject in dictionary:
					for word in dictionary[subject]:
						if count_word(word, title) > 0:
							keywords_in_title[title].append(subject)
							break

	result_kp = []
	result_title = []
	result_title_in_standard_file = []
	precision = []
	recall = []
	for year, title, abstract, text in zip(years, titles, abstracts, full_texts):
		# FIXME 过滤掉没有打好标签的论文, 如果该论文打好标签了,
		#  获取topic-by-teacher.csv文件里面的title，后面需要通过这个title来获取standard keywords
		title_in_standard_file = find_title(title, standard_keywords.keys(), pattern)
		if not title_in_standard_file:
			print('paper has no standard_keywords')
			continue

		# if title not in standard_keywords.keys():
		#     print('paper has no standard_keywords')
		#     continue

		# FIXME 使用摘要来选词
		# text = abstract

		if not type(text) == str:
			text = ''

		counter = {}
		first = {}
		occ_title = {}
		occ_abs = {}
		for subject in subjects:
			count = count_word(subject, text)
			pos = text.find(subject)
			first[subject] = pos if pos != -1 else float('inf')
			occ_title[subject] = count_word(subject, title) > 0
			occ_abs[subject] = count_word(subject, abstract) > 0
			if subject in dictionary:
				for word in dictionary[subject]:
					count += count_word(word, text)
					pos = text.find(word)
					occ_title[subject] = count_word(word, title) > 0
					occ_abs[subject] = count_word(word, abstract) > 0
					if pos != -1:
						first[subject] = min(first.get(subject), pos)
			counter[subject] = count
		res = sorted(counter.items(), key=lambda x: x[1], reverse=True)
		res = list(filter(lambda x: x[1] > 30, res))
		# res = list(filter(lambda x: x[1] > 3, res))
		if len(res) == 0:
			# print('no words')
			continue
		# print(res)

		keyphrase = []
		if not len(res) == 0:
			x, y = vectorizer(res, standard_keywords, title, occ_title, occ_abs)
			x_train = encoder.transform(x).toarray()
			y_pred = clf.predict(x_train)
			keyphrase = [res[i][0] for i, pred in enumerate(y_pred) if pred == 1]

		# 没有打出标签
		if len(keyphrase) == 0:
			# print('no keywords')
			continue

		if len(keyphrase) > 0:
			# FIXME title出现的关键词全部保留
			keyphrase.extend(keywords_in_title[title])
			# FIXME 过滤一些不是节点的词
			keyphrase = list(set([k for k in keyphrase if k not in exception]))

		result_kp.append(','.join(keyphrase))

		result_title_in_standard_file.append(title_in_standard_file)
		result_title.append(title)

		# 计算准确率等
		num_true = 0
		for kp in keyphrase:
			# if kp in standard_keywords.get(title, []):
			if kp in standard_keywords[title_in_standard_file]:
				num_true += 1
		precision.append(num_true / len(keyphrase))

		if len(standard_keywords.get(title_in_standard_file, [])):
			recall.append(num_true / len(standard_keywords.get(title_in_standard_file, [])))
		else:
			recall.append(0)

	p = np.mean(precision)
	r = np.mean(recall)
	print(f'precision = {p}, recall = {r}, f1 = {2 * p * r / (p + r)}')
	output = {
		# 'year': years,
		# 'title': titles,
		'title': result_title,
		'keyword': result_kp,
		# 'standard': [','.join(standard_keywords.get(t, [])) for t in result_title_in_standard_file],
		# 'recall': recall
	}
	# print(len(years), len(titles), len(result_kp))
	cols = [ 'title', 'keyword']
	# pd.DataFrame(output).to_csv(output_file, index=False, columns=cols, encoding='utf_8_sig')

	# 准确率不为1的结果输出
	with open(output_file, 'w', encoding='utf-8-sig') as f:
		csv_writer = CSV.writer(f)
		csv_writer.writerow(['title', 'keyword', 'standard', 'precision'])

		for title, keyword, standard, p in zip(result_title, result_kp, [','.join(standard_keywords.get(t, [])) for t in result_title_in_standard_file], precision):
			if p < 1:
				csv_writer.writerow([title, keyword, standard, p])


if __name__ == '__main__':
	# get_results('./result/nocs.csv',
	#             ['./data/nocs/', './data/dac.csv'],
	#             ['./data/nocs-topic-by-teacher/', './data/dac-topic-by-teacher.csv'])

	# get_results('./result/date.csv', ['./data/date.csv'], ['./data/date-topic-by-teacher.csv'])
	# get_results('./result/isca.csv', ['./data/isca.csv'], ['./data/isca-topic-by-teacher.csv'])
	# get_results('./result/hiImpact.csv', ['./data/hiImpact.csv'], ['./data/hiImpact-topic-by-teacher.csv'])
	# get_results('./result/hpca.csv', ['./data/hpca.csv'], ['./data/hpca-topic-by-teacher.csv'])

	# get_results('./result/iccad.csv', ['./data/iccad.csv'])
	# get_results('./result/aspdac.csv', ['./data/aspdac.csv'])


	get_results('./result/all.csv',
	            [ './data/nocs/', './data/dac.csv',
	              './data/date.csv', './data/isca.csv',
	              './data/hiImpact.csv', './data/hpca.csv'
	              ],
	            [ './data/nocs-topic-by-teacher/', './data/dac-topic-by-teacher.csv',
	              './data/date-topic-by-teacher.csv', './data/isca-topic-by-teacher.csv',
	              './data/hiImpact-topic-by-teacher.csv', './data/hpca-topic-by-teacher.csv'
	              ])
#