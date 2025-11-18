#!/home/dunbo/anaconda3/envs/cheminfo/bin/python

from pdbfixer import PDBFixer
from openmm.app import PDBFile
import argparse

def parser_args():
    parser = argparse.ArgumentParser(description='This is a program to fix peptide or protein based on pdbfixer. no solvent is added.')
    parser.add_argument('pdbfile', help='input a pdb file')
    args = parser.parse_args()
    return args


def run():
    args = parser_args()
    pdbfile = args.pdbfile
    fix_and_output(pdbfile)


def fix_and_output(pdbfile):
    output_path = pdbfile.split(".pdb")[0] + "_Hyd.pdb"

    fixer = PDBFixer(filename = pdbfile)
    fixer.removeHeterogens(False)
    #residuelist = fixer.topology.residues()
    fixer.findMissingResidues()
    fixer.missingResidues = {}
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    fixer.addMissingHydrogens(7.0)

    print("output pdb:", output_path)
    PDBFile.writeFile(fixer.topology, fixer.positions, open(output_path, 'w'))


if __name__ == '__main__':
        run()
