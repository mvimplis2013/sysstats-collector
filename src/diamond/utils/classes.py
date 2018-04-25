# coding=utf-8

import configobj
import os
import sys
import logging
import inspect
import traceback
import pkg_resources
import imp

logger = logging.getLogger('diamond')

def load_collectors(paths):
    """
    Load all collectors 
    
    Arguments:
        paths {[type]} -- [description]
    """

    collectors = load_collectors_from_paths(paths)
    collectors.update(load_collectors_from_entry_point('diamond.collectors'))

    return collectors

def load_include_path(paths):
    """
    Scan for and add paths to the include path
    
    Arguments:
        paths {[type]} -- [description]
    """

    for path in paths:
        # Verify is valid
        if not os.path.isdir(path):
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

def load_collectors_from_paths(paths):
    """
    Scan for collectors to load from path
    """
    # Initialize return value
    collectors = {}

    if paths is None:
        return

    if isinstance(paths, basestring):
        paths = paths.split(',')
        paths = map(str.strip, paths)

    load_include_path(paths)
    
    for path in paths:
        # Get a list of files in the directory, if the directory exists
        if not os.pasth.exists(path):
            raise OSError("Directory does not exist: %s" % path)

        if path.endswith('tests') or path.endswith('fixtures'):
            return collectors

        # Load all the files in the path
        for f in os.listdir(path):
            # Are we a directory? If so process down

    # Return Collector classes
    return collectors

    