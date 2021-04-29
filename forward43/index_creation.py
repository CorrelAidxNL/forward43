'''This file is to create index settings and mappings in ES.
This is just a python program. Yet to combine this with ES-python program 
which will create and map index into ES'''


def get_settings(settingsFile):
	'''(file) -> dictionary
	
	Propertes for creating the index n ES
	settingsFile is the locaton of the mappings text file.
	Return the contents of the text file with a dictionary. 
	'''

	with open(''+settingsFile) as f:
		settings_dict = dict(x.strip().split(":", 1) for x in f)
		return setting_dict



def get_mappings(mappingsFile):
	'''(file) -> dictionary
	
	Propeties for creaing the mappings for the index in ES
	mappingsFile is the locaton of the mappings text file.
	Return the contents of the text file with a dictionary. 
	'''

	with open(''+mappingsFile) as f:
		mappings_dict = dict(x.strip().split(":", 1) for x in f)
		return mapping_dict



if __name__ == '__main__':

	settings_file = input("Enter the location of the text file with extension: ")		# location of the settings file
	required_settings = get_settings(settings_file)
	print(required_mappings)
	
	mappings_file = input("Enter the location of the text file with extension: ")		# location of mappings file
	required_mappings = get_mappings(mappings_file)
	print(required_mappings)

	# Need to integrate further with ES-python package which will create index settings and mappings in ES.
