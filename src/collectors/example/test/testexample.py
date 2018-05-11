#!/usr/bin/env python
# coding=utf-8
##################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch

from diamond.collector import Collector
from example import ExampleCollector

##################################################

class TestExampleCollector(CollectorTestCase):
    
    def setUp(self):
        config = get_collector_config('ExampleCollector', {
            'interval': 10
        })

        self.collector = ExampleCollector(config, None)

    def test_import(self):
        self.assertTrue(ExampleCollector)

    @patch.object(Collector, 'publish')
