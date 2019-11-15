import requests
import re
import glob
from openpyxl import Workbook, load_workbook
import hashlib
from PIL import Image
import os, sys

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


def deserial(first):
	'''
	Deserealize all data from each of data['goal_items']
	
	Returns:
	
	outside_text_kanji, outside_text_hrkt, outside_text_eng, outside_text_part_of_speech, sound, inside_1_text_kanji, inside_1_text_kanji_blank, inside_1_text_hrkt, first_eng, str(first_image), first_sound, inside_2_text_kanji, inside_2_text_kanji_blank, inside_2_text_hrkt, second_eng, str(second_image), second_sound, distractors
	
	Do not fetch all the data from json, if you want you can dig it yourself
	'''
	item = first['item']

	outside_text_kanji = item['cue']['text']
	outside_text_hrkt = item['cue']['transliterations']['Hrkt']
	outside_text_eng = item['response']['text']
	outside_text_part_of_speech = item['cue']['part_of_speech']
	sound = first['sound']
	sentences = first['sentences']
	
	first_sent = sentences[0]
	inside_1_text_kanji = first_sent['cue']['text']
	#spliting XXXXX<b>ZZZ</b>YYYY type of sentences
	inside_1_text_kanji_blank_t = [_i.split('</b>') for _i in inside_1_text_kanji.split('<b>')] 
	b_kanji_1 = inside_1_text_kanji_blank_t[1][0]
	left_s_1 = ''.join(inside_1_text_kanji_blank_t[0])
	right_s_1 = ''.join(inside_1_text_kanji_blank_t[1][1:])
	
	inside_1_text_kanji_blank = left_s_1 + '{{c1::<b>' + b_kanji_1  + '</b>::' + outside_text_part_of_speech + ' --- ' + outside_text_eng + '}}' + right_s_1 # make a cloze type of entity for anki
	
	inside_1_text_hrkt = first_sent['cue']['transliterations']['Hrkt']
	first_eng = first_sent['response']['text']
	first_image = first_sent['image']
	first_sound = first_sent['sound']
	try:
		second_sent = sentences[1]
		inside_2_text_kanji = second_sent['cue']['text']

		inside_2_text_kanji_blank_t = [_i.split('</b>') for _i in inside_2_text_kanji.split('<b>')]
		b_kanji_2 = inside_2_text_kanji_blank_t[1][0]
		left_s_2 = ''.join(inside_2_text_kanji_blank_t[0])
		right_s_2 = ''.join(inside_2_text_kanji_blank_t[1][1:])
		
		inside_2_text_kanji_blank = left_s_2 + '{{c1::<b>' + b_kanji_2  + '</b>::' + outside_text_part_of_speech + ' --- ' + outside_text_eng + '}}' + right_s_2
		
		inside_2_text_hrkt = second_sent['cue']['transliterations']['Hrkt']
		second_eng = second_sent['response']['text']
		second_image = second_sent['image']
		second_sound = second_sent['sound']
	except Exception as e: # if there is no second sentence, make all None
		second_sent = 'None'
		inside_2_text_kanji = 'None'
		inside_2_text_kanji_blank = 'None'
		inside_2_text_hrkt = 'None'
		second_eng = 'None'
		second_image = 'None'
		second_sound = 'None'

	distractors = [_d['text'] for _d in first['distractors']['cue']]
	
	return outside_text_kanji, outside_text_hrkt, outside_text_eng, outside_text_part_of_speech, sound, inside_1_text_kanji, inside_1_text_kanji_blank, inside_1_text_hrkt, first_eng, str(first_image), first_sound, inside_2_text_kanji, inside_2_text_kanji_blank, inside_2_text_hrkt, second_eng, str(second_image), second_sound, distractors


def xlsx_to_csv(file):
	'''
	Make a csv from xlsx
	'''
	
	wb = load_workbook(filename = file)
	ws = wb.active
	data_x = tuple(ws.values)
	text = ''
	for _d in data_x:

		if None in _d:
			_d = _d[:-1] + ('None',)
		try:
			row = ';'.join(_d) + '\n'
			text += row
		except:
			text += 'Something goes wrong' + len(data_x[0])*';' + '\n'
	csv_name = file.split('.xlsx')[0] + '.csv'
	with open(csv_name, 'w', encoding='utf-8') as f:
		f.write(text)

def downloader(url, download = False):
	'''
	Download files and save them by url-sensitive way 
	'''
	try:
		url = url.strip()
	except:
		return 'None'
		
	try: # just in case two times
		res = requests.get(url, headers=headers, allow_redirects=True)
		res.raise_for_status()
	except:
		try:
			res = requests.get(url, headers=headers, allow_redirects=True)
			res.raise_for_status()
		except:
			pass
	#in order to save files that have the same name but different links.
	rand = hashlib.sha256(url.encode()).hexdigest()
	filename = rand + url.split('/')[-1].split('?')[0] 
	if download:
		print(filename)
	if 'None' in filename:
		filename = 'None'
	if download:
		if 'None' in filename:
			pass
		else:
			if not os.path.exists('./files/'):
				os.makedirs('./files/')
			open('./files/' + filename, 'wb').write(res.content)
	return filename



def make_json_list():
	'''
	Make a list of all the json in directory (recursive)
	'''
	path = './/'

	files = [f for f in glob.glob(path + "**/*.json", recursive=True)]

	f_dic = dict()
	f_list = []
	for _f in files:
		f_list.append([_f[2:].split('_')[0], _f[2:]])
	cores_num = int(max([_t[0] for _t in f_list])) + 1
	cores = [[] for _ in range(cores_num)]

	for _p in f_list:
		cores[int(_p[0])].append(_p[1])
	return cores



def resize_aspect_fit(path, final_size):
	'''
	Resize all the images in directory and keep a aspect ratio.
	'''
	dirs = os.listdir( path )
	for item in dirs:
		if item == '.DS_Store':
			continue
		if os.path.isfile(path+item):
			try:
				im = Image.open(path+item)
				f, e = os.path.splitext(path+item)
				size = im.size
				ratio = float(final_size) / max(size)
				new_image_size = tuple([int(x*ratio) for x in size])
				im = im.resize(new_image_size, Image.ANTIALIAS)
				print(f,e)
				if e == '.jpg' or e == '.jpeg':
					im.save(f + e, 'JPEG', quality=90)
				elif e == '.png':
					im.save(f + e, 'PNG')
			except:
				pass