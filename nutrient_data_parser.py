from food_parser import FoodParser

class NutrientDataParser(FoodParser):
	def __init__(self):
		super().__init__()

		self.fields = [
			'food_id',
			'nutrient_id',
			'value',
			'num_data_pts',
			'std_error',
			'src_cd',
			'deriv_cd',
			'ref_ndb',
			'add_nutr_mark',
			'num_of_studies',
			'min',
			'max',
			'degrees_of_freedom',
			'low_eb',
			'up_eb',
			'stat_cmt',
			'add_mod_date',
			'cc'
		]