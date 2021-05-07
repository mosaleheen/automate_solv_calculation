#!/usr/bin/env python
# -*-coding: utf-8 -*-

#generate_input.py
#Mohammad Saleheen
#CREATED: 05-06-2021

from random import randint

def generate_dotinp(**kwargs):
    # Check if essential keys are there
    essential_keys = ['Nbr_Species','Box_info','Temperature_Info','Chemical_Potential_Info']
    if not all(key in kwargs for key in essential_keys):
        print('Please specify the following essential keys: \n \
              1. Nbr_Species \n \
              2. Box_info \n \
              3. Temperature_Info \n \
              4. Chemical_Potential_Info')
        return -1

    title = '! This is an input file for a GCMC simulation. '
    endstring = '!--------------'
    seeds = f'{randint(1, 1e8)} {randint(1, 1e8)}'

    kwargs.setdefault('Run_Name', 'pore.out')
    kwargs.setdefault('Sim_Type', 'gcmc')
    kwargs.setdefault('Nbr_Species', 1)
    kwargs.setdefault('VDW_Style','lj cut_tail 12.0')
    kwargs.setdefault('Charge_Style','coul ewald 12 0.00001')
    kwargs.setdefault('Seed_Info', seeds)
    kwargs.setdefault('Rcutoff_Low', 0.85)
    kwargs.setdefault('Pair_Energy', 'true')
    kwargs.setdefault('Run_Type','equilibration  500')
    kwargs.setdefault('Simulation_Length_Info',['units steps',
                                                'prop_freq 5000',
                                                'coord_freq 5000',
                                                'run 10000000'])
    kwargs.setdefault('Property_Info 1',['energy_total',
                                         'volume',
                                         'nmols',
                                         'pressure',
                                         'density',
                                         'mass_density'])
    kwargs.setdefault('CBMC_Info', ['kappa_ins 12',
                                    'rcut_cbmc 6.5'])

    if kwargs['Nbr_Species'] == 2:
        kwargs.setdefault('Mixing_Rule', 'lb')
        kwargs.setdefault('Start_Type','add_to_config 1 0 geometry.xyz 0 1')
        kwargs.setdefault('Molecule_Files',['geometry.mcf 1',
                                            'tip4p.mcf 10000'])
        kwargs.setdefault('Move_Probability_Info', {
                    'Prob_Translation' : [0.25, '0.00 2.00'],
                    'Prob_Rotation':[0.25, '0.00 45.00'],
                    'Prob_Insertion':['0.25', 'none cbmc'],
                    'Prob_Deletion': 0.25,
                    'Done_Probability_Info':''
                                           })
        kwargs.setdefault('Fragment_Files','species2/frag1/frag1.dat  1')
    elif kwargs['Nbr_Species'] == 1:
        kwargs['Start_Type'] = 'make_config 3000'
        kwargs['Molecule_Files'] = 'tip4p.mcf 10000'
        kwargs['Move_Probability_Info'] = {
                    'Prob_Translation':[0.25, 2.0],
                    'Prob_Rotation':[0.25, 45.00],
                    'Prob_Insertion':['0.25', 'cbmc'],
                    'Prob_Deletion': 0.25,
                    'Done_Probability_Info':''
                                           }
        kwargs['Fragment_Files'] = 'species1/frag1/frag1.dat  1'
    else:
        print('The script only works for 2 species.')
        return -1

    file = 'pore.inp'
    with open(file, 'w') as fwand:
        fwand.write('{}\n\n'.format(title))
        for key, value in kwargs.items():
            if isinstance(value, dict):
                fwand.write('# {}\n\n'.format(key))
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, list):
                        fwand.write('# {}\n'.format(sub_key))
                        for element in sub_value:
                            fwand.write('{}\n'.format(element))
                        fwand.write('{}\n\n'.format(endstring))
                    else:
                        if sub_value:
                            fwand.write('# {}\n{}\n{}\n\n'.format(sub_key, sub_value, endstring))
                        else:
                            fwand.write('# {}\n{}\n\n'.format(sub_key, endstring))
            elif isinstance(value, list):
                fwand.write('# {}\n'.format(key))
                for element in value:
                    fwand.write('{}\n'.format(element))
                fwand.write('{}\n\n'.format(endstring))
            else:
                fwand.write('# {}\n{}\n{}\n\n'.format(key, value, endstring))
        fwand.write('END\n')
