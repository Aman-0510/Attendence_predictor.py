"""
PS 98 - Attendance Percentage Predictor
Fits a straight line (np.polyfit) on weekly attendance and predicts a future week.
"""

import sys

import numpy as np
import pandas as pd


def validate(attendance):
    """Return an error message (str) if data is invalid, else None."""
    if len(attendance) < 2:
        return "At least 2 weeks of data are required."
    if any(a < 0 or a > 100 for a in attendance):
        return "Attendance must be between 0 and 100."
    return None


def fit_line(weeks, attendance):
    """Best-fit straight line: attendance = slope * week + intercept."""
    slope, intercept = np.polyfit(weeks, attendance, 1)
    return float(slope), float(intercept)


def predict(weeks, attendance, target_week):
    """Validate, fit, predict. Prints the result. Returns True if successful."""
    error = validate(attendance)
    if error:
        print(error)
        return False

    slope, intercept = fit_line(weeks, attendance)
    raw = slope * target_week + intercept
    result = min(100.0, max(0.0, raw))  # cap between 0 and 100

    print(f"Slope: {slope:.2f} | Intercept: {intercept:.2f}")
    note = " (capped at 100)" if raw > 100 else " (capped at 0)" if raw < 0 else ""
    print(f"Predicted attendance for week {target_week}: {result:.2f}%{note}")
    if result >= 75:
        print("Safe")
    else:
        print("Warning: below 75%")
    return True


def read_csv(path):
    """CSV must have an 'attendance' column (optional 'week' column)."""
    df = pd.read_csv(path)
    attendance = df["attendance"].astype(float).tolist()
    if "week" in df.columns:
        weeks = df["week"].astype(float).tolist()
    else:
        weeks = list(range(1, len(attendance) + 1))
    return weeks, attendance


def read_manual():
    """Weeks are numbered 1, 2, 3... automatically."""
    raw = input("Enter weekly attendance % separated by commas (e.g. 90,88,86): ")
    attendance = [float(x) for x in raw.split(",") if x.strip() != ""]
    weeks = list(range(1, len(attendance) + 1))
    return weeks, attendance


def run_tests():
    """Runs all 4 test cases from the problem statement."""
    print("--- Test Case 1: Normal Input ---")
    predict([1, 2, 3, 4, 5], [90, 88, 86, 84, 82], 10)

    print("\n--- Test Case 2: Boundary / Minimum Input ---")
    predict([1, 2], [90, 80], 3)

    print("\n--- Test Case 3: Invalid Input ---")
    print("(a)", end=" ")
    predict([1], [90], 2)
    print("(b)", end=" ")
    predict([1, 2, 3], [90, 105, 80], 4)

    print("\n--- Test Case 4: Different Valid Scenario ---")
    predict([1, 2, 3, 4, 5], [70, 74, 78, 82, 86], 9)


def main():
    print("=== Attendance Percentage Predictor ===")
    print("1. Enter attendance manually")
    print("2. Load attendance from CSV file")
    print("3. Run all 4 test cases")
    choice = input("Choose (1/2/3): ").strip()

    try:
        if choice == "3":
            run_tests()
            return
        elif choice == "1":
            weeks, attendance = read_manual()
        elif choice == "2":
            path = input("CSV file path: ").strip()
            weeks, attendance = read_csv(path)
        else:
            print("Invalid choice.")
            return

        target = int(input("Predict for week number: "))
        predict(weeks, attendance, target)
    except ValueError:
        print("Invalid input. Please enter numbers only.")
    except (FileNotFoundError, KeyError):
        print("CSV file not found, or it has no 'attendance' column.")


if __name__ == "__main__":
    main()
    sys.exit(0)