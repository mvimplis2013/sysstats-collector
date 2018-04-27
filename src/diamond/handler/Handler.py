import logging

class Handler():
    """
    Handlers process metrics that are collected by Collectors
    """
    def __init__(self, config=None, log=None):
        self.enabled=True

