# coding=utf-8

import configobj
import os
import sys
import logging
import inspect
import traceback
import pkg_resources
import imp

from diamond.util import load_class_from_name
from diamond.collector import Collector
from diamond.handler.Handler import Handler

from diamond.utils.log import DebugFormatter

logger = logging.getLogger('diamond')
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(DebugFormatter())
logger.addHandler(streamHandler)

def load_collectors(paths):
    """
    Load all collectors 
    
    Arguments:
        paths {[type]} -- [description]
    """

    collectors = load_collectors_from_paths(paths)
    collectors.update(load_collectors_from_entry_point('diamond.collectors'))

    return collectors

def load_handlers(config, handler_names):
    """
    Load handlers
    
    Arguments:
        config {[type]} -- [description]
        handler_names {[type]} -- [description]
    """

    handlers = []

    if isinstance(handler_names, str):
        handler_names = [handler_names]

    for handler in handler_names:
        logger.debug("Loading Handler %s", handler)

        try:
            # Load Handler Class
            cls = load_dynamic_class(handler, Handler)
        except (ImportError, SyntaxError):
            # Log Error
            logger.warning("Failed to load hadler %s. %s", 
                handler, traceback.format_exc())

            continue

    return handlers

def load_dynamic_class(fqn, subclass):
    """
    Dynamically load fqn class and verify it's a subclass of `subclass`
    """
    if not isinstance(fqn, str):
        return fqn

    cls = load_class_from_name(fqn)
    print( "class:", cls, "... subclass:", subclass)
    print( "isSubclass:", issubclass(cls, subclass))
    print( cls.__bases__ )
    
    if cls == subclass or not issubclass(cls, subclass):
        raise TypeError("%s is not a valid %s" %(fqn, subclass.__name__))

    return cls

def load_include_path(paths):
    """
    Scan for and add paths to the include path
    
    Arguments:
        paths {[type]} -- [description]
    """

    for path in paths:
        # Verify is valid
        if not os.path.isdir(path):
            logger.error('Not a valid include path: %s' % path)
            continue
        # Add path to system path, to avoid name clashes
        if path not in sys.path:
            sys.path.insert(1, path)
        # Load all the files in path
        for f in os.listdir(path):
            # Are we a direcory ?
            fpath = os.path.join(path, f)
        
            if os.path.isdir(fpath):
                load_include_path([fpath])

    logger.debug("Sys Path is %s" % sys.path)

def load_collectors_from_paths(paths):
    """
    Scan for collectors to load from path
    """
    # Initialize return value
    collectors = {}

    if paths is None:
        return

    logger.debug("Load Collectors from Path(s): %s" % paths)

    if isinstance(paths, str):
        paths = paths.split(',')
        paths = map(str.strip, paths)

    paths = list(paths)
    
    load_include_path(paths)
    
    for path in paths:
        # Get a list of files in the directory, if the directory exists
        if not os.path.exists(path):
            raise OSError("Directory does not exist: %s" % path)

        if path.endswith('tests') or path.endswith('fixtures'):
            return collectors

        # Load all the files in the path
        for f in os.listdir(path):
            # Are we a directory? If so process down
            fpath = os.path.join(path, f)
            
            if os.path.isdir(fpath):
                subcollectors = load_collectors_from_paths([fpath])
                for key in subcollectors:
                    collectors[key] = subcollectors[key]

            # Ignore anything that isn' a .py file
            elif (os.path.isfile(fpath) and len(f) > 3 and 
                    f[-3:] == '.py' and f[0:4] != 'test' and f[0] != '.'
                    ):                
                modname = f[:-3]
                print(",,!!", modname)
                fp, pathname, description = imp.find_module(modname, [path])

                try:
                    # Import the module 
                    mod = imp.load_module(modname, fp, pathname, description)
                except (KeyboardInterrupt, SystemExit) as err:
                    logger.error(
                        "System or Keyboard Interrupt "
                        "while loading module %s" %modname)
                    if isinstance(err, SystemExit):
                        sys.exit(err.code)
                    raise KeyboardInterrupt
                except Exception:
                    # Log error
                    logger.error('Failed to import module: %s. %s',
                        modname, traceback.format_exc())
                else:
                    for name, cls in get_collectors_from_module(mod):
                        logger.debug("Found Collector: %s. %s", name, cls)
                        collectors[name] = cls
                finally:
                    if fp:
                        fp.close()

    # Return Collector classes
    return collectors

def load_collectors_from_entry_point(path):
    """
    Load collectors that were installed into an entry_point
    
    Arguments:
        path {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    collectors = {}
    for ep in pkg_resources.iter_entry_points(path):
        try:
            mod = ep.load()
        except Exception:
            logger.error('Failed to import entry_point: %s.%s',
                ep.name,
                traceback.format_exc())
        else:
            collectors.update(get_collectors_from_module(mod))
    return collectors

def get_collectors_from_module(mod):
    """
    Locate all of the collector classes within a given module
    
    Arguments:
        mod {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    for attrname in dir(mod):
        attr = getattr(mod, attrname)
        # Only attempting to load classes that are 
        # Collectors but NOT the bases class
        if ((inspect.isclass(attr) and 
            issubclass(attr, Collector) and 
            attr != Collector)):
            if attrname.startswith('parent_'):
                continue
            # Get class name
            fqcn = '.'.join([mod.__name__, attrname])
            try:
                # Load Collector class 
                cls = load_dynamic_class(fqcn, Collector)
                # Add Collector class
                yield cls.__name__, cls
            except Exception:
                # Log error
                logger.error(
                    "Failed to load Collector: %s. %s",
                    fqcn, traceback.format_exc())
                continue

def initialize_collector(cls, name=None, configfile=None, handlers=[]):
    """
    Initialize collector
    
    Keyword Arguments:
        name {[type]} -- [description] (default: {None})
        configfile {[type]} -- [description] (default: {None})
        handlers {list} -- [description] (default: {[]})
    
    Returns:
        [type] -- [description]
    """
    collector = None

    try:
        # Initialize collector 
        collector = cls(name=name, configfile=configfile, handlers=handlers)
    except Exception:
        # Log error
        logger.error("Failed to initialize Collector: %s. %s", 
            cls.__name__, traceback.format_exc() )

    # Return collector
    return collector


    # Return Collector classes
    return collectors

    