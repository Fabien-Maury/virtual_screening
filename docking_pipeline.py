import os
from rdkit import Chem
from rdkit.Chem import AllChem

def run_command(command): # python wrapper to run a command in the linux terminal
  status = False
  try:
    os.system(command)
    status = True
  except Exception as e:
    print(str(e))
    status = False
  return(status)

def prepare_pdb_receptor(pdb_receptor, output_folder): # from a PDB receptor file, generates a prepared PDBQT file
  name = pdb_receptor.split('.')[0].split('/')[-1]
  receptor_h = name + "_h.pdb"
  command1 = "reduce " + pdb_receptor + " > " + output_folder + "/" + receptor_h # add hygrogens to receptor (adfr)
  command2 = "prepare_receptor -r " + output_folder + "/" + receptor_h + " -o " + output_folder + "/" + name + ".pdbqt" # prepare_receptor (adfr)
  status1 = run_command(command1)
  status2 = run_command(command2)
  status_total = status1 and status2
  return(status_total)

def read_sdf(sdf_file): # read 1st molecule in an SDF file
  mols = []
  suppl = Chem.SDMolSupplier(sdf_file)
  for mol in suppl:
    mols.append(mol)
  return(mols[0])

def read_smiles(smiles_string): # read molecule in a SMILES string
  mol = Chem.MolFromSmiles(smiles_string)
  return(mol)

def generate_conf(mol, n): # generates n conformers optimized with MMFF field, from mol (rdkit)
  mol = AllChem.AddHs(mol)
  params = Chem.rdDistGeom.ETKDGv3()
  confs = Chem.rdDistGeom.EmbedMultipleConfs(mol, numConfs = n, params = params)
  nb_converge = 0
  for conf in confs :
    optimisation = AllChem.MMFFOptimizeMolecule(mol, confId = conf)
    nb_converge += optimisation
    if optimisation == -1 :
      print('This conformer cannot be setup')
    else : 
      nb_converge += optimisation 
  return(mol)

def write_conformers(filename, mol): # writes conformers of a molecule to SDF file (rdkit)
  writer = Chem.SDWriter(filename + ".sdf")
  for id in range(mol.GetNumConformers()) :
    writer.write(mol, confId = id)
  writer.close()
  return()

def prep_sdf_lig(sdf_lig, output_folder): # from a SDF ligand, generates a prepared PDBQT file (meeko)
  name = sdf_lig.split('.')[0].split("/")[-1]
  command = "mk_prepare_ligand.py -i " + sdf_lig + " -o " + output_folder + "/" + name + ".pdbqt -w"
  status = run_command(command)
  return(status)

def write_config(txt_center_receptor, filename, box_size = 20.0): # use the receptor center coordinates to write a vina config file
  file = open(txt_center_receptor, "r")
  x, y, z = file.readlines()[0].strip(" ").strip("[").strip("]").split(",")
  file.close()
  new_file = open(filename, "w")
  new_file.write('center_x = ' + str(x) + "\n")
  new_file.write('center_y = ' + str(y) + "\n")
  new_file.write('center_z = ' + str(z) + "\n")
  new_file.write('size_x = ' + str(float(box_size)) + "\n")
  new_file.write('size_y = ' + str(float(box_size)) + "\n")
  new_file.write('size_z = ' + str(float(box_size)))
  new_file.close()
  return()

def docking(pdbqt_receptor, pdbqt_ligand, config_file, output_name): # generates a PDBQT output file after docking PDQT receptor and ligand, and generates an output txt file
  command = "vina --receptor " + pdbqt_receptor + " --ligand " + pdbqt_ligand + " \
       --config " + config_file + " \
       --exhaustiveness=32 --out " + output_name + "_out.pdbqt > " + output_name + "_out.txt"
  status = run_command(command)
  return(status)

def full_docking(smiles_string, pdb_pocket, pocket_center, output_name, ligand_name):
  temp = "temp_docking_files"
  command1 = "mkdir " + temp
  command2 = "rm -r temp_docking_files"
  run_command(command1)
  try:
    pocket_name = pdb_pocket.split(".")[0].split('/')[-1]

    prepare_pdb_receptor(pdb_pocket, temp)
    write_config(pocket_center, temp + "/" + pocket_name + "_config.txt")
    mol = read_smiles(smiles_string)
    mol = generate_conf(mol, 1)
    write_conformers(temp + "/" + ligand_name + "_temp_lig", mol)
    prep_sdf_lig(temp + "/" + ligand_name + "_temp_lig.sdf", temp)
    docking(temp + "/" + pocket_name + ".pdbqt", temp + "/" + ligand_name + "_temp_lig.pdbqt", temp + "/" + pocket_name + "_config.txt", output_name)
    print("Receptor : " + pocket_name + ", and ligand : " + ligand_name + " have been docked\n")
  except Exception as e:
    print(e)
  #run_command(command2)
  return()