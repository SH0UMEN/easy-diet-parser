from food_parser import FoodParser

class FoodDescParser(FoodParser):
	def __init__(self):
		super().__init__()

		self.fields = [
			'id',
			'category_id',
			'title',
			'short_description',
			'common_name',
			'manufactured_name',
			'survey',
			'ref_description',
			'refuse',
			'scientific_name',
			'n_factor',
			'protein_factor',
			'fat_factor',
			'cho_factor'
		]