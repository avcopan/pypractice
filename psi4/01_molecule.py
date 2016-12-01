import psi4

psi4.core.set_global_option('BASIS', 'CC-PVDZ')
print(psi4.core.get_option('SCF', 'BASIS'))

xyzstring = """
units angstrom
O     0.0000000000    0.0000000000   -0.0711762954
H     0.0000000000   -0.8916195680    0.5648097613
H     0.0000000000    0.8916195680    0.5648097613
"""
molecule = psi4.core.Molecule.create_molecule_from_string(xyzstring)
molecule.update_geometry()
molecule.print_out()

