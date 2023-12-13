# Copyright 2019 Antonio Terceiro
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =*= License: GPL-3+ =*=

import cliapp
import logging
import tempfile

import vmdb


class RamdiskPlugin(cliapp.Plugin):

    def enable(self):
        self.app.step_runners.add(RamdiskStepRunner())


class RamdiskStepRunner(vmdb.StepRunnerInterface):

    def get_required_keys(self):
        return ['ramdisk']

    def run(self, step, setting, state):
        tag = step['ramdisk']
        chroot = state.tags.get_mount_point(tag)
        mount_point = state.tags.get_mount_point(tag)
        fname = state.filename.split('.')[0]
        initrd = '{}.initrd'.format(fname)
        kernel = '{}.kernel'.format(fname)
        cp_kernel = 'find boot/ -type f -name "vmlinu*" -exec cp {{}} {} \;'.format(kernel)
        cmd = ("cd {} && find . | LC_ALL=C sort | cpio --quiet -o -H newc | "
               "xz -9e -T0 --check=crc32 > {} && {}").format(mount_point, initrd, cp_kernel)
        fd, path = tempfile.mkstemp()
        with open(fd, 'w') as file_:
            file_.write(cmd)
        logging.info("********************************************************")
        logging.info("********************************************************")
        logging.info("*********** Creating ramdisk, please wait... ***********")
        logging.info("********************************************************")
        logging.info("********************************************************")
        output = vmdb.runcmd(['bash', path])
