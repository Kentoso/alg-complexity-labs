import random
import string
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

from stringset import StringSet


def generate_random_words(num_words, max_length=15):
    """
    Generates a list of random words consisting of lowercase letters a-z.

    Parameters:
        num_words (int): Number of words to generate.
        max_length (int): Maximum length of each word.

    Returns:
        list[str]: List of randomly generated words.
    """
    words = []
    for _ in range(num_words):
        length = random.randint(1, max_length)
        word = "".join(random.choices(string.ascii_lowercase, k=length))
        words.append(word)
    return words


def main():
    start = 1000
    end = 10**6
    step = 10000
    max_word_length = 15
    num_steps = (end - start) // step + 1

    word_counts = []
    execution_times = []

    string_set = StringSet()

    with tqdm(total=num_steps, desc="Testing StringSet") as pbar:
        for num_words in range(start, end + 1, step):
            words = generate_random_words(num_words, max_length=max_word_length)

            for word in words:
                string_set.insert(word)

            start_time = time.perf_counter()
            palindromes = string_set.find_all_palindromes()
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time

            word_counts.append(num_words)
            execution_times.append(elapsed_time)

            pbar.update(1)

            string_set.clear()

    plt.figure(figsize=(12, 6))
    plt.scatter(word_counts, execution_times, s=10, alpha=0.5)
    plt.title("Execution Time for find_all_palindromes vs. Number of Words")
    plt.xlabel("Number of Words")
    plt.ylabel("Time Taken (seconds)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.savefig("palindrome_execution_time.png")


if __name__ == "__main__":
    main()
