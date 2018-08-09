import csv


with open('Hourly Messages.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    messages = []
    for line in reader:
        #line= "".join(line)
        messages.append(line)
        #print(line[0][0])
    print(messages)
