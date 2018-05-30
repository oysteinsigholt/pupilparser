import csv
import json

drawings = {}
responses = []

with open('form_responses.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	i = 0
	for row in reader:
		responses.append(row)
		i += 1

for i in range(len(responses[0])):
	drawing = i//5
	attribute = i%5

	drawings[drawing] = [
		{"name": "originality",
		"ratings": []},
		{"name": "creativity",
		"ratings": []},
		{"name": "flexibility",
		"ratings": []},
		{"name": "elaboration",
		"ratings": []},
		{"name": "fluency",
		"ratings": []},
	]

for n in range(len(responses)):
	for i in range(len(responses[0])):
		drawing = i//5
		attribute = i%5

		drawings[drawing][attribute]["ratings"].append(int(responses[n][i]))

for drawing in range(len(drawings)):
	for attribute in range(len(drawings[drawing])):
		drawings[drawing][attribute]["mean"] = float(sum(drawings[drawing][attribute]["ratings"])) / float(len(drawings[drawing][attribute]["ratings"]))

print json.dumps(drawings, indent=4)
