#!/usr/bin/env python3
import warnings
import os

# Suppress ALL warnings at the earliest possible point
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.simplefilter("ignore")

from src.cli.interface import main

if __name__ == "__main__":
    main()
