import os
from filecmp import dircmp
from shutil import copytree, copy2
from time import sleep

COPY_DIR_MESSAGE = "Copied directory {} from {} to {}"
COPY_FILE_MESSAGE = "Copied {} from {} to {}"
DELETE_DIR_MESSAGE = "Deleted directory {} from {}"
DELETE_FILE_MESSAGE = "Deleted file {} from {}"


class Synchronizer:

    def __init__(self, source, replica, sync_interval, running_time=60):
        self._source = os.path.abspath(source)
        self._replica = os.path.abspath(replica)
        self._sync_interval = sync_interval
        self._running_time = running_time
        self._output_data = ""
        self._curr_log = ""

    def synchronize(self):
        time_counter = 0
        while time_counter < self._running_time:
            self._synchronize_directories(self._source, self._replica)
            sleep(self._sync_interval)
            time_counter += self._sync_interval

        with open('log.txt', 'w') as f:
            f.truncate(0)
            f.write(self._output_data)

    def _synchronize_directories(self, source_dir, replica_dir):
        """This method synchronize two directories. If there is a common directory, the algorithm will compare what is
           inside the directories by calling this recursively.
        """
        comparison = dircmp(source_dir, replica_dir)
        if comparison.common_dirs:
            for directory in comparison.common_dirs:
                self._synchronize_directories(os.path.join(source_dir, directory), os.path.join(replica_dir, directory))
        files_to_be_copied = []
        if comparison.right_only:
            self._delete(replica_dir, comparison.right_only)
        for file in comparison.left_only:
            files_to_be_copied.append(file)
        for file in comparison.diff_files:
            files_to_be_copied.append(file)
        self._copy(files_to_be_copied, source_dir, replica_dir)

    def _copy(self, file_list, src, dest):
        """Copy files and subdirectories from source directory to destination directory
        """
        for file in file_list:
            src_path = os.path.join(src, os.path.basename(file))
            if os.path.isdir(src_path):
                copytree(src_path, os.path.join(dest, os.path.basename(file)))
                self._curr_log = COPY_DIR_MESSAGE
            else:
                copy2(src_path, dest)
                self._curr_log = COPY_FILE_MESSAGE

            self._curr_log = self._curr_log.format(os.path.basename(src_path), os.path.dirname(src_path), dest)
            self._print_curr_log()

    def _delete(self, directory, file_list):
        """Delete files and subdirectories from directory
        """
        for file in file_list:
            path = os.path.join(directory, file)
            if os.path.isdir(path):
                files = os.listdir(path)
                self._delete(path, files)
                os.rmdir(path)
                self._curr_log = DELETE_DIR_MESSAGE
            else:
                os.remove(path)
                self._curr_log = DELETE_FILE_MESSAGE
            self._curr_log = self._curr_log.format(file, directory)
            self._print_curr_log()

    def _print_curr_log(self):
        print(self._curr_log)
        self._output_data += self._curr_log + '\n'
