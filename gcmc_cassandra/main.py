#!/usr/bin/env python
# -*-coding: utf-8 -*-

#main.py
#Mohammad Saleheen
#CREATED: 05-06-2021
import generate_input
input_params = {'Sim_Type':'gcmc',
                'Nbr_Species':2,
                'Box_info': [1,
                             'orthogonal',
                             '44.4412 48.1095 49.0000'],
                'Temperature_Info': 298.0,
                'Chemical_Potential_Info': -44.90
               }
generate_input.generate_dotinp(**input_params)
generate_input.get_geometry_xyz(3,3,1)
generate_input.get_geometry_pdb()

