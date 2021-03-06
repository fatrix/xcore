# Copyright (c) 2011 Philip Sahli from sahli.net

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from fabric.api import *

def dotcloud_upgrade_pip():
    local("dotcloud run %(dotcloud_service)s -- pip install --upgrade -r current/%(pip_requirement_file)s" % env)

def dotcloud_push():
    local("dotcloud push -b %(dotcloud_git_branch)s %(dotcloud_service)s ." % env)

def dotcloud_pip():
    local("dotcloud run %(dotcloud_service)s -- pip install -r current/%(pip_requirement_file)s" % env)

def dotcloud_deploy_upgrade():
    dotcloud_push()
    dotcloud_upgrade_pip()
    dotcloud_syncdb()
    dotcloud_restart()

def dotcloud_syncdb():
    local("dotcloud run %(dotcloud_service)s -- python current/%(module)s/manage.py syncdb" % env)
    local("dotcloud run %(dotcloud_service)s -- python current/%(module)s/manage.py migrate" % env)


def dotcloud_restart():
    local("dotcloud restart %(dotcloud_service)s" % env)

def dotcloud_deploy():
    dotcloud_push()
    dotcloud_pip()
    dotcloud_syncdb()
    dotcloud_restart()
