from food_parser import FoodParser

class GroupDescParser(FoodParser):
	def __init__(self):
		super().__init__()

		self.fields = [
			'id',
			'title'
		]