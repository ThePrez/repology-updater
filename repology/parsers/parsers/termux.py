# Copyright (C) 2018 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import json
import re

from repology.parsers import Parser
from repology.parsers.maintainers import extract_maintainers
from repology.parsers.versions import VersionStripper


class TermuxJsonParser(Parser):
    def iter_parse(self, path, factory, transformer):
        normalize_version = VersionStripper().strip_left_greedy(':')

        with open(path, 'r', encoding='utf-8') as jsonfile:
            for packagedata in json.load(jsonfile):
                pkg = factory.begin()

                pkg.set_name(packagedata['name'])
                pkg.set_version(packagedata['version'], normalize_version)

                pkg.set_summary(packagedata['description'])
                pkg.add_homepages(packagedata['homepage'])
                pkg.add_downloads(packagedata.get('srcurl'))

                match = re.search(' @([^ ]+)$', packagedata['maintainer'])
                if match:
                    pkg.add_maintainers(match.group(1).lower() + '@termux')
                else:
                    pkg.add_maintainers(extract_maintainers(packagedata['maintainer']))

                yield pkg
