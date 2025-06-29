import sys
import os

def mapper():
    current_movie_id = None
    for line in sys.stdin:
        line = line.strip()
        if line.endswith(":"):
            current_movie_id = line[:-1]  # Remove colon
        elif current_movie_id and line:
            parts = line.split(",")
            if len(parts) == 3:
                customer_id, rating, _ = parts
                print(f"{customer_id}\t{current_movie_id},{rating}")

def reducer():
    for line in sys.stdin:
        customer_id, value = line.strip().split("\t")
        movie_id, rating = value.split(",")
        print(f"{customer_id},{movie_id},{rating}")

if __name__ == "__main__":
    # Determine if running as mapper or reducer based on filename or argument
    script_name = os.path.basename(sys.argv[0])
    if "mapper" in script_name or (len(sys.argv) > 1 and sys.argv[1] == "mapper"):
        mapper()
    elif "reducer" in script_name or (len(sys.argv) > 1 and sys.argv[1] == "reducer"):
        reducer()
