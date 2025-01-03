# pylint: skip-file
import base64
import csv
import json
import re

import alibabacloud_oss_v2 as oss
from . import TestIntegration, OBJECTNAME_PREFIX, random_str


class TestSelectObject(TestIntegration):
    def test_select_object_csv(self):
        def select_call_back(consumed_bytes, total_bytes=None):
            print('Consumed Bytes:' + str(consumed_bytes) + '\n')

        data = "name,school,company,age\nLora Francis,School,Staples Inc,27\n#Lora Francis,School,Staples Inc,27\nEleanor Little,School,\"Conectiv, Inc\",43\nRosie Hughes,School,Western Gas Resources Inc,44\nLawrence Ross,School,MetLife Inc.,24\n"
        key = 'select_object_csv.csv'
        expression = 'select * from ossobject'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
            content_type='text/txt',
        ))
        self.assertEqual(200, result.status_code)

        request = oss.SelectObjectRequest(
            headers={'content-length': '422'},
            bucket=self.bucket_name,
            key=key,
            select_request=oss.SelectRequest(
                expression=base64.b64encode(expression.encode()).decode(),
                input_serialization=oss.InputSerialization(
                    compression_type=None,
                    csv_input=oss.CSVInput(
                        file_header_info='Ignore',
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character=base64.b64encode('\"'.encode()).decode(),
                        comment_character=base64.b64encode('#'.encode()).decode(),
                        allow_quoted_record_delimiter=True,
                    ),
                ),
                output_serialization=oss.OutputSerialization(
                    csv_output=oss.CSVOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character=base64.b64encode('\"'.encode()).decode(),
                    ),
                    output_raw_data=False,
                    keep_all_columns=True,
                    enable_payload_crc=True,
                    output_header=False,
                ),
                options=oss.SelectOptions(
                    skip_partial_data_record=False,
                ),
            ),
            progress_callback=select_call_back,
        )
        result = self.client.select_object(request)
        self.assertIsNotNone(result)
        self.assertEqual(206, result.status_code)
        content = b''
        try:
            for chunk in result.body:
                content += chunk
        except Exception as e:
            print(e)
        self.assertEqual(str(data.split('#')[1]).encode(), content)

    def test_select_object_csv_file_concat(self):
        key = 'sample_data_concat.csv'
        expression = "select Year,StateAbbr, CityName, Short_Question_Text from ossobject where (data_value || data_value_unit) = '14.8%'"
        file_path = '../tests/data/sample_data.csv'

        result = self.client.put_object_from_file(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ), file_path)
        self.assertEqual(200, result.status_code)

        request = oss.SelectObjectRequest(
            bucket=self.bucket_name,
            key=key,
            select_request=oss.SelectRequest(
                expression=base64.b64encode(expression.encode()).decode(),
                input_serialization=oss.InputSerialization(
                    csv_input=oss.CSVInput(
                        file_header_info='Use',
                    ),
                ),

            ),
        )
        result = self.client.select_object(request)
        self.assertIsNotNone(result)
        self.assertEqual(206, result.status_code)

        content = b''
        try:
            for chunk in result.body:
                content += chunk
        except Exception as e:
            print(e)
        print(f'content: {content}')

        select_data = b''
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                line = b''
                if row['Data_Value_Unit'] == '%' and row['Data_Value'] == '14.8':
                    line += row['Year'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['StateAbbr'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['CityName'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['Short_Question_Text'].encode('utf-8')
                    line += '\n'.encode('utf-8')
                    select_data += line

            print(select_data)
            self.assertEqual(select_data, content)

    def test_select_object_csv_file_complicate_condition(self):
        key = 'sample_data_complicate_condition.csv'
        expression = "select Year,StateAbbr, CityName, Short_Question_Text, data_value, data_value_unit, category, high_confidence_limit from ossobject where data_value > 14.8 and data_value_unit = '%' or Measure like '%18 Years' and Category = 'Unhealthy Behaviors' or high_confidence_limit > 70.0 "
        file_path = '../tests/data/sample_data.csv'

        result = self.client.put_object_from_file(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ), file_path)
        self.assertEqual(200, result.status_code)

        request = oss.SelectObjectRequest(
            bucket=self.bucket_name,
            key=key,
            select_request=oss.SelectRequest(
                expression=base64.b64encode(expression.encode()).decode(),
                input_serialization=oss.InputSerialization(
                    csv_input=oss.CSVInput(
                        file_header_info='Use',
                    ),
                ),

            ),
        )
        result = self.client.select_object(request)
        self.assertIsNotNone(result)
        self.assertEqual(206, result.status_code)

        content = b''
        try:
            for chunk in result.body:
                content += chunk
        except Exception as e:
            print(e)
        print(f'content: {content}')


        matcher = re.compile('^.*18 Years$')
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            select_data = b''
            spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                line = b''
                if len(row['Data_Value']) > 0 and float(row['Data_Value']) > 14.8 and row['Data_Value_Unit'] == '%' or matcher.match(row['Measure']) and row['Category'] == 'Unhealthy Behaviors' or len(row['High_Confidence_Limit']) > 0 and float(row['High_Confidence_Limit']) > 70.0:
                    line += row['Year'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['StateAbbr'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['CityName'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['Short_Question_Text'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['Data_Value'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['Data_Value_Unit'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['Category'].encode('utf-8')
                    line += ','.encode('utf-8')
                    line += row['High_Confidence_Limit'].encode('utf-8')
                    line += '\n'.encode('utf-8')
                    select_data += line
            print(select_data)
            self.assertEqual(select_data, content)

    def test_select_object_json(self):
        data = "{\t\"name\":\"Eleanor Little\",\n\t\"age\":43,\n\t\"company\":\"Conectiv, Inc\"}\n{\t\"name\":\"Rosie Hughes\",\n\t\"age\":44,\n\t\"company\":\"Western Gas Resources Inc\"}\n"

        key = "select_object_json.json"
        expression = 'select * from ossobject as s where cast(s.age as int) > 40'
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
        ))
        self.assertEqual(200, result.status_code)

        request = oss.SelectObjectRequest(
            bucket=self.bucket_name,
            key=key,
            select_request=oss.SelectRequest(
                expression=base64.b64encode(expression.encode()).decode(),
                input_serialization=oss.InputSerialization(
                    compression_type=None,
                    json_input=oss.JSONInput(
                            type='LINES',
                            parse_json_number_as_string=True,
                    ),
                ),
                output_serialization=oss.OutputSerialization(
                    json_output=oss.JSONOutput(
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                    ),
                    output_raw_data=False,
                    keep_all_columns=True,
                    enable_payload_crc=True,
                    output_header=False,
                ),
                options=oss.SelectOptions(
                    skip_partial_data_record=False,
                ),
            ),
        )
        result = self.client.select_object(request)
        self.assertIsNotNone(result)
        self.assertEqual(206, result.status_code)
        content = b''
        try:
            for chunk in result.body:
                content += chunk
        except Exception as e:
            print(e)

        self.assertEqual(data.replace("\t", "").replace(",\n", ",").encode(), content)

    def test_select_object_json_file_line_range(self):
        key = 'sample_json_lines_line_range.json'
        expression = "select person.firstname as aaa as firstname, person.lastname, extra from ossobject'"
        json_file_path = '../tests/data/sample_json.json'
        json_lines_path = '../tests/data/sample_json_lines.json'

        result = self.client.put_object_from_file(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ), json_lines_path)
        self.assertEqual(200, result.status_code)

        request = oss.CreateSelectObjectMetaRequest(
            bucket=self.bucket_name,
            key=key,
            json_meta_request=oss.JsonMetaRequest(
                input_serialization=oss.InputSerialization(
                    json_input=oss.JSONInput(
                        type='LINES',
                    ),
                ),
            ),
        )

        result = self.client.create_select_object_meta(request)

        request = oss.SelectObjectRequest(
            bucket=self.bucket_name,
            key=key,
            select_request=oss.SelectRequest(
                expression=base64.b64encode(expression.encode()).decode(),
                input_serialization=oss.InputSerialization(
                    json_input=oss.JSONInput(
                        type='LINES',
                        range='line-range=10-50',
                    ),

                ),
                output_serialization=oss.OutputSerialization(
                    json_output=oss.JSONOutput(
                        record_delimiter=base64.b64encode(','.encode()).decode(),
                    )
                )
            ),
        )
        result = self.client.select_object(request)
        self.assertIsNotNone(result)
        self.assertEqual(206, result.status_code)

        content = b''
        try:
            for chunk in result.body:
                content += chunk
        except Exception as e:
            print(e)
        print(f'content: {content}')

        content = content[0:len(content) - 1]  # remove the last ','
        content = b"[" + content + b"]"  # make json parser happy
        result = json.loads(content.decode('utf-8'))

        result_index = 0
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            index = 0
            for row in data['objects']:
                select_row = {}
                if index >= 10 and index < 50:
                    select_row['firstname'] = row['person']['firstname']
                    select_row['lastname'] = row['person']['lastname']
                    select_row['extra'] = row['extra']
                    self.assertEqual(result[result_index], select_row)
                    result_index += 1
                elif index >= 50:
                    break
                index += 1

    def test_select_object_json_file_complicate_condition(self):
        key = 'sample_json_linesz_complicate_condition.json'
        expression = "select person.firstname, person.lastname, congress_numbers from ossobject where startdate > '2017-01-01' and senator_rank = 'junior' or state = 'CA' and party = 'Republican'"
        json_file_path = '../tests/data/sample_json.json'
        json_lines_path = '../tests/data/sample_json_lines.json'

        result = self.client.put_object_from_file(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
        ), json_lines_path)
        self.assertEqual(200, result.status_code)

        request = oss.CreateSelectObjectMetaRequest(
            bucket=self.bucket_name,
            key=key,
            json_meta_request=oss.JsonMetaRequest(
                input_serialization=oss.InputSerialization(
                    json_input=oss.JSONInput(
                        type='LINES',
                    ),
                ),
            ),
        )
        result = self.client.create_select_object_meta(request)

        request = oss.SelectObjectRequest(
            bucket=self.bucket_name,
            key=key,
            select_request=oss.SelectRequest(
                expression=base64.b64encode(expression.encode()).decode(),
                input_serialization=oss.InputSerialization(
                    json_input=oss.JSONInput(
                        type='LINES',
                    ),

                ),
                output_serialization=oss.OutputSerialization(
                    json_output=oss.JSONOutput(
                        record_delimiter=base64.b64encode(','.encode()).decode(),
                    )
                )
            ),
        )
        result = self.client.select_object(request)
        self.assertIsNotNone(result)
        self.assertEqual(206, result.status_code)

        content = b''
        try:
            for chunk in result.body:
                content += chunk
        except Exception as e:
            print(e)
        print(f'content: {content}')

        content = content[0:len(content) - 1]  # remove the last ','
        content = b"[" + content + b"]"  # make json parser happy
        result = json.loads(content.decode('utf-8'))

        result_index = 0
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            for row in data['objects']:
                if row['startdate'] > '2017-01-01' and row['senator_rank'] == 'junior' or row['state'] == 'CA' and row['party'] == 'Republican':
                    self.assertEqual(result[result_index]['firstname'], row['person']['firstname'])
                    self.assertEqual(result[result_index]['lastname'], row['person']['lastname'])
                    self.assertEqual(result[result_index]['congress_numbers'], row['congress_numbers'])
                    result_index += 1

    def test_select_object_csv_metadata(self):
        key = 'select_object_metadata_csv.csv'
        data = "name,school,company,age\nLora Francis,School,Staples Inc,27\nEleanor Little,School,\"Conectiv, Inc\",43\nRosie Hughes,School,Western Gas Resources Inc,44\nLawrence Ross,School,MetLife Inc.,24"
        key = OBJECTNAME_PREFIX + random_str(16)

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
            content_type='text/txt',
        ))
        self.assertEqual(200, result.status_code)

        request = oss.CreateSelectObjectMetaRequest(
            bucket=self.bucket_name,
            key=key,
            csv_meta_request=oss.CsvMetaRequest(
                overwrite_if_exists=True,
                input_serialization=oss.InputSerialization(
                    compression_type=None,
                    csv_input=oss.CSVInput(
                        file_header_info='NONE',
                        record_delimiter=base64.b64encode('\n'.encode()).decode(),
                        field_delimiter=base64.b64encode(','.encode()).decode(),
                        quote_character=base64.b64encode('\"'.encode()).decode(),
                    ),
                ),
            ),
        )

        result = self.client.create_select_object_meta(request)

        content = b''
        try:
            for chunk in result.body:
                content += chunk
        except Exception as e:
            print(e)
        print(f'content: {content}')

        self.assertEqual(5, result.body.select_resp.rows)
        self.assertEqual(1, result.body.select_resp.splits)

    def test_select_object_json_metadata(self):
        key = 'select_object_metadata_json.json'
        data = "{\n\t\"name\": \"Lora Francis\",\n\t\"age\": 27,\n\t\"company\": \"Staples Inc\"\n}\n{\n\t\"k2\": [-1, 79, 90],\n\t\"k3\": {\n\t\t\"k2\": 5,\n\t\t\"k3\": 1,\n\t\t\"k4\": 0\n\t}\n}\n{\n\t\"k1\": 1,\n\t\"k2\": {\n\t\t\"k2\": 5\n\t},\n\t\"k3\": []\n}"
        key = OBJECTNAME_PREFIX + random_str(16)

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            acl=oss.ObjectACLType.PRIVATE,
            body=data,
            content_type='text/txt',
        ))
        self.assertEqual(200, result.status_code)

        request = oss.CreateSelectObjectMetaRequest(
            bucket=self.bucket_name,
            key=key,
            json_meta_request=oss.JsonMetaRequest(
                overwrite_if_exists=True,
                input_serialization=oss.InputSerialization(
                    json_input=oss.JSONInput(
                        type='LINES',
                    ),
                    compression_type=None,
                ),
            ),
        )

        result = self.client.create_select_object_meta(request)

        content = b''
        try:
            for chunk in result.body:
                content += chunk
        except Exception as e:
            print(e)
        print(f'content: {content}')

        self.assertEqual(3, result.body.select_resp.rows)
        self.assertEqual(1, result.body.select_resp.splits)