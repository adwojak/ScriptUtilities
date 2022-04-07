from multiprocessing import Process
from os import stat
from time import sleep


class HotReload:
    def __init__(self, files_to_watch, pipe_input):
        self.files_to_watch = files_to_watch
        self.pipe_input = pipe_input
        self.files_checking = self._get_files_checking()
        self.process = Process(target=self._start_reload_process, daemon=True)

    def run(self):
        self.process.start()

    def stop(self):
        self.process.terminate()

    def _start_reload_process(self):
        while self.process.is_alive():
            changed_files = []
            for file in self.files_to_watch:
                last_modify_time = stat(file).st_mtime
                if self.files_checking[file] != last_modify_time:
                    changed_files.append(file)
                    self.files_checking[file] = last_modify_time
            if changed_files:
                self.pipe_input.send(changed_files)
            sleep(1)

    def _get_files_checking(self):
        return {file: stat(file).st_mtime for file in self.files_to_watch}
