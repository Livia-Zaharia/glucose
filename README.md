# Glucose
Analysis of glucose data got from a dexcom device. 
Basic idea starts from the pattern recognition that could work on large amount of data in glucose patterns.

The script was started as course assignment, so it might need improvement. It should be taken as a study material but not as it being a final version.

Simple explanation- whereas a CGM offers large amount of data, that data may be further analyzed by procedure that the standard app does not offer. As such I used my personal data to test it. The patterns I was searching for where similarity in the segments of the graph. Numerically defined, using a percentage to define similarity.

A segment of the graph is the class called ripple and represents a change of graph direction which has a certain amplitude.

The similarity in ripples can reveal where a certain pattern occurred and allow the circumstances to be analyzed in depth for treatment or to further personal study to discuss with the medic. 

As input
-cvs from Dexcom CGM

As output 
-a database containing the values of ripple instances (sql lite)
-database of statistics- interaction between ripples or traits of ripple (sql lite)
-summary of statistics (xls)
-folder containing data for each ripple in part- (html)(xls)


#
## Setting up the enviorment

`python -m venv .venv`

## Activating the enviorment

`.venv\Scripts\activate`

## Deactivating the enviorment
`deactivate`


## Dependencies
#
Can be installed individually or done by the requirements.txt file extracted from the tested version
### 1.Kaleido

`pip install kaleido`

*might require a previous version, especially on Windows 11 systems*

[issue explained here](https://stackoverflow.com/questions/69016568/unable-to-export-plotly-images-to-png-with-kaleido)

#
### 2. Pandas
`pip install pandas`

*note it will install as dependencies also numpy on which is based*
#
### 3. Plotly
`pip install plotly`

#
### 4.Openpyxl
`pip install openpyxl`

#
### 5.PySimpleGui
`python pip -m install pysimplegui`

#
### 6.SciPy
`python -m pip install scipy`



