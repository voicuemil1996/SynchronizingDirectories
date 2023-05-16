The purpose of this script is to synchronize two folders: source and replica.
Synchronization is made to be one-way, source->replica (after synchronization is done, the replica folder should contain exactly the same content as source).
Synchronization is done periodically, depending of sync_interval parameter, during the time the script runs (running_time parameter).

The script can be run using command line parameters.
eg: python main.py -s "sourced" -r "replica" -si 5 -rt 10

To see more info about command line parameters, use: python main.py -h.
