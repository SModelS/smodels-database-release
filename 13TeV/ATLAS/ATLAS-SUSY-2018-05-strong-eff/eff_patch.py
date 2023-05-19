#!/usr/bin/env python3

import json
import sys
sys.path.append('/Users/sahanan/smodels-utils')
sys.path.append('/Users/sahanan/smodels')
from smodels_utils.morexsecs.refxsecComputer import RefXSecComputer
from smodels_utils import SModelSUtils
from smodels.tools.physicsUnits import fb, pb

#++++++load the json file to be read++++++++
with open('llh_jsons/SRC_patchset.json', 'r') as f:
    js = json.load(f)

lumi = 139/fb
xs = RefXSecComputer()

#++++++++load all the relevant cross-sections+++++++++++
gg = xs.getXSecsFrom(f'{SModelSUtils.installDirectory()}/smodels_utils/morexsecs/tables/xsecgluino13.txt',columns={"mass":0, "xsec":2})
ss = xs.getXSecsFrom(f'{SModelSUtils.installDirectory()}/smodels_utils/morexsecs/tables/xsecsquark13.txt',columns={"mass":0, "xsec":2})

#list of all patchset json files to be read
Bkg_files = ['SRC_patchset.json','SRHigh_patchset.json','SRLow_patchset.json','SRMed_patchset.json','SRZHigh_patchset.json','SRZLow_patchset.json','SRZMed_patchset.json']

#list of all file names to write the output efficiencies into
file_name = ['SRC','SRHigh','SRLow','SRMed','SRZHigh','SRZLow','SRZMed']

#list of all the signal region names occuring in the relevant patchset files
sr_name = ['SRC_mll', 'SRHigh_mll', 'SRLow_mll', 'SRMed_mll', 'SRZHigh_cuts','SRZLow_cuts','SRZMed_cuts']

#name of path in the patchset under 'patch'
goodpath = "/channels/0/samples/"

#name of the topologies in the patchset
topo_name = ['GG_N2_ZN1','SS_N2_ZN1']

#name of the topologies in the output file
topos = ['T5ZZ','T6ZZ']

for k in range(len(topos)):
    for j in range(len(Bkg_files)):
        #load the json file to be read
        with open(f'llh_jsons/{Bkg_files[j]}', 'r') as file:
            js = json.load(file)
            #no of values in 'data' under 'value' in 'patch' = no of bins
            bin_size = len(js['patches'][0]['patch'][0]['value']['data'])
            for i in range(bin_size):
                #output file of efficiencies for each bin
                name = 'orig/EffFromPatch_'+ file_name[j] + '_' + topos[k]+'_Bin_'+ str(i+1) + '.csv'
                with open(name, 'w') as out:
                    out.write('# M(G), M(LSP), Efficiency\n')
                    for pa in js['patches']:
                        if topo_name[k] in pa['metadata']['values'][0]:
                            #extract efficiencies
                            massvector = pa['metadata']['values']
                            if k == 0: xsec = xs.interpolate(massvector[1], gg)
                            else : xsec = xs.interpolate(massvector[1], ss)
                            xsec *= pb
                            for op in pa['patch']:
                                if goodpath in op['path']:
                                    signal = op['value']['data'][i]
                                    eff = signal/xsec/lumi
                                    if eff > 1. :
                                        print("ERROR. sr : ", name," | signal : ", signal, " | xs : ", xsec, " | massv : ", massvector)
                                        continue
                                    out.write("{} , {} , {}\n".format(massvector[1], massvector[2], eff))

