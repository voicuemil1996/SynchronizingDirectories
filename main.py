from synchronizer import Synchronizer
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

if __name__ == "__main__":

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--source", default="source", type=str, help="Path to source folder")
    parser.add_argument("-r", "--replica", default="replica", type=str, help="Path to replica folder")
    parser.add_argument("-si", "--sinterval", default=5, type=int, help="Synchronizing time period in seconds")
    parser.add_argument("-rt", "--rtime", default=60, type=int, help="Running time period")
    args = vars(parser.parse_args())
    source = args["source"]
    replica = args["replica"]
    sync_interval = args["sinterval"]
    running_time = args["rtime"]

    synchronizer_obj = Synchronizer(source, replica, sync_interval, running_time)
    synchronizer_obj.synchronize()
