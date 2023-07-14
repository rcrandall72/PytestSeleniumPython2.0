import json


with open("report.json") as report_file:
    data = json.load(report_file)

# Get the total test time
test_time = round(data["report"]["summary"]["duration"], 2)

# Get the list of failed tests
failed_tests = []
for item in data["report"]["tests"]:
    if item["outcome"] == "failed":
        failed_tests.append(item["name"].split("::")[-1])

no_passed = sum(1 for test in data["report"]["tests"] if test["outcome"] == "passed")
no_failed = sum(1 for test in data["report"]["tests"] if test["outcome"] == "failed")
no_skipped = sum(1 for test in data["report"]["tests"] if test["outcome"] == "skipped")

# Print the report
print("Test Summary:")
print(f"{no_passed} passed, {no_failed} failed, {no_skipped} skipped")
print(f"{test_time} seconds")
if failed_tests:
    print("Failed Tests:")
    for test in failed_tests:
        print(f"- {test}")