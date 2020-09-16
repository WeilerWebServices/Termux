When backups are enabled, this folder's per-run subfolders hold copies of prior versions
of items replaced or removed in test2, along with a __addedd__.txt giving new items added 
to test2.  

The subfolders are made automatically when test2 is the TO folder; they are excluded from 
comparisons and synchronization, and their __added__.txt is excluded from updates in mergeall's 
"-restore" mode.

The oldest subfolder here, "date150325-time115227", reflects the changes made for the test 
folders' starting state, run with FROM=test1 and TO=test2, in -auto -backup mode.  Later
runs reflect various changes made after th the initial synchronization.
