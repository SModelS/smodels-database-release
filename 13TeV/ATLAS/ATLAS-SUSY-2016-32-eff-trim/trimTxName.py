#!/usr/bin/python3

# %% Load required modules
import os,sys,time
import numpy as np
from scipy.spatial import ConvexHull
import logging
import matplotlib.pyplot as plt
import seaborn as sns

FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT,datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)



def rmGridPoints(txdata,points=None):
    """
    Remove points from the TxNameData object.
    If points is a list of indices, it will remove the respective points, otherwise
    one point will be removed from each simplex.

    :param txdata: TxNameData object containing the data grid points as the "data" attribute.

    :param points: list of indices to be removed from txdata. If None, one point will be removed from each simplex.

    :return: TxNameData object corresponding to the grid with removed points. The new (trimmed) data grid points are stored in the "data" attribute.
    """

    #Use input list to remove points
    if points:
        reducedGrid = [pt for i,pt in enumerate(txdata.data) if not i in points]
        txRed = TxNameData(reducedGrid, tx.dataType, 'dataReduced')
        txRed.data = reducedGrid
        return txRed

    #Get convex hull:
    cHull = ConvexHull(txdata.tri.points)

    iremove = []
    isimpRm = set([])
    #Loop over points and store indices of points to be removed:
    for ipt,pt in enumerate(txdata.tri.points):
        if pt in cHull.points[cHull.vertices]: continue #Skip points at the edge (convexHull)
        #Get list of simplices containing point
        isimpList = set([isimp for isimp,simplex in enumerate(txdata.tri.simplices) if ipt in simplex])
        #Do not remove point if any of the simplices already had a point removed:
        if isimpList.intersection(isimpRm): continue
        iremove.append(ipt)
        isimpRm.update(isimpList)

    reducedGrid = [pt for i,pt in enumerate(txdata.data) if not i in iremove]

    #Construct a TxNameData object with the reduced grid
    try:
        txRed = TxNameData(reducedGrid, tx.dataType, 'dataReduced')
        txRed.data = reducedGrid
    except Exception as e:
        logger.error("Could not create TxNameData object with data given: %s" %e)
        sys.exit()

    return txRed


def testInterpolation(txRed,txdata):
    """
    Use the newGrid to compute values for points which only appear in dataGrid.
    Return a list of with the indices of points in dataGrid and their relative difference to the
    interpolation using reducedGrid.
    The check ignores points with zero efficiencies/upper limits.

    The TxNameData object is used to transform the reducedGrid and interpolate.

    :param txdata: TxNameData object containing the original data grid points as the "data" attribute.

    :pram txRed: TxNameData object corresponding to the grid with removed points. The new (trimmed) data grid points are stored in the "data" attribute.

    :return: 2D array with indices of points present only in txdata, the relative difference between the interpolation using txRed
             and the original value (obtained from txdata.data).
    """

    diffs = []
    for ipt,pt in enumerate(txdata.data):
        if pt in txRed.data: continue
        if not pt[1]: continue #skip points with zero


        reldiff = abs(txRed.getValueFor(pt[0])-pt[1])/pt[1]
        diffs.append([ipt,reldiff,pt[1]])

    return diffs


