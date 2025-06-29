#!/usr/bin/env python3
import sys
def reducer():
    current_movie = None
    sum_ratings = 0
    count_ratings = 0
    for line in sys.stdin:
        movie_id, rating = line.strip().split("\\t")
        rating = float(rating)
        if current_movie == movie_id:
            sum_ratings += rating
            count_ratings += 1
        else:
            if current_movie:
                avg_rating = sum_ratings / count_ratings if count_ratings > 0 else 0
                print(f"{current_movie},{avg_rating:.2f}")
            current_movie = movie_id
            sum_ratings = rating
            count_ratings = 1
    if current_movie:
        avg_rating = sum_ratings / count_ratings if count_ratings > 0 else 0
        print(f"{current_movie},{avg_rating:.2f}")
if __name__ == "__main__":
    reducer()
