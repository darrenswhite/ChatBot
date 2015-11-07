import os.path
import pickle
import random
import re
import string


def calc_prob(value):
	"""
	Calculate the probability of each combination
	:param value: A list of combination options to calculate probabilities
	:return: The list of combination options with thier calculated probabilities
	"""

	total = sum(i[1] for i in value)

	for i in value:
		i[1] /= total

	return value


def generate_reply(key):
	"""
	Generates a pseudorandom sentence based on the given key
	:param key: The key word to base the sentence on
	:return: A randomly generated sentence
	"""

	sentence = []
	curr_word = key
	curr_item = get_word_item(curr_word)
	ended = False

	while True:
		sentence.append(curr_word)

		if curr_item is None:
			break

		curr_word = get_next_word(curr_item[1])
		curr_item = get_word_item(curr_word)

		for c in sent_end:
			if c not in curr_word:
				continue

			sentence.append(curr_word[:curr_word.find(c) + 1])
			ended = True
			break
		if ended:
			break

	curr_word = get_prev_word(keys[0])
	ended = False

	while True:
		if curr_word is None:
			break

		sentence.insert(0, curr_word)

		curr_word = get_prev_word(curr_word)

		for c in sent_end:
			if c not in curr_word:
				continue

			ended = True
			break
		if ended:
			break

	if len(sentence) <= 1:
		return 'Sorry, I didn\'t get that.'

	return ' '.join(sentence)


def get_next_word(options):
	"""
	Gets the next word based upon its probability
	:param options: The word-probability options
	:return: The next word based upon probability
	"""

	count = random.uniform(0, 1)

	for word, prob in options:
		if count < prob:
			return word

		count -= prob

	return None


def get_prev_word(word):
	"""
	Gets the previous word based upon its probability
	:return: The previous word based upon probability
	"""

	if word is None:
		return None

	possible = []

	for item in data_dict.items():
		for i in item[1]:
			if word == i[0] or word in i[0]:
				possible.append(item[0])

	if len(possible) == 0:
		return None

	return random.choice(possible)


def get_word_item(word):
	"""
	Get the item in the dictionary for this key word
	:param word: The key in the dictionary
	:return: The dictionary item for the key
	"""

	for item in data_dict.items():
		op = item[0].lower()
		if op == word.lower() or op.startswith(word.lower()):
			return item

	return None


def load_dict():
	"""
	Creates a new data dictionary. If an archive of a previous
	dictionary exists, then load it. If an argument of a file path
	has been specified then update the dictionary with the contents
	of that file. Store the dictionary to the archive file.
	:return: The data dictionary to be used
	"""

	archive = '.data_dict'
	global data_dict

	if os.path.isfile(archive):
		data_dict = pickle.load(open(archive, 'rb'))

	if len(data_dict) == 0:
		print('[SYSTEM] >> No data dictionary currently exists!')

	while len(data_dict) == 0:
		path = input('[SYSTEM] >> Please enter external text source path: ')
		update_dict(read_file(path))

	print('')

	pickle.dump(data_dict, open(archive, 'wb'))


def read_file(path):
	"""
	Opens and reads data from the file path
	:param path: The path of the file to read from
	:return: The file text contents
	"""

	try:
		f = open(path, 'r')
	except IOError:
		print('[SYSTEM] >> File does not exist!\n')
		return None

	return f.read()


def update_dict(text):
	"""
	Updates the data dictionary with the given text
	:param text: The text to parse and calculate probabilities for
	"""

	if text is None:
		return

	text = re.sub(r'[\n\r]+', ' ', text.strip())
	words = text.split()

	for i in range(len(words) - combos + 1):
		curr = ' '.join(words[i:i + combos - 1])
		option = words[i + combos - 1]
		options = []

		if curr in data_dict:
			options = data_dict[curr]

		value = [option, float(text.count(' '.join([curr, option])))]

		found = False

		for op in options:
			if option == op[0]:
				found = True
				break

		if not found:
			options.append(value)

		data_dict[curr] = options

	for key in data_dict:
		data_dict[key] = calc_prob(data_dict[key])


data_dict = {}
combos = 2
sent_end = '.!?'

load_dict()

print('Welcome To The ChatBot!\n')
print('The data that was provided has been successfully loaded.')
print('The topic that you can ask questions about is Steve Jobs\' biography.')
print('')

words = ['hello', 'my', 'is', 'it', 'the', 'does', 'he', 'she', 'will', 'they', 'they\'re', 'their', 'there', 'how',
         'what', 'where', 'when', 'why', 'with', 'who', 'like', 'are', 'whats', 'do', 'you', 'in', 'happened']

while True:
	user_input = input('[USER] >> ')

	if len(user_input) == 0:
		print('[SYSTEM] >> Could you please type something.\n')
		continue

	for i in string.punctuation:
		user_input = user_input.replace(i, '')

	keys = [x for x in user_input.split() if x.lower() not in words]

	if len(keys) == 0:
		print('[SYSTEM] >> Sorry I didn\'t understand that.\n')
		continue

	print('[BOT] >> ' + generate_reply(random.choice(keys)) + '\n')