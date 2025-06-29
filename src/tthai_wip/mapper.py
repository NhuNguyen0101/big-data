#!/usr/bin/env python3
import sys

def mapper():
    current_movie_id = None
    for line in sys.stdin:
        line = line.strip()
        if line.endswith(":"):
            current_movie_id = line[:-1]
        elif current_movie_id and line:
            parts = line.split(",")
            if len(parts) == 3:
                customer_id, rating, _ = parts
                print(f"{customer_id}\\t{current_movie_id},{rating}")

if __name__ == "__main__":
    mapper()
