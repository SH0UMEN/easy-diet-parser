from food_parser import FoodParser

class NutrientDefinitionParser(FoodParser):
	def __init__(self):
		super().__init__()

		self.fields = [
			'id',
			'units',
			'tagname',
			'description',
			'num_of_decimal',
			'sort_order'
		]