# Glucose
Analysis of glucose data got from a dexcom device. 
Basic ideea starts from the pattern recognition that could work on large amount of data in glucose patterns.

As output it has a database containg the values divided according to the inherent logic that a pattern- called ripple- will occur after two changes of graph direction.

#
## Setting up the enviorment

`python -m venv .venv`

## Activating the enviorment

`.venv\Scripts\activate`

## Deactivating the enviorment
`deactivate`


## Dependencies
#
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
### 4.Xlswritter
`pip install xlswritter`

#
### 5.PySimpleGui
`python pip -m install pysimplegui`


