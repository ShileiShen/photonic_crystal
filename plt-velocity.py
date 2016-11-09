import re
import sys
import math
from pprint import pprint
import matplotlib.pyplot as plt

def get_vector_magnitude(vec_str):
	VEC_REGEX = re.compile("#\((.*?) (.*?) (.*?)\)")
	m = VEC_REGEX.match(vec_str)
	if (m is None) or (len(m.groups()) != 3):
		raise ValueError("Invalid vector -> {0}".format(vec_str))
	else:
		x,y,z = m.groups()
		return math.sqrt(float(x)**2 + float(y)**2 + float(z)**2)

def parse_file(mode, filename):
	"""
	Parse file to retrieve data
	"""
	LINE_REGEX = re.compile("t{mode}velocity:, (.*)".format(mode=mode))
	def get_line_data(line):
		m = LINE_REGEX.match(line)
		if (m is None) or (len(m.groups()) != 1):
			raise ValueError("Invalid Line format -> {0}".format(line))
		else:
			return m.group(1)

	with open(filename) as f:
		k_index = []
		velocities = ([], [])
		for line in f:
			line_data = get_line_data(line).split(", ")
			k_index.append(line_data[0])
			velocities[0].append(get_vector_magnitude(line_data[1]))
			velocities[1].append(get_vector_magnitude(line_data[2]))

	return (k_index, velocities)

def plot_data(data):
	k_index, velocities = data
	plt.plot(k_index, velocities[0], 'o-', label="Band 1")
	plt.plot(k_index, velocities[1], 'o-', label="Band 2")
	
	plt.legend(fontsize='xx-small')
	plt.xlabel("k-index")
	plt.ylabel("Group velocity magnitude")

	plt.show()


def main():
	mode = sys.argv[1]
	filename = sys.argv[2]
	data = parse_file(mode, filename)
	# pprint(data)
	plot_data(data)

if __name__ == '__main__':
	main()