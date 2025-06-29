#!/usr/bin/env python3
import sys

def reducer():
    for line in sys.stdin:
        customer_id, value = line.strip().split("\\t")
        movie_id, rating = value.split(",")
        print(f"{customer_id},{movie_id},{rating}")

if __name__ == "__main__":
    reducer()
