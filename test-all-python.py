#!/usr/bin/python

# Copyright (c) 2014, Alexander Belchenko
# All rights reserved.
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided
# that the following conditions are met:
#
# * Redistributions of source code must retain
#   the above copyright notice, this list of conditions
#   and the following disclaimer.
# * Redistributions in binary form must reproduce
#   the above copyright notice, this list of conditions
#   and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the author nor the names
#   of its contributors may be used to endorse
#   or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" Ad-hoc test runner against multiple python versions. """

import subprocess
import sys
import time


PYTHONS = (
    # display name, executable [full] path
    #('2.3', 'C:\Python23\python'),     # 2.3 is not supported
    ('2.4', 'C:\Python24\python'),
    ('2.5', 'C:\Python25\python'),
    ('2.6-32bit', 'C:\Python26-32bit\python'),
    ('2.6-64bit', 'C:\Python26-64bit\python'),
    ('2.7-32bit', 'C:\Python27-32bit\python'),
    ('2.7-64bit', 'C:\Python27-64bit\python'),
    ('3.3-32bit', 'C:\Python33-32bit\python'),
    ('3.3-64bit', 'C:\Python33-64bit\python'),
    )


def main():
    retcode = 0
    not_found = []
    failed = []
    print('%s started: %s\n' % (__file__, time.asctime()))
    for display_name, executable in PYTHONS:
        if checkPythonExists(display_name, executable):
            if not runTestWithPython(display_name, executable):
                retcode = 1
                failed.append(display_name)
        else:
            not_found.append(display_name)
    if failed or not_found:
        print('\n' + '-'*20)        
    if failed:
        print('Tests failed with pythons: %s' % (', '.join(failed)))
    if not_found:
        print('Not found python versions: %s' % (', '.join(not_found)))
    return retcode

def checkPythonExists(display_name, executable):
    """ Run `python -V` and check that it runs OK. """
    sys.stdout.write('Check presence of python %s ... ' % display_name)
    cmd = '%s -V' % executable
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        exc = sys.exc_info()[1]     # current exception
        sys.stdout.write('ERROR\n  Exception: %s\n' % str(exc))
        return False
    stdout, stderr = p.communicate()
    retcode = p.poll()
    output = ''
    if stdout:
        output = stdout.decode('ascii', 'replace')
    elif stderr:
        output = stderr.decode('ascii', 'replace')        
    output = output.replace('\r', '')
    if not output.endswith('\n'):
        output = output + '\n'
    sys.stdout.write(output)
    return retcode == 0

def runTestWithPython(display_name, executable):
    """ Runs `$(PYTHON) setup.py test -q` """
    cmd = '%s setup.py test -q' % executable
    sys.stdout.write('   Running tests against %s ... ' % display_name)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    retcode = p.poll()
    if retcode == 0:
        sys.stdout.write('OK\n')
        return True
    else:
        sys.stdout.write('FAILED\n')
        return False

if __name__ == '__main__':
    sys.exit(main())