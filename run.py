# test_env_manager.py
import sys
import os
sys.path.insert(0, '.')

from env_manager import EnvManager

def get_data_from_envff(ffpth = './fcc-env.env'):
	env_mngr = EnvManager()
	result = env_mngr.read_from_file(ffpth)
	return result

def get_fcc_envdata():
	fcc_path_manual = get_data_from_envff('./fcc-env.env')['fcc_path']
	fccenvdd = get_data_from_envff(os.path.join(os.path.abspath(fcc_path_manual),".env"))
	return fccenvdd
