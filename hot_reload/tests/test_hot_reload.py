from multiprocessing import Pipe
from os import remove

from hot_reload.hot_reload import HotReload


class TestHotReload:
    def test_hot_reload_create_empty(self):
        output_pipe, input_pipe = Pipe()
        hot_reload = HotReload([], input_pipe)
        assert hot_reload.files_to_watch == []
        assert hot_reload.files_checking == {}
        assert hot_reload.pipe_input == input_pipe

    def test_hot_reload_watch_file(self):
        # TODO Tmp solution, need to mock file
        file_name = "test_file"
        with open(file_name, "w") as new_file:
            new_file.write("a")
        output_pipe, input_pipe = Pipe()
        hot_reload = HotReload(["test_file"], input_pipe)
        hot_reload.run()
        with open(file_name, "a") as new_file:
            new_file.write("n")
        assert output_pipe.recv() == [file_name]
        hot_reload.stop()
        remove(file_name)
