from stringset import StringSet
import sys


def main():
    string_set = StringSet()
    count = 0

    for line in sys.stdin:
        line = line.strip()

        if line == "#":
            palindromes = string_set.find_all_palindromes()
            print(f"Found {len(palindromes)} palindromes:")
            print(palindromes)
            break

        if count >= 10**6:
            break

        try:
            operation, string = line.split()
        except ValueError:
            print("Invalid input")
            continue

        if operation == "+":
            found = string_set.insert(string)
            print("ok" if found else "not found")
        elif operation == "-":
            found = string_set.delete(string)
            print("ok" if found else "not found")
        elif operation == "?":
            found = string_set.search(string)
            print("yes" if found else "no")

        count += 1


if __name__ == "__main__":
    main()
