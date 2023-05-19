#!/usr/bin/env python3

"""
.. module:: convert
   :synopsis: used to create info.txt and the <txname>.txt files.

"""
import sys
import os
import argparse
import copy

argparser = argparse.ArgumentParser(description =  
'create info.txt, txname.txt, twiki.txt and sms.py')
argparser.add_argument ('-utilsPath', '--utilsPath', 
help = 'path to the package smodels_utils',\
type = str )
argparser.add_argument ('-smodelsPath', '--smodelsPath', 
help = 'path to the package smodels_utils',\
type = str )
argparser.add_argument ('-t', '--ntoys', 
help = 'number of toys to throw',\
type = int, default=200000  )
args = argparser.parse_args()

if args.utilsPath:
    utilsPath = args.utilsPath
else:
    databaseRoot = '../../../'
    sys.path.append(os.path.abspath(databaseRoot))
    from utilsPath import utilsPath
    utilsPath = databaseRoot + utilsPath
if args.smodelsPath:
    sys.path.append(os.path.abspath(args.smodelsPath))

sys.path.append(os.path.abspath(utilsPath))
from smodels_utils.dataPreparation.inputObjects import MetaInfoInput,DataSetInput
from smodels_utils.dataPreparation.databaseCreation import databaseCreator
from smodels_utils.dataPreparation.massPlaneObjects import x, y, z

DataSetInput.ntoys=args.ntoys

#+++++++ global info block ++++++++++++++
info = MetaInfoInput('ATLAS-SUSY-2013-12')
info.sqrts = '8.0'
info.private = False
info.lumi = '20.3'
info.publication = 'http://link.springer.com/article/10.1007/JHEP04(2014)169'
info.url = 'https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2013-12/'
info.arxiv = 'http://arxiv.org/abs/1402.7029'
info.contact = 'SModelS'
info.prettyName = '3 leptons (e,mu,tau) + Etmiss'
info.comment = 'Efficiency Maps given only for single bin for TChiChipmSlepL and TChiWZ. Efficiency Maps are for aggregated bins for TChiChipmStauL and TChiWH.'
#info.supersedes = 'ATLAS-CONF-2013-035; CONF-2012-154'



#+++++++ dataset block ++++++++++++++
dsname = "SR0tau_a_Bin20"
dataset = DataSetInput(dsname)
dataset.setInfo(dataType = 'efficiencyMap', dataId = dsname, observedN = 0.0, expectedBG = 0.3 , bgError = 2.0)
#+++++++ next txName block ++++++++++++++
TChiChipmSlepL = dataset.addTxName('TChiChipmSlepL')
TChiChipmSlepL.constraint ="2.*([[['L+'],['L-']],[['L'],['nu']]] + [[['L+'],['L-']],[['nu'],['L']]] + [[['L-'],['L+']],[['L'],['nu']]] + [[['L-'],['L+']],[['nu'],['L']]])"
TChiChipmSlepL.conditionDescription ="[[['L+'],['L-']],[['L'],['nu']]] ~ [[['L+'],['L-']],[['nu'],['L']]], [[['L+'],['L-']],[['nu'],['L']]] > 2.7*[[['ta+'],['ta-']],[['nu'],['L']]], [[['L+'],['L-']],[['L'],['nu']]] > 2.7*[[['ta+'],['ta-']],[['L'],['nu']]], [[['L+'],['L-']],[['nu'],['L']]] > 2.7*[[['L+'],['L-']],[['nu'],['ta']]], [[['L+'],['L-']],[['L'],['nu']]] > 2.7*[[['L+'],['L-']],[['ta'],['nu']]],[[['L+'],['L-']],[['nu'],['L']]] > 2.7*[[['e+'],['e-']],[['nu'],['L']]], [[['L+'],['L-']],[['L'],['nu']]] > 2.7*[[['e+'],['e-']],[['L'],['nu']]], [[['L+'],['L-']],[['nu'],['L']]] > 2.7*[[['L+'],['L-']],[['nu'],['e']]], [[['L+'],['L-']],[['L'],['nu']]] > 2.7*[[['L+'],['L-']],[['e'],['nu']]]"
TChiChipmSlepL.condition ="Csim([[['L+'],['L-']],[['L'],['nu']]],[[['L+'],['L-']],[['nu'],['L']]],[[['L-'],['L+']],[['nu'],['L']]],[[['L-'],['L+']],[['L'],['nu']]]); Cgtr([[['L+'],['L-']],[['nu'],['L']]],3.*[[['ta+'],['ta-']],[['nu'],['L']]]); Cgtr([[['L+'],['L-']],[['L'],['nu']]],3.*[[['ta+'],['ta-']],[['L'],['nu']]]);Cgtr([[['L+'],['L-']],[['nu'],['L']]],3.*[[['L+'],['L-']],[['nu'],['ta']]]); Cgtr([[['L+'],['L-']],[['L'],['nu']]],3.*[[['L+'],['L-']],[['ta'],['nu']]]);Cgtr([[['L+'],['L-']],[['nu'],['L']]],3.*[[['e+'],['e-']],[['nu'],['L']]]); Cgtr([[['L+'],['L-']],[['L'],['nu']]],3.*[[['e+'],['e-']],[['L'],['nu']]]); Cgtr([[['L+'],['L-']],[['nu'],['L']]],3.*[[['L+'],['L-']],[['nu'],['e']]]); Cgtr([[['L+'],['L-']],[['L'],['nu']]],3.*[[['L+'],['L-']],[['e'],['nu']]])"
TChiChipmSlepL.source = "ATLAS"
#+++++++ next mass plane block ++++++++++++++
TChiChipmSlepL050 = TChiChipmSlepL.addMassPlane(2*[[x, x*0.5+(1.-0.5)*y, y]])
TChiChipmSlepL050.figure = "FigAux 5a"
TChiChipmSlepL050.figureUrl = "https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2013-12/figaux_05a.png"
TChiChipmSlepL050.dataUrl = 'https://doi.org/10.17182/hepdata.63114.v1/t52'
TChiChipmSlepL050.setSources(dataLabels= ['expExclusion', 'obsExclusion'],
                 dataFiles= ['orig/exc_slepL_expected.txt', 'orig/exc_slepL_obs.txt'],
                 dataFormats= ['txt', 'txt'],units= [None, None])
