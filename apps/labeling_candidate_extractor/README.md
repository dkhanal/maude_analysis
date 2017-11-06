maude_pre_labeling

This application goes through a set of input files and extracts *potential* positive and negative records. Four different sets of records are extracted:

- Potential Positive Records -- records that are likely to be positive.
- Potential Negative Records -- records that are likely to be negative
- Questionable Positive Records -- records that could be positive (with lower confidence)
- Questionable Negative Records -- records that could be negative (with lower confidence)

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