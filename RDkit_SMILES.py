#!/home/dunbo/miniforge3/envs/DECIMER/bin/python

import rdkit
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, Crippen, rdMolDescriptors, AllChem
import argparse
# from matplotlib.colors import ColorConverter

def parser_args():
    parser = argparse.ArgumentParser(description='This is to convert a smiles string to Figure or mol format. Please use it under WSL system')
    parser.add_argument('string', help='input a smiles string, inside a \" \" to avoid possible special character.')
    parser.add_argument('--output', help='Give a output file name for the figure', type = str)
    parser.add_argument('--mode', help='Output mode: 1: png; 2: 3D mol file', type = int)
    args = parser.parse_args()
    return args


def run():
    args = parser_args()
    string = args.string
    output_path = args.output
    mode = args.mode
    if mode is None:
        mode = 1
    if output_path is None:
        output_path = string + ".png"
    SMILES2mol(string, output_path, mode)


def SMILES2mol(string, output_path, mode):
    molecule = Chem.MolFromSmiles(string)
    if mode == 1:
        img = Draw.MolToImage(molecule)
        img.save(output_path)
    if mode == 2:
        molecule_H = Chem.AddHs(molecule)
        AllChem.EmbedMolecule(molecule_H)
        print(Chem.MolToMolBlock(molecule_H))
         




if __name__ == '__main__':
	run()