def trimGrid(txdata,maxdiff=0.05,maxiter=10):
    """
    Try to reduce the given dataGrid removing points so the relative difference in testInterpolation
    is never above maxdiff. Points with values (efficiencies or upper limits) above minval are ignored.

    :param txdata: TxNameData object containing the original data grid points as the "data" attribute.

    :param madiff: Maximum allowed relatived difference in interpolation in order for a point to be removed.

    :return: the reduced TxNameData object (the reduced points are stored in the data attribute).
    """

    nremoved = 1 #numer of points removed in last iteration
    inputTx = txdata
    niter = 0
    maxd = 0.0

    print("Trimming original data with %i points >" %(len(dataGrid)), end="" )
    while nremoved > 0 and niter < maxiter and maxd < maxdiff:

        print( ".", end="", flush=True )

        #First remove points uniformly using the simplices:
        trialTx = rmGridPoints(inputTx)

        logger.debug("Removed %i trial points" %(len(inputTx.data) - len(trialTx.data)))

        #Now check the differences in interpolation between both grids
        #exactly at the points removed:
        diff = testInterpolation(trialTx,inputTx)

        #Identify good points to be removed:
        removePoints = []
        for d in diff:
            ipt = d[0]
            relDiff = d[1]
            val = d[2]
            if relDiff < maxdiff:
                removePoints.append(ipt)

        logger.debug("Removing %i points" %(len(removePoints)))

        #Get the reduced grid with only the good points removed:
        txRed = rmGridPoints(inputTx,removePoints)

        nremoved = len(inputTx.data) - len(txRed.data)
        niter += 1
        #Now do the same with the reduced grid:
        inputTx = txRed
        #Check the interpolation against the original data
        diff = testInterpolation(txRed,txdata)
        maxd = max([d[1] for d in diff])
        logger.debug("Maximum relative difference at iteration %i = %1.3f " %(niter,maxd))


    print( "< done after %i iterations" %niter)

    return txRed


