# By Deepak Khanal
# dkhanal@gmail.com

class FoiTextRow():
    def __init__(self, **kwargs):

        # Each record has the following format: MDR_REPORT_KEY|MDR_TEXT_KEY|TEXT_TYPE_CODE|PATIENT_SEQUENCE_NUMBER|DATE_REPORT|FOI_TEXT
        self.raw_line = kwargs['line']

        self.fields = self.raw_line.split('|')

        number_of_fields = len(self.fields)

        # Set up a named accessor for each field
        if number_of_fields > 0:
            self.mdr_report_key = self.fields[0]

        if number_of_fields > 1:
            self.mdr_text_key = self.fields[1]

        if number_of_fields > 2:
            self.text_type_code = self.fields[2]

        if number_of_fields > 3:
            self.patient_sequence_number = self.fields[3]

        if number_of_fields > 4:
            self.date_report = self.fields[4]

        if number_of_fields > 5:
            self.foi_text = self.fields[5]

        return super().__init__()

