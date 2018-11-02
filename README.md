# Sheet Clean

`What is this?`  
This is a python script to get all the following from a xlsx file
- country code, country name, and phone number from numbers
- city, country from address

## What you need
- This script
- The Excel file to verify all the Emails ( are they valid )
- Max data 10,000 fields

## How

- open terminal
- Get the script
```
git clone https://github.com/Faisal-Manzer/xclean.git
```
- Go into folder
```
cd sheet-clean
```
- install all requirements
```
pip install -r requirements.txt
```
- Run the script
```
python3 app.py
```

- Select the File
- Set options
- Wait, the cleaned file will be automatically saved. For 10,000 data it will take 10 min approx

## Take Care
- Remove all formatting from excel file `Home > Clear > All Format` in Excel Ribbon
- Should contain a `Name` filed (case sensitive)
- Max size is 10,000
