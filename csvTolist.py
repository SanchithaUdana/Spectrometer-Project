import csv


def csv_to_two_lists(file_path):
    column1 = []
    column2 = []

    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # Skip the header if present
        next(csvreader, None)

        for row in csvreader:
            column1.append(row[0])  # First column data
            column2.append(row[1])  # Second column data

    return column1, column2


# Example usage:
file_path = 'data.csv'
list1, list2 = csv_to_two_lists(file_path)
print("List 1:", list1)
print("List 2:", list2)
