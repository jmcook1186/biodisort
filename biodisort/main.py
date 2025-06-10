#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from biosnicar.drivers import get_albedo

# call easy albedo func
albedo = get_albedo.get("adding-doubling", plot=True, validate=True)
