## Import a library called "CSV"
import csv

## Open file and read into the raw text (from Quandl: https://www.quandl.com/FRED/GDP)
raw_text = open('FRED-GDP.csv', 'r')

## Create our two empty lists, in a dictionary
data = {"dates":[],
        "gdp":[]}

## Create a reader object using the CSV library. Skip the first line.
reader = csv.reader(raw_text, delimiter=',')
reader.next()

## Iterate over each line in the CSV file using the reader
for line in reader:
    ## Save the date
    data["dates"].append(line[0])
    
    ## Save the GDP value, which we first convert to a floating-point number (real number)
    data["gdp"].append(float(line[1]))

    
## Some Computations
print "Total GDP:",sum(data["gdp"])

print "Average GDP:",sum(data["gdp"])*1.0 / len(data["gdp"])

print "Highest GDP:",max(data["gdp"])


## Slow way of finding date with highest GDP
max_gdp = max(data["gdp"])
max_gdp_index = -1
for i in range(len(data["gdp"])):
    if data["gdp"][i] == max_gdp:
        max_gdp_index = i
print "Date with highest GDP (1):", data["dates"][max_gdp_index]


## Another way of finding date with highest GDP
print "Date with highest GDP (2):", data["dates"][data["gdp"].index(max(data["gdp"]))]


## Another way of finding date with highest GDP
print "Date with highest GDP (3):", max(zip(data["dates"],data["gdp"]), key = lambda x:x[1])[0]