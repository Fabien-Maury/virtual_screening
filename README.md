# Step-by-step tutorial to this virtual screening pipeline

1. Use a linux distribution (this code was tested on Ubuntu), and install conda and python3
2. open a terminal in the folder containing all the files
3. prepare the conda environment using these commands and testing.txt :
>conda create -n testing --file testing.txt \
>conda activate testing \
>sudo apt-get install autodock-vina \
>pip install pandas \
>pip install scipy \
>pip install rdkit \
>pip install meeko


### A. SINGLE DOCKING : 

4. for a single docking, use the file "single_test.py". Edit the file to include the path to your receptor and ligand, in the space at the beginning of the code
5. in your terminal, launch the script by running this command :
>python3 single_test.py

OR

### B. VIRTUAL SCREENING : 

4. to dock multiple ligands, on a set of receptors, use "screening.py". Edit the file to include the path to your receptor folder and ligands list, in the space at the beginning of the code
5. in your terminal, launch the script by running this command :
>python3 screening.py

6. a lot of text will be displayed quickly on your terminal, and it will then freeze for a while (possibly a long time depending on the size of the molecules). If you are in case B : virtual screening, this will repeat until an attempt at docking each receptor with each ligand has been made.

7. When the code has finished running. Results will be in folders named after the receptors that were used. In each of these folders, there will be 2 files per docked ligand. These files will be called "receptor_docked_ligand_out.pdbqt" and receptor_docked_ligand_out.txt". The .pdbqt one contains the coordinates of the atoms of the docked ligand and receptor. The .txt one contains a summary of the docking and the ranked scores of the different poses achieved by the docking.



## NOTES : 
- ligand input must be in the SMILES format. Relevant SMILES strings must be stored in a .txt file (here ligands_database.txt)
- receptor input files must be in the .pdb format.
- coordinates for the center of the receptor must be stored in a .txt file as : "[x, y, z]"
- here both .pdb and .txt files for pocket_example1 are in the "pocket_example1 folder", which is itself in the "pockets" folder. You can add your own pockets folders to "pockets" following that model
- all input files must follow the naming convention from the given example
- while the scripts are running, new files and folders will be created in the working directory, do not interact with them until the code has finished running, or failure may occur
- if errors happen due to missing packages, you can problably install them in your environment with pip install
