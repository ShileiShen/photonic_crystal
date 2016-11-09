import re
import sys
import matplotlib.pyplot as plt
from pprint import pprint

def get_num_bands(mode, header):
	columns = header.split(", ")
	if columns[0] != "k index":
		return -1
	else:
		for i in range(5,len(columns)):
			if columns[i] != "t{mode} band {n}".format(mode=mode, n=i-4):
				return -1
		return len(columns) - 5

def parse_file(mode, filename):
	"""
	Parse file to retrieve data
	"""
	LINE_REGEX = re.compile("t{mode}freqs:, (.*)".format(mode=mode))
	def get_line_data(line):
		m = LINE_REGEX.match(line)
		if (m is None) or (len(m.groups()) != 1):
			raise ValueError("Invalid Line format -> {0}".format(line))
		else:
			return m.group(1)

	with open(filename) as f:
		header = get_line_data(f.readline())
		num_bands = get_num_bands(mode, header)
		if num_bands == -1:
			raise ValueError("Invalid file header -> {0}".format(header))
		k_index = []
		bands = [[] for _ in range(num_bands)]
		for line in f:
			line_data = get_line_data(line).split(", ")
			k_index.append(line_data[0])
			for i,band in enumerate(bands):
				band.append(line_data[5+i])

	return (k_index, bands)

def plot_data(mode, data):
	k_index, bands = data
	lines = []
	labels = []
	for i,band in enumerate(bands):
		label="T{mode} Band {n}".format(mode=mode.upper(), n=i+1)
		line = plt.plot(k_index, band, 'o-', label=label)
		lines.append(line)
		labels.append(label)
	plt.legend(fontsize='xx-small')

	# plt.axhspan(0.2034, 0.2396, facecolor='b', edgecolor='none', alpha=0.2)
	# plt.text(8,(0.2034+0.2396)/2-0.005, "Bandgap")
	
	plt.xlabel("k-index")
	plt.ylabel("frequency ($c/a$)")
	plt.show()


def combined_plot(te_filename, tm_filename):
	te_k_index, te_bands = parse_file("e", te_filename)
	tm_k_index, tm_bands = parse_file("m", tm_filename)
	if te_k_index != tm_k_index:
		raise ValueError("k-indicies unequal in TE and TM bands") 
	else:
		for i,band in enumerate(te_bands):
			te_line, = plt.plot(te_k_index, band, 'r--', linewidth=2, label="TE-like bands")
		for i,band in enumerate(tm_bands):
			tm_line, = plt.plot(tm_k_index, band, 'g--', linewidth=2, label="TM-like bands")
	plt.legend((te_line,tm_line),("TE-like bands", "TM-like bands"),fontsize='x-small')

	plt.axhspan(0.2034, 0.2396, facecolor='b', edgecolor='none', alpha=0.2)
	plt.text(8,(0.2034+0.2396)/2-0.005, "TE Bandgap")

	plt.xticks((1.0,6.0,11.0,16.0),("$\\Gamma$", "$M$", "$K$", "$\\Gamma$"))
	plt.xlabel("Reciprocal Space")
	plt.ylabel("frequency ($c/a$)")

	plt.show()

def main():
	mode = sys.argv[1]
	if mode == "c" :
		te_filename = sys.argv[2]
		tm_filename = sys.argv[3]
		combined_plot(te_filename, tm_filename)
	else:
		filename = sys.argv[2]
		# pprint (parse_file(mode, filename))
		data = parse_file(mode, filename)
		plot_data(mode, data)

if __name__ == '__main__':
	main()
