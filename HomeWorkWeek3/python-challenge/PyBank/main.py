import csv
import os

# Choose File Number 1 or 2
file_num = 1

# Create file path and save as file
file = os.path.join('Resources', 'budget_data_'+ str(file_num) +'.csv')

#Lists for month and revenue data
months = []
revenue = []

#Read csv and parse data into lists
#Revenue list will be list of integers
with open(file, 'r') as csvfile:
    readcsv = csv.reader(csvfile)
    
    next(readcsv, None)

    for row in readcsv:
        months.append(row[0])
        revenue.append(int(row[1]))

#Find total months
total_months = len(months)

#Create greatest increase, decrease variables and set them equal to the first revenue entry
#Set total revenue = 0 
greatest_inc = revenue[0]
greatest_dec = revenue[0]
total_revenue = 0

#Loop through revenue indices and compare # to find greatest inc and dec
#Also add each revenue to total revenue
for r in range(len(revenue)):
    if revenue[r] >= greatest_inc:
        greatest_inc = revenue[r]
        great_inc_month = months[r]
    elif revenue[r] <= greatest_dec:
        greatest_dec = revenue[r]
        great_dec_month = months[r]
    total_revenue += revenue[r]

#Calculate average_change
average_change = round(total_revenue/total_months, 2)

#Sets path for output file
output_dest = os.path.join('OutputFiles','pybank_output_file_' + str(file_num) + '.txt')

#Opens the output destination in write mode and prints the summary
with open(output_dest, 'w') as writefile:
    writefile.writelines('Financial Analysis\n')
    writefile.writelines('----------------------------' + '\n')
    writefile.writelines('Total Months: ' + str(total_months) + '\n')
    writefile.writelines('Total Revenue: $' + str(total_revenue) + '\n')
    writefile.writelines('Average Revenue Change: $' + str(average_change) + '\n')
    writefile.writelines('Greatest Increase in Revenue: ' + great_inc_month + ' ($' + str(greatest_inc) + ')'+ '\n')
    writefile.writelines('Greatest Decrease in Revenue: ' + great_dec_month + ' ($' + str(greatest_dec) + ')')

#opens the output file in r mode and prints to terminal
with open(output_dest, 'r') as readfile:
    print(readfile.read())    