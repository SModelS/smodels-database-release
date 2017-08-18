.. image:: docs/manual/source/images/banner720.png

================
SModelS Database
================

SModelS stores all the information about the experimental results in the Database.
The Database is organized as files in an ordinary (UNIX) directory hierarchy, with a thin Python
layer serving as the access to the database.

The :ref:`Database <Database>` is organized as files in an ordinary (UNIX)
directory hierarchy, with a thin Python layer serving as the access to the
database.  The overall structure of the directory hierarchy and its contents is
depicted in the scheme below (click to enlarge):

.. image:: docs/manual/source/images/DatabaseFolders.png
   :width: 80%


Installation
============

The installation procedure explained above also installs SModelS'
:ref:`database of experimental results <databaseStruct>`
in the smodels-database subdirectory.
The complete list of analyses and results included in the database can be
consulted at `http://smodels.hephy.at/wiki/ListOfAnalysesv11 <http://smodels.hephy.at/wiki/ListOfAnalysesv11>`_.
We note that all the results in the official database release have been
carefully validated  and the validation material can be
found at `http://smodels.hephy.at/wiki/Validationv11 <http://smodels.hephy.at/wiki/Validationv11>`_.

The database can conveniently be updated independently from SModelS code
updates. It suffices to unpack any new database tarball and replace the database
directory. In the same fashion, one can easily add additional results as
explained below.


.. _addingFastlim:

Adding FastLim data
^^^^^^^^^^^^^^^^^^^

The official SModelS database can be augmented with data from the
`fastlim <http://cern.ch/fastlim>`_ database.
A tarball with the *properly converted* fastlim-1.0 efficiency maps is provided and
needs to be exploded in the top level directory of the database.

That is, the following steps need to be performed ::

 mv smodels-v1.1-fastlim-1.0.tgz <smodels-database folder>
 cd <smodels-database folder>
 tar -xzvf smodels-v1.1-fastlim-1.0.tgz
 rm smodels-v1.1-fastlim-1.0.tgz

Once the fastlim folders have been added to the database,
SModelS auto-detects fastlim results and issues an acknowledgement.
When using these results, please properly cite the fastlim paper; for
convenience, a bibtex file is provided in the smodels-fastlim tarball.


Adding one's own results
^^^^^^^^^^^^^^^^^^^^^^^^

Adding additional experimental results is a matter of copying and editing text
files. Once the new folders and files have been added following the
:ref:`database structure format <folderStruct>`, SModelS
automatically rebuilds the binary (Pickle) database file.
The added results will then be available for using with the
the SModelS tools.


For citing the experimental analyses in the database, you can use
*smodels-database/database.bib*.

.. _SModelS online manual: http://smodels.readthedocs.io/
