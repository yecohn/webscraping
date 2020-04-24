# PublicWelfare
PublicWelfare is a project that measures the indexes (characteristics) that affect people's welfare.

## Installation Requirements
Run the following via command line in order to install the packages you need to run the project using the package manager [pip](https://pip.pypa.io/en/stable/)
```
pip install -r requirements.txt
```

## How to run the program
Run the command "python --table <subject1> <year1>" to receive only one table of a certain subject and a certain year.
subject: cost-of-living, crime, health-care, quality-of-life, property-investment, traffic, pollution.
year: 2013, 2014, 2015, 2016, 2017
You can add as many arguments as you want in one command as long as it's in the following format:
"python --table <subject1> <year1> <subject2> <year2> <subject3> <year3>...<subjectN> <yearN>"
You can also run "python --all_tables" to receive all of the tables (all subjects, all years).
You also have "--help" in which all the above is explained again in the console.

## Authors
[Yaniv Cohen](https://github.com/yaniv92648)

[Yehoshua Cohen](https://github.com/yosh01123)
