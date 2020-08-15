import logging
import subprocess

from loopy.constants.Arguments import ARGUMENT_ID_HOST, ARGUMENT_ID_PORT, ARGUMENT_ID_SERVICE

class Executor:
    def __init__(self):
        pass


class ShellExecutor(Executor):
    def __init__(self):
        super(ShellExecutor, self).__init__()

    # os.subprocess expects an array to execute
    def exec_cmd(self, cmd, args, target, input=None):

        cmd_list = list()
        cmd_list.append(cmd)

        for arg in args:
            if ARGUMENT_ID_HOST in arg:
                arg = arg.replace(ARGUMENT_ID_HOST, target.get_host())

            if ARGUMENT_ID_PORT in arg:
                arg = arg.replace(ARGUMENT_ID_PORT, str(target.get_port()))
            
            if ARGUMENT_ID_SERVICE in arg:
                arg = arg.replace(ARGUMENT_ID_SERVICE, target.get_host())

            cmd_list.append(arg)

        logging.debug('Executing {}'.format(cmd_list))

        process = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if input:
            process.stdin.write(bytes(input))
        (out, err) = process.communicate()

        # stdout
        if out:
            out = out.decode('utf-8')

        # stderr
        if err:
            err = err.decode('utf-8')

        return {'output' : out, 'errors' : err} 