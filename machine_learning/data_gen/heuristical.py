import csv
import random
from pathlib import Path

"""
Function that generates an aboutput based on a threshold of probability and noise
"""
def generate_output(a, b, threshold=0.8, noise=0.05):
    """
    Returns 'a' with probability equal to 'threshold', otherwise returns 'b'.
    """
    chance = random.random()
    if chance < noise:
      return random.choice([a,b])

    #double reroll is necessary because otherwise the data would be a bit skewed
    chance = random.random()
    if chance < threshold:
        return a
    return b

"""
Function that generates the synthetic data
"""
def generate_synthetic_data(limit=500):
    headers = [
        "ghost_job",
        "vagueness_score",
        "salary_present",
        "days_opened",
        "post_on_website",
        "hiring_timeline",
        "hiring_manager_listed",
        "repost_frequency_year",
    ]
    data = [headers]

    for _ in range(limit):
        ghost_job = random.choice([True, False])

        # Base threshold for ghost job traits
        threshold = 0.8

        # Invert probability if it is a legitimate job posting
        if not ghost_job:
            threshold = 1.0 - threshold

        # Sample feature values based on state
        vagueness_score = generate_output(random.uniform(7.0, 10.0), random.uniform(0.0, 3.0), threshold)
        salary_present = generate_output(False, True, threshold)
        days_opened = generate_output(random.uniform(35, 100), random.uniform(0, 35), threshold)
        post_on_website = generate_output(False, True, threshold)
        hiring_timeline = generate_output(False, True, threshold)
        repost_frequency_year = generate_output(random.randint(1, 2), random.randint(3, 20), threshold)

        threshold = 0.6 if ghost_job else 0.4

        hiring_manager_listed = generate_output(False, True, threshold)

        row = [
            ghost_job,
            round(vagueness_score, 2),
            salary_present,
            round(days_opened, 1),
            post_on_website,
            hiring_timeline,
            hiring_manager_listed,
            repost_frequency_year,
        ]

        data.append(row)

    return data

"""
Function that writes the heuristical dataset as a csv file 
"""
def write_csv(filename='heuristic.csv', limit=500):
    data = generate_synthetic_data(limit)

    try:
        with open(f"../data/{filename}", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"invalid file name has been used! {str(e)}")

    print(f"Successfully generated {limit} synthetic rows in {filename}")


if __name__ == "__main__":
    write_csv(limit=500)