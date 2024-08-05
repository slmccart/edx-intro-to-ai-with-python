import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence_list = []
    labels = []

    # In the CSV, columns 10, 15, 16, and 17 need special handling:
    #   Column 10: Month needs to be converted from 'AAA' to a zero-based month index 0-11
    #   Column 15: VisitorType needs to be converted from 'Returning_Visitor' or 'New_Visitor' to 1 or 0, respectively
    #   Column 16: Weekend needs to be converted from 'TRUE' or 'FALSE' to 1 or 0, respectively
    #   Column 17: Revenue needs to be converted from 'TRUE' or 'FALSE' to 1 or 0, respectively
    special_columns = [10, 15, 16]

    int_columns = [0, 2, 4, 11, 12, 13, 14]
    float_columns = [1, 3, 5, 6, 7, 8, 9]

    month_indices = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "May": 4,
        "June": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11,
    }

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        # Omit header row
        next(reader, None)
        for row in reader:
            # Put every element except the last into evidence, converting special elements as needed
            evidence = []
            for i in range(len(row[:-1])):
                if i in int_columns:
                    evidence.append(int(row[i]))
                elif i in float_columns:
                    evidence.append(float(row[i]))
                else:
                    match i:
                        case 10:  # Month
                            evidence.append(month_indices[row[i]])
                        case 15:  # VisitorType
                            if row[i] == "Returning_Visitor":
                                evidence.append(1)
                            else:
                                evidence.append(0)
                        case 16:  # Weekend
                            if row[i] == "TRUE":
                                evidence.append(1)
                            else:
                                evidence.append(0)

            evidence_list.append(evidence)

            # Convert last element from 'TRUE' or 'FALSE' to 1 or 0
            label = row[-1]
            if label == "TRUE":
                labels.append(1)
            else:
                labels.append(0)

    return (evidence_list, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
