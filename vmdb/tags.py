# Copyright 2018  Lars Wirzenius
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


import vmdb


class Tags:

    def __init__(self):
        self._tags = {}
        self._tagnames = []

    def get_tags(self):
        return list(self._tags.keys())

    def has_tag(self, tag):
        return tag in self._tags

    def get_dev(self, tag):
        item = self._get(tag)
        return item['dev']

    def get_mount_point(self, tag):
        item = self._get(tag)
        return item['mount_point']

    def get_fstype(self, tag):
        item = self._get(tag)
        return item['fstype']

    def append(self, tag):
        if tag in self._tags:
            raise TagInUse(tag)
        self._tagnames.append(tag)
        self._tags[tag] = {
            'dev': None,
            'mount_point': None,
            'fstype': None,
        }

    def set_dev(self, tag, dev):
        item = self._get(tag)
        if item['dev'] is not None:
            raise AlreadyHasDev(tag)
        item['dev'] = dev

    def set_mount_point(self, tag, mount_point):
        item = self._get(tag)
        if item['mount_point'] is not None:
            raise AlreadyMounted(tag)
        item['mount_point'] = mount_point

    def set_fstype(self, tag, fstype):
        item = self._get(tag)
        if item['fstype'] is not None:
            raise AlreadyHasFsType(tag)
        item['fstype'] = fstype

    def _get(self, tag):
        item = self._tags.get(tag)
        if item is None:
            raise UnknownTag(tag)
        return item


class TagInUse(Exception):

    def __init__(self, tag):
        super().__init__('Tag already used: {}'.format(tag))


class UnknownTag(Exception):

    def __init__(self, tag):
        super().__init__('Unknown tag: {}'.format(tag))


class AlreadyHasDev(Exception):

    def __init__(self, tag):
        super().__init__('Already has device: {}'.format(tag))


class AlreadyMounted(Exception):

    def __init__(self, tag):
        super().__init__('Already mounted tag: {}'.format(tag))


class AlreadyHasFsType(Exception):

    def __init__(self, tag):
        super().__init__('Already has filesystem type: {}'.format(tag))
