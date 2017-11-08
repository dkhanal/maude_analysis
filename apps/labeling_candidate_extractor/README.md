Labeling Candidate Extractor

The MAUDE dataset published by the FDA is not labeled. This application goes through each file in the MAUDE dataset and determines if a particular record is 'positive' or 'negative' candidate. To achieve this, explict and strong string matches are performed. The output of this application are a set of these files:

`<input_filename>.pos.txt` => Positive records
`<input_filename>.neg.txt` => Negative records
`<input_filename>.maybe.neg.txt` => Potentially negative records, but were rejected due to a potential positive signal.
`<input_filename>.maybe.pos.txt` => Potentially positive records, but were rejected due to a potential negative signal.
`<input_filename>.process.txt` => A processing log file with a specific reason for why a particular record was deemed positive or negative.

To Run:

```
python main.py
```

For cloud-integration, make sure to add a file called .setenv.py and include these lines:

```
import os

os.environ['azure_account_name'] = '<azure account name>'
os.environ['azure_account_key'] = '<azure account key>'

```