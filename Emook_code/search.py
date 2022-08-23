from thefuzz import fuzz
from thefuzz import process
def	thefuzz_search(items: list, search: str):
	a = []
	for item in items:
		coincidence = fuzz.partial_ratio(item.lower(), search.lower())	# Получаю % совпадения
		if coincidence != 0:
			a.append([item, coincidence]) # Добавляется список ['текст', % совпадения] в список "a"

	N = len(a)
	for i in range(N-1): # Пузырьковая сортировка списка вида: [['Текст1', 1], ['fwetfs', '2']]
		for j in range(N-i-1):
			if a[j][1] < a[j+1][1]:
				a[j], a[j+1] = a[j+1], a[j]

	sort_n = []
	for i in range(len(a)):
		sort_n.append(a[i][0]) # Делаю отсортированый список только из items 
	return sort_n

def	thefuzz_search_id(items: list, search: str):
	a = []
	for item in items:
		if item != '':
			coincidence = fuzz.partial_ratio(item, search)	# Получаю % совпадения
			if coincidence != 0:
				a.append([item, coincidence]) # Добавляется список ['текст', % совпадения] в список "a"

	N = len(a)
	for i in range(N-1): # Пузырьковая сортировка списка вида: [['Текст1', 1], ['fwetfs', '2']]
		for j in range(N-i-1):
			if a[j][1] < a[j+1][1]:
				a[j], a[j+1] = a[j+1], a[j]
	
	b = []
	for i in a:
		if i not in b:
			b.append(i)
	a = b

	sort_n = []
	for i in range(len(a)):
		sort_n.append(a[i][0]) # Делаю отсортированый список только из items 
	return sort_n