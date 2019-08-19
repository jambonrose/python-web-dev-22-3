"""Run synchronous script mimicking IO with sleep"""
from time import perf_counter, sleep


def mimic_io():
    """Pretend to perform disk/network IO"""
    print("Start")
    sleep(1)
    print("Finish")


def main():
    """Perform multiple IO calls synchronously"""
    mimic_io()
    mimic_io()
    mimic_io()


if __name__ == "__main__":
    s = perf_counter()
    main()
    elapsed = perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
