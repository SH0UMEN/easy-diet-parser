class FoodParser:
	def __init__(self):
		self.data = {}

	def parse(self, filename):
		print('Parsing {} file...'.format(filename))

		file = open(filename, 'r')
		lines = file.readlines()
		self.data = {}

		for i in range(len(lines)):
			record = self.parse_line(lines[i], i)
			self.data[record['id']] = record

		file.close()

		print('{} parsing is completed'.format(filename))

		return self.data

	def parse_line(self, line, index):
		fields = self.get_fields()
		values = line.strip().split('^')
		record = {}

		for i in range(len(values)):
			value = values[i]

			if value.startswith('~'):
				value = value[1:-1]
			if value != '':
				if value.isdigit():
					value = int(value)
				else:
					try:
						value = float(value)
					except ValueError:
						value = value
			else:
				value = 0

			record[fields[i]] = value

		if 'id' not in fields:
			record['id'] = index

		return record

	def get_fields(self):
		return self.fields

	def filter_fields(self, fields_to_stay):
		fields = self.get_fields()
		data = {}

		for identifier in self.data:
			data[identifier] = {}

			for field in fields_to_stay:
				if field not in fields:
					continue

				data[identifier][field] = self.data[identifier][field]

		return data
