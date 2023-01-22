import docking_pipeline
import os
from os import listdir
from os.path import isfile, join

#########################################################################

pockets_folder = "pockets"
ligands_list = "ligand_database.txt"

#########################################################################

smiles_file = open(ligands_list, "r")
first_smiles_list = smiles_file.readlines()
first_smiles_list = [i.strip('\n') for i in first_smiles_list]
ligand_names_list = []
smiles_list = []
for i in range(len(first_smiles_list)):
	ligand_name, smile = first_smiles_list[i].split(';')
	ligand_names_list.append(ligand_name)
	smiles_list.append(smile)

pockets = [x[0] for x in os.walk(pockets_folder)]


for pocket in pockets:
		local_files = [pocket + "/" + f for f in listdir(pocket) if isfile(join(pocket, f))]
		pocket_paths = [i for i in local_files if i.endswith(".pdb")]


pocket_path = pocket_paths[0]
pocket_name = pocket_path.split('.')[0].split('/')[-1]
os.system("mkdir " + pocket_name)


smiles_str = smiles_list[0]
pdb_pocket = pocket_path
pocket_center = pocket_path.replace('.pdb','_center.txt')
ligand_name = ligand_names_list[i]
output_name = pocket_name + "/" + pocket_name + '_docked_' + ligand_name

args = (smiles_str, pdb_pocket, pocket_center, ligand_name, output_name)
for arg in args:
	print(arg)

run = docking_pipeline.full_docking(smiles_str, pdb_pocket, pocket_center, output_name, ligand_name)
print("\nEND\n")
