##!/usr/bin/env python
#############################################################################################

from __future__ import print_function

import os
import sys
import optparse
import traceback

from configobj import ConfigObj 

try:
    from setproctitle import setproctitle
except ImportError:
    setproctitle = None

for path in [
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')),
    os.path.join('opt', 'diamond', 'lib'),
]:
    if os.path.exists(os.path.join(path, 'diamond', '__init__.py')):
        sys.path.append(path)
        break

from diamond.collector import Collector
from diamond.collector import str_to_bool

def getIncludePaths(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))
        
        # print('->', cPath)
        # print('syspath -> ', sys.path)

        if os.path.isfile(cPath) and len(f) > 3 and f[-3:] == '.py':
            sys.path.append(os.path.dirname(cPath))

    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))
        if os.path.isdir(cPath):
            getIncludePaths(cPath)

collectors = {}

def getCollectors(path):
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))
        if (os.path.isfile(cPath) and len(f) > 3 and f[-3:] == '.py' and f[0:4] != 'test'):
            modname = f[:-3]
            print('modname -->', modname)

            try:
                # Import the module
                module = __import__(modname, globals(), locals(), ['*'])
                # Find the name
                for attr in dir(module):
                    # print('attr -->', attr)

                    cls = getattr(module, attr)
                    # print('class -> ', cls )

                    try:
                        if (issubclass(cls, Collector) and cls.__name__ not in collectors):
                            collectors[cls.__name__] = module
                            break
                    except TypeError:
                        continue
                print("Imported module: %s %s" % (modname, cls.__name__))
            except Exception:
                print("Failed to import module: %s. %s" % (modname, traceback.format_exc()))
                collectors[modname] = False
                continue
                
    for f in os.listdir(path):
        cPath = os.path.abspath(os.path.join(path, f))
        if os.path.isdir(cPath):
            getCollectors(cPath)

def typeToString(key):
    if isinstance(obj.config[key], basestring):
        user_val = obj.config[key]
    elif isinstance( obj.config[key], bool):
        user_value = str(obj.config[key])
    elif isinstance(obj.config[key], int):
        user_value = str(obj.config[key])
    elif isinstance(obj.config[key], list):
        user_value = str(obj.config[key])[1:-1]
    else:
        raise NotImplementedError("Unknown type!")

    return user_val

def stringToType(key, value):
    if type( obj.config[key] ) is type(val):
        config_file[key]=value
    elif isinstance( obj.config[key], basestring):
        if val.lower() == 'false':
            config_file[key] = False
        elif val.lower() == 'true':
            config_file[key] = True
        else:
            raise NotImplementedError("Unknown type!") 

def boolCheck(val):
    if isinstance(val, basestring):
        return str_to_bool(val)
    elif isinstance(val, bool):
        return val
    else:
        raise NotImplementedError("Uknown type!")

def configureKey(key):
    if not config_keys[key]:
        return

    try:
        user_val = typeToString(key)
    except NotImplementedError:
        return

    print("\n")
    if key in default_conf_help:
        print(default_conf_help)
    val = raw_input(key + ' [' + user_value + ']: ')

    # Empty user input? Default to current value
    if len(val) == 0:
        val = obj.config[key]

    try:
        stringToType(key, val)
    except NotImplementedError:
        return

###########################################################################################################

if __name__ == '__main__':
    if setproctitle:
        setproctitle('diamond-setup')

    # Initialize Options
    parser = optparse.OptionParser()
    parser.add_option("-c", "--configfile", dest="configfile", default="/etc/diamond/diamond.conf", help="Path to the config file")
    parser.add_option("-C", "--collector", dest="collector", default=None, help="Configure a single collector")
    parser.add_option("-p", "--print", action="store_true", dest="dump", default=False, help="Just print the defaults")

    # Parse Command Line Args
    (options, args) = parser.parse_args()

    # Initialize Config
    if os.path.exists( options.configfile ):
        config = ConfigObj(os.path.abspath(options.configfile))
    else:
        print("ERROR: Config File: %s does not exist." % (options.configfile), file=sys.stderr)
        print("Please run python config.py -c /path/to/diamond.conf", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    if not options.dump:
        print('')
        print('I will be over writing files in')
        print(config['server']['collectors_config_path'])
        print('Please type yes to continue')

        val = input('Are you sure? ')
        if val != 'yes':
            sys.exit(1)

    getIncludePaths(config['server']['collectors_path'])
    getCollectors(config['server']['collectors_path'])
    sys.exit(-1)

    tests = []

    foundcollector = False
    for collector in collectors:
        if options.collector and collector != options.collector:
            continue

        # Skip configuring the basic collector object
        if collector == "Collector":
            continue

        foundcollector = True

        config_keys = []
        config_file = ConfigObj()
        config_file.filename = (config['server']['collectors_config_path'] + '/' + collector + ".conf")

        # Find the class and load it from the collector module  



