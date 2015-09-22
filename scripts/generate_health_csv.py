# Copyright 2014 Open Connectome Project (http://openconnecto.me)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author  : Kunal Lillaney
# Email   : lillaney@jhu.edu
# Date    : Sep 21, 2015

# This file converts the csv located at the DATA location to the desired format for the purposes for JHUDash 2015.
# DATA - http://hcup-us.ahrq.gov/faststats/StatePayerServlet?state1=NY&type1=SL05&combo1=s&state2=&type2=SL05&combo2=s&expansionInfoState=hide&dataTablesState=hide&definitionsState=hide&exportState=show

import csv
import argparse
from collections import Counter

def read_files(file_name):
  """Read the xlx files"""

  # Creating a list of all years
  years_row = range(2003,2013,1)
  acc_values = {}
  states_values = {}
  # Reading the csv file
  with open(file_name, 'rb') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
      
      # Accumlating years over quarters
      for year in years_row:
        acc_values[year] = 0
        for value in sorted(row.keys()):
          if str(year) in value:
            acc_values[year] += int(row[value] if row[value] !='' else 0)
      
      # Separating out the types of patients
      if not states_values.has_key(row['State']):
        # If entry does not exist then create it
        states_values[row['State']] = {}
      else:
        # Sum the values based on various factors
        if states_values[row['State']].has_key(row['Expected_Payer']):
          test = Counter(states_values[row['State']][row['Expected_Payer']])
          test.update(Counter(acc_values))
          states_values[row['State']][row['Expected_Payer']] = dict(test)
        else:
          states_values[row['State']][row['Expected_Payer']] = acc_values

  # Writing the output csv files
  for file_name in ['Medicare','Uninsured','Medicaid','Private']:
    with open('{}.csv'.format(file_name), 'wb') as csv_file:
      csv_writer = csv.writer(csv_file)
      # Writing the header for the csv file
      csv_writer.writerow(['State']+[str(i) for i in years_row])
      # Writing the actual data
      for state in sorted(states_values.keys()):
        csv_writer.writerow([state]+states_values[state][file_name].values())


def main():
  """Take in the arguments for user"""

  parser = argparse.ArgumentParser(description='Input')
  parser.add_argument('file_name', action='store', help='Directory Name')
  result = parser.parse_args()
  
  # Call the function to read the data csv and generate the csv
  read_files(result.file_name)

if __name__ == '__main__':
  main()
