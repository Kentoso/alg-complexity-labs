from stringset import StringSet
import sys


def main():
    string_set = StringSet()
    count = 0

    for line in sys.stdin:
        line = line.strip()

        if line == "#":
            break

        if count >= 10**6:
            break

        operation, string = line.split()

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
