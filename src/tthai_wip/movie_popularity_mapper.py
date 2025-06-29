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
                rating = parts[1]
                print(f"{current_movie_id}\\t{rating}")
if __name__ == "__main__":
    mapper()
