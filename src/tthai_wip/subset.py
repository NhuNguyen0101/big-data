import os
import shutil

# Define paths
input_dir = "../dataset"
output_dir = "subset_training_set"
movie_ids = set(str(i) for i in range(1, 1001))  # MovieIDs 1–1000
user_ids = set()  # Track selected users
max_users = 10000

os.makedirs(output_dir, exist_ok=True)

# Filter movie files
for file in os.listdir(input_dir):
    if file.startswith("mv_") and file.split("_")[1].zfill(7) in movie_ids:
        with open(os.path.join(input_dir, file), "r") as f:
            lines = f.readlines()
            movie_id = lines[0].split(":")[0]
            subset_lines = [lines[0]]  # Keep movie ID line
            for line in lines[1:]:
                customer_id = line.split(",")[0]
                if len(user_ids) < max_users:
                    user_ids.add(customer_id)
                    subset_lines.append(line)
                elif customer_id in user_ids:
                    subset_lines.append(line)
        # Write filtered file
        with open(os.path.join(output_dir, file), "w") as f:
            f.writelines(subset_lines)
