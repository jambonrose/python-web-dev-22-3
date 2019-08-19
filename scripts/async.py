#!/usr/bin/env python3
"""Demonstrate async/await by mimiciking IO with sleep"""

import asyncio
from time import perf_counter


async def mimic_io():
    """Pretend to perform disk/network IO"""
    print("Start")
    await asyncio.sleep(1)
    print("Finish")


async def main():
    """Perform multiple IO calls asynchronously"""
    await asyncio.gather(mimic_io(), mimic_io(), mimic_io())


if __name__ == "__main__":
    s = perf_counter()
    asyncio.run(main())
    elapsed = perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
