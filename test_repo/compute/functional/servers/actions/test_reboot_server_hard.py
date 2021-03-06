"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import time

from cafe.drivers.unittest.decorators import tags
from cloudcafe.compute.common.types import NovaServerRebootTypes
from test_repo.compute.fixtures import ComputeFixture


class RebootServerHardTests(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RebootServerHardTests, cls).setUpClass()
        response = cls.compute_provider.create_active_server()
        cls.server = response.entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RebootServerHardTests, cls).tearDownClass()

    @tags(type='smoke', net='yes')
    def test_reboot_server_hard(self):
        """ The server should be power cycled """
        public_address = self.compute_provider.get_public_ip_address(self.server)
        remote_instance = self.compute_provider.get_remote_instance_client(self.server, public_address)
        uptime_start = remote_instance.get_uptime()
        start = time.time()

        self.compute_provider.reboot_and_await(self.server.id, NovaServerRebootTypes.HARD)
        remote_client = self.compute_provider.get_remote_instance_client(self.server, public_address)
        finish = time.time()
        uptime_post_reboot = remote_client.get_uptime()
        self.assertLess(uptime_post_reboot, (uptime_start + (finish - start)))