TChiChipmSlepL050.addSource('efficiencyMap',('orig/Table48.csv','orig/Table52.csv'), dataFormat='mcsv')
TChiChipmSlepL050.efficiencyMap._unit = '0.0001'


#+++++++ dataset block ++++++++++++++
dsname = "SR0tau_a_Bin16"
dataset = DataSetInput(dsname)
dataset.setInfo(dataType = 'efficiencyMap', dataId = dsname, observedN = 3.0, expectedBG = 4.6 , bgError = 3.7)
#+++++++ next txName block ++++++++++++++
TChiWZ = dataset.addTxName('TChiWZ')
TChiWZ.constraint ="[[['W']],[['Z']]]"
TChiWZ.conditionDescription ="None"
TChiWZ.condition ="None"
TChiWZ.source = "ATLAS"
TChiWZ.massConstraint = None

TChiWZoff = dataset.addTxName('TChiWZoff')
TChiWZoff.validationTarball = "TChiWZoff_8Tev.tar.gz"
TChiWZoff.constraint ="71.*([[['mu+','mu-']],[['l','nu']]] + [[['e+','e-']],[['l','nu']]])"
TChiWZoff.conditionDescription ="[[['mu+','mu-']],[['l','nu']]] > [[['e+','e-']],[['l','nu']]]"
TChiWZoff.condition ="Cgtr([[['mu+','mu-']],[['l','nu']]],[[['e+','e-']],[['l','nu']]])"
TChiWZoff.massConstraint = [['dm <= 76.0'], ['dm <= 86.0']]
TChiWZoff.source = "ATLAS"
#+++++++ next mass plane block ++++++++++++++
TChiWZ_1 = TChiWZ.addMassPlane(2*[[x, y]])
TChiWZ_1.figure = "FigAux 5b"
TChiWZ_1.figureUrl = "https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2013-12/figaux_05b.png"
TChiWZ_1.dataUrl = 'https://doi.org/10.17182/hepdata.63114.v1/t53'

TChiWZ_1.setSources(dataLabels= ['expExclusion', 'obsExclusion'],
                 dataFiles= ['orig/exc_tchiwz_expected.txt', 'orig/exc_tchiwz_obs.txt'],
                 dataFormats= ['txt', 'txt'])

TChiWZ_1.addSource('efficiencyMap',('orig/Table49.csv','orig/Table53.csv'), dataFormat='mcsv')
TChiWZ_1.efficiencyMap._unit = '0.0001'

TChiWZoff.addMassPlane(TChiWZ_1)


#+++++++ dataset block ++++++++++++++
obsN = [38.0, 87.0, 277.0, 122.0, 21.0, 6.0, 0.0, 0.0, 0.0, 0.0]
expBG = [31.0, 73.0, 264.5, 130.2, 18.2, 4.1, 1.9, 0.4, 0.4, 0.1]
bgErr = [2.1, 3.3, 11.2, 6.2, 1.5, 0.6, 0.4, 0.1, 0.1, 0.1]