if __name__ == "__main__":


    import argparse
    ap = argparse.ArgumentParser( description=
            "Remove (redundant) points from an upper limit or efficiency map grid. Points will be removed until the new grid differs by maxdiff." )
    ap.add_argument('-f', '--inputfile', required=True,
            help='path to TxName file to be trimmed.')
    ap.add_argument('-o', '--outputfile', required=True,
            help='name of the output data file. The file be a copy of the original file, with the upperLimits or efficiencyMap data grid replaced by the trimmed grid.')
    ap.add_argument('-P', '--plot', action='store_true',
            help='If set, will plot the resulting grids (only for 2D data grids).')
    ap.add_argument('-d', '--maxdiff', required=False, type=float, default = 0.05,
            help='Maximum relative difference allowed for interpolation (defaul = 0.05)')
    ap.add_argument('-m', '--minval', required=False, type=float, default = 1e-10,
            help='Minimum value for y values. Values below this limit, it will be automatically removed (defaul = 1e-10)')
    ap.add_argument('-smodelsPath', '--smodelsPath', required=False, default = '~/smodels',
            help='Path to smodels folder (default = ~/smodels).')
    ap.add_argument('-v', '--verbose', default='info',
            help='verbose level (debug, info, warning or error). Default is error')

    t0 = time.time()
    args = ap.parse_args()


    level = args.verbose.lower()
    levels = { "debug": logging.DEBUG, "info": logging.INFO,
               "warn": logging.WARNING,
               "warning": logging.WARNING, "error": logging.ERROR }
    if not level in levels:
        logger.error ( "Unknown log level ``%s'' supplied!" % level )
        sys.exit()
    logger.setLevel(level = levels[level])


    smodelsPath = os.path.expanduser(args.smodelsPath)
    if not os.path.isdir(smodelsPath):
        logger.error("SModelS folder %s not found" %smodelsPath)
        sys.exit()

    sys.path.append(smodelsPath)
    from smodels.experiment.txnameObj import TxNameData
    from smodels.tools.physicsUnits import GeV,fb,pb,TeV

    #%% Get data
    if not os.path.isfile(args.inputfile):
        logger.error("Data file %s not found" %args.inputfile)

    dataBlock = None
    dataType = None
    with open(args.inputfile,'r') as f:
        d = f.read()
        if 'upperLimits' in d:
            dataBlock = d.split('upperLimits:')[1]
            dataType = 'upperLimits'
        elif 'efficiencyMap' in d:
            dataBlock = d.split('efficiencyMap:')[1]
            dataType = 'efficiencyMap'
    if not dataBlock:
        logger.error("Blocks upperLimits and efficiencyMap not found in %s" %args.inputfile)
        sys.exit()

    if 'expected' in dataBlock:
        dataBlock = dataBlock.split('expected')[0]

    try:
        data = eval(dataBlock,{'fb' : fb, 'pb' : pb, 'GeV' : GeV, 'TeV' : TeV})
    except:
        logger.error("Error extracting grid from %s. Does it contain other units than fb, pb, GeV or TeV?" %args.inputfile)


    dataGrid = [pt for pt in data if pt[1] > args.minval]
    print(len(dataGrid))
    print(dataGrid[:3])
    #Get original txnamedata:
    tx = TxNameData(dataGrid, dataType, 'dataReduced')
    tx.data = dataGrid

    #points with efficiencies/upper limits below this value will be removed:
    minval = args.minval
    #maximum allowed relative difference between original and trimmed grid (after removing low value points):
    maxdiff = args.maxdiff

    txRed = trimGrid(tx,maxdiff=maxdiff,maxiter=15)

    #Sanity check: finally compare the final grid with the original one and check
    #if the differences added up too much:
    diff = testInterpolation(txRed,tx)
    maxdiff = max([d[1] for d in diff if d[2] > 1e-10])
    logger.info("Maximum interpolation difference = %1.3f " %(maxdiff))
    logger.info('Final grid length = %i' %len(txRed.data))


    if args.plot:
        basename = os.path.basename(args.outputfile)
        basename = os.path.splitext(basename)[0]
        iremoved = [pt[0] for pt in diff]
        ikept = [i for i,pt in enumerate(dataGrid) if not i in iremoved]

        plot = basename+"_DiffHist.png"
        #Plot hitogram of diffs:
        fig = plt.figure(figsize=(10,8))
        plt.hist(100*np.array(diff)[:,1],bins=50)
        plt.xlabel("Relative difference (%)")
        plt.ylabel("Number of points")
        plt.savefig(plot)
        logger.info("Saved plot %s" %plot)


        #Special plots for 2D data:
        if tx.dimensionality == 2:
            plotA = '%s_gridRm.png' %basename
            plotB = '%s_gridComp.png' %basename
            # %%
            #Plot original grid, removed points and final difference in interpolation
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15,6))
            axes[0].triplot(tx.tri.points[:,0], tx.tri.points[:,1], tx.tri.simplices.copy())
            axes[0].scatter(tx.tri.points[iremoved][:,0],tx.tri.points[iremoved][:,1],color='red', label = 'Points Removed')
            # plt.yscale('log')
            axes[0].legend()
            axes[0].set_title("Original simplices")
            im = axes[1].scatter(tx.tri.points[iremoved,0],tx.tri.points[iremoved,1],c=[d[1] for d in diff],
                                 vmin=0.,vmax=0.2,s=35,cmap=plt.cm.get_cmap('RdYlBu'))
            cb = fig.colorbar(im)
            axes[1].set_title("Relative Difference")
            plt.tight_layout()
            plt.savefig(plotA)
            logger.info("Saved plot %s" %(plotA))

            interpData = []
            for pt in dataGrid:
                if pt in reducedGrid:
                    interpData.append(pt[1])
                else:
                    interpData.append(txRed.getValueFor(pt[0]))

            fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(20,6))
            axes[0].scatter(tx.tri.points[:,0],tx.tri.points[:,1],c=tx.y_values,s=35,cmap=plt.cm.get_cmap('RdYlBu'))
            axes[0].set_title("Original Grid")

            axes[1].scatter(tx.tri.points[:,0],tx.tri.points[:,1],c=interpData,s=35,cmap=plt.cm.get_cmap('RdYlBu'))
            axes[1].scatter(tx.tri.points[ikept,0],tx.tri.points[ikept,1],s=40,facecolor='none',edgecolors='g',
                            label='Points kept')
            axes[1].legend()
            axes[1].set_title("Interpolation with Reduced Grid")
            im = axes[2].scatter(tx.tri.points[:,0],tx.tri.points[:,1],c=interpData/tx.y_values,s=40,
                            cmap=plt.cm.get_cmap('RdYlBu'),vmin = 0.5, vmax=1.5)
            cb = fig.colorbar(im)
            axes[2].set_title("Ratio of grids")
            plt.tight_layout()
            plt.savefig(plotB)

            logger.info("Saved plot %s" %(plotB))

    logger.info('Done in %1.2f min' %((time.time()-t0)/60.))
