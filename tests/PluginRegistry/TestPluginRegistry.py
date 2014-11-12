#!/usr/bin/env python2

import unittest
import os

from Cura.Application import Application
from Cura.PluginRegistry import PluginRegistry
from Cura.PluginError import PluginNotFoundError

class TestApplication(Application):
    def registerTestPlugin(self, name):
        self._test_plugin = name
        
    def getTestPlugin(self):
        return self._test_plugin

class TestPluginRegistry(unittest.TestCase):
    # Called before the first testfunction is executed
    def setUp(self):
        self._app = TestApplication()

    # Called after the last testfunction was executed
    def tearDown(self):
        pass

    def test_MetaData(self):
        registry = self._createRegistry()
        
        metaData = registry.getMetaData("TestPlugin")
        self.assertEqual("TestPlugin", metaData["name"])
        self.assertEqual("test", metaData["type"])

    def test_Load(self):
        registry = self._createRegistry()
        
        registry.loadPlugin("TestPlugin")
        self.assertEqual("TestPlugin", self._app.getTestPlugin())
    
    def test_LoadNested(self):
        registry = self._createRegistry()
        
        registry.loadPlugin("TestPlugin2")
        self.assertEqual("TestPlugin2", self._app.getTestPlugin())
        
    def test_FindAllPlugins(self):
        registry = self._createRegistry()
        
        names = registry._findAllPlugins()
        self.assertEqual(["TestPlugin", "TestPlugin2"], names)
        
    def test_PluginNotFound(self):
        registry = self._createRegistry()
        
        self.assertRaises(PluginNotFoundError, registry.loadPlugin, "NoSuchPlugin")
        
    def _createRegistry(self):
        registry = PluginRegistry()
        registry.addPluginLocation(os.path.dirname(os.path.abspath(__file__)))
        registry.setApplication(self._app)
        return registry

if __name__ == "__main__":
    unittest.main()