obsN_summed = sum(obsN)
expBG_summed = sum(expBG)
bgErr_summed = sum(bgErr)

dsname = "SR2tau_a"
dataset = DataSetInput(dsname)
dataset.setInfo(dataType = 'efficiencyMap', dataId = dsname, observedN = obsN_summed, expectedBG = expBG_summed , bgError = bgErr_summed)
#+++++++ next txName block ++++++++++++++
TChiChipmStauL = dataset.addTxName('TChiChipmStauL')
TChiChipmStauL.constraint ="2.*([[['nu'],['ta']],[['ta+'],['ta-']]] + [[['ta'],['nu']] , [['ta+'],['ta-']]]+[[['nu'],['ta']],[['ta-'],['ta+']]] + [[['ta'],['nu']],[['ta-'],['ta+']]])"
TChiChipmStauL.conditionDescription ="[[['nu'],['ta']],[['ta+'],['ta-']]] ~ [[['ta'],['nu']],[['ta+'],['ta-']]],[[['nu'],['ta']],[['ta+'],['ta-']]] ~ [[['nu'],['ta']],[['ta-'],['ta+']]], [[['nu'],['ta']],[['ta+'],['ta-']]] ~ [[['ta'],['nu']],[['ta-'],['ta+']]]"
TChiChipmStauL.condition ="Csim([[['nu'],['ta']],[['ta+'],['ta-']]],[[['ta'],['nu']],[['ta+'],['ta-']]],[[['nu'],['ta']],[['ta-'],['ta+']]],[[['ta'],['nu']],[['ta-'],['ta+']]])"
TChiChipmStauL.source = "ATLAS"
#+++++++ next mass plane block ++++++++++++++
TChiChipmStauL050 = TChiChipmStauL.addMassPlane(2*[[x, x*0.5+(1.-0.5)*y, y]])
TChiChipmStauL050.figure = "FigAux 5c"
TChiChipmStauL050.figureUrl = "https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2013-12/figaux_05c.png"
TChiChipmStauL050.dataUrl = 'https://doi.org/10.17182/hepdata.63114.v1/t54'
TChiChipmStauL050.setSources(dataLabels= ['expExclusion', 'obsExclusion'],
                 dataFiles= ['orig/exc_stauL_expected.txt', 'orig/exc_stauL_obs.txt'],
                 dataFormats= ['txt', 'txt'])

TChiChipmStauL050.addSource('efficiencyMap',('orig/Table50.csv','orig/Table54.csv'), dataFormat='mcsv')
TChiChipmStauL050.efficiencyMap._unit = '0.0001'


#+++++++ dataset block ++++++++++++++
obsN = [5.0, 5.0, 5.0, 0.0]
expBG = [3.7, 7.2, 3.8, 3.5]
bgErr = [0.5, 0.8, 0.6, 0.5]

obsN_summed = sum(obsN)
expBG_summed = sum(expBG)
bgErr_summed = sum(bgErr)

dsname = "SR2tau_b"
dataset = DataSetInput(dsname)
dataset.setInfo(dataType = 'efficiencyMap', dataId = dsname, observedN = obsN_summed, expectedBG = expBG_summed , bgError = bgErr_summed)

#+++++++ next txName block ++++++++++++++
TChiWH = dataset.addTxName('TChiWH')
TChiWH.validationTarball = "TChiWH_8Tev.tar.gz"
TChiWH.constraint ="[[['W']],[['higgs']]]"
TChiWH.conditionDescription ="None"
TChiWH.condition ="None"
TChiWH.source = "ATLAS"
#+++++++ next mass plane block ++++++++++++++
TChiWH_1 = TChiWH.addMassPlane(2*[[x, y]])
TChiWH_1.figure = "FigAux 5d"
TChiWH_1.figureUrl = "https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2013-12/figaux_05d.png"
TChiWH_1.dataUrl = 'https://doi.org/10.17182/hepdata.63114.v1/t55'
TChiWH_1.setSources(dataLabels= ['expExclusion', 'obsExclusion'],
                 dataFiles= ['orig/exc_tchiwh_expected.txt', 'orig/exc_tchiwh_obs.txt'],
                 dataFormats= ['txt', 'txt'])

TChiWH_1.addSource('efficiencyMap',('orig/Table51.csv','orig/Table55.csv'), dataFormat='mcsv')
TChiWH_1.efficiencyMap._unit = '0.0001'


databaseCreator.create()
