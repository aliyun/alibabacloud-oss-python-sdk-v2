
# pylint: skip-file
import os
import time
import random
import io
import alibabacloud_oss_v2 as oss
from . import TestIntegration, random_str

class TestAppendOnlyFile(TestIntegration):
    def test_append_file_bytes_only(self):
        key = 'append_file-' + random_str(6)
        data1 = "helle world"
        data2 = random_str(12345)
        data3 = random_str(100*1024*5 + 1234)
        mix_data = data1 + data2 + data3

        self.assertFalse(self.client.is_object_exist(self.bucket_name, key))

        # open empty
        append_f: oss.AppendOnlyFile = None
        with self.client.append_file(self.bucket_name, key) as f:
            append_f = f
            self.assertEqual(0, f.tell())
            self.assertEqual(True, f.writable())
            self.assertEqual('ab', f.mode)
            self.assertEqual(f'oss://{self.bucket_name}/{key}', f.name)
            self.assertEqual(False, f.closed)

            n = f.write(data1.encode())
            self.assertEqual(len(data1), n)
            self.assertEqual(len(data1), f.tell())

            n = f.write(data2.encode())
            self.assertEqual(len(data2), n)
            self.assertEqual(len(data1) + len(data2), f.tell())

            n = f.write(data3.encode())
            self.assertEqual(len(data3), n)
            self.assertEqual(len(data1) + len(data2) + len(data3), f.tell())

        self.assertIsNotNone(append_f)
        self.assertIsInstance(append_f, oss.AppendOnlyFile)
        self.assertEqual(True, append_f.closed)
        # can close many times
        append_f.close()
        append_f.close()

        result = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertEqual(len(mix_data), result.content_length)
        self.assertEqual('Appendable', result.object_type)
        self.assertEqual(mix_data.encode(), result.body.content)

        # open exist
        append_f: oss.AppendOnlyFile = None
        with self.client.append_file(self.bucket_name, key) as f:
            self.assertEqual(len(mix_data), f.tell())
            f.write(b'123')
            append_f = f
            self.assertEqual(False, append_f.closed)
            f.flush()

        self.assertIsNotNone(append_f)
        self.assertEqual(True, append_f.closed)
        result = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertEqual(len(mix_data) + len('123'), result.content_length)
        self.assertEqual('Appendable', result.object_type)
        self.assertEqual((mix_data + '123').encode(), result.body.content)

        # flush
        key = 'append_file-flush-' + random_str(6)
        self.assertEqual(False, self.client.is_object_exist(self.bucket_name, key))
        append_f: oss.AppendOnlyFile = None
        with self.client.append_file(self.bucket_name, key) as f:
            append_f = f
            self.assertEqual(0, f.tell())
            self.assertEqual(False, append_f.closed)
            f.flush()
            self.assertIsNotNone(f._hash_crc64)
        self.assertEqual(True, self.client.is_object_exist(self.bucket_name, key))
        result = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertEqual('Appendable', result.object_type)
        self.assertEqual(0, result.content_length)

        # open-close
        key = 'append_file-open-close-' + random_str(6)
        self.assertEqual(False, self.client.is_object_exist(self.bucket_name, key))
        append_f = self.client.append_file(self.bucket_name, key)
        self.assertIsNotNone(append_f)
        self.assertEqual(False, append_f.closed)
        self.assertEqual(0, append_f.tell())
        append_f.close()
        self.assertEqual(True, append_f.closed)
        self.assertEqual(False, self.client.is_object_exist(self.bucket_name, key))


    def test_append_file_fail(self):
        # open normal file
        key = 'normal_file-' + random_str(6)
        data = "helle world"
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)
        self.assertEqual(True, self.client.is_object_exist(self.bucket_name, key))

        try: 
            self.client.append_file(self.bucket_name, key)
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('Not a appendable file', str(err))

        # access closed file
        append_f: oss.AppendOnlyFile = None
        key = 'new-append_file-' + random_str(6)
        self.assertFalse(self.client.is_object_exist(self.bucket_name, key))
        with self.client.append_file(self.bucket_name, key) as f:
            self.assertEqual(0, f.tell())
            f.write(b'123')
            append_f = f
            self.assertEqual(False, append_f.closed)

        self.assertTrue(self.client.is_object_exist(self.bucket_name, key))
        self.assertIsNotNone(append_f)

        # flush
        try: 
            append_f.flush()
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('I/O operation on closed file.', str(err))

        # tell
        try: 
            append_f.tell()
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('I/O operation on closed file.', str(err))

        # writable
        try: 
            append_f.writable()
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('I/O operation on closed file.', str(err))

        # write
        try: 
            append_f.write(b'123')
            self.fail('shoud not here')
        except Exception as err:
            self.assertIn('I/O operation on closed file.', str(err))

        # write non bytes data
        append_f: oss.AppendOnlyFile = None
        key = 'new-append_file-' + random_str(6)
        self.assertFalse(self.client.is_object_exist(self.bucket_name, key))
        with self.client.append_file(self.bucket_name, key) as f:
            self.assertEqual(0, f.tell())
            try: 
                f.write('123')
                self.fail('shoud not here')
            except Exception as err:
                self.assertIn('Not a bytes type, got ', str(err))

    def test_append_file_write_from(self):
        key = 'append_file-write_from' + random_str(6)
        data1 = random_str(12345)
        data2 = random_str(23456)
        data3 = random_str(34567)
        data4 = random_str(200*1024 + 45678)
        data5 = random_str(1111)
        all_data = data1 + data2 + data3 + data4 + data5

        str_data = data1
        bytes_data = data2.encode()
        bytesio_data = io.BytesIO(data3.encode())
        stringio_data = io.StringIO(data4)

        self.assertFalse(self.client.is_object_exist(self.bucket_name, key))

        with self.client.append_file(self.bucket_name, key) as f:
            n = f.write_from(str_data)
            self.assertEqual(len(data1), n)

            n = f.write_from(bytes_data)
            self.assertEqual(len(data2), n)

            n = f.write_from(bytesio_data)
            self.assertEqual(len(data3), n)

            n = f.write_from(stringio_data)
            self.assertEqual(len(data4), n)

            n = f.write(data5.encode())
            self.assertEqual(len(data5), n)

        result = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertEqual(len(all_data), result.content_length)
        self.assertEqual('Appendable', result.object_type)
        self.assertEqual(all_data.encode(), result.body.content)
         

    def test_append_file_write_from_file(self):
        key = 'append_file-write_from_file' + random_str(6)
        filepath = "./tests/data/example.jpg"

        example_data = b''
        with open(filepath, 'rb') as f:
            example_data = f.read()

        with open(filepath, 'rb') as f:
            with self.client.append_file(self.bucket_name, key) as ff:
                n = ff.write_from(f)
                self.assertEqual(len(example_data), n)

        result = self.client.get_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertEqual(len(example_data), result.content_length)
        self.assertEqual('Appendable', result.object_type)
        self.assertEqual(example_data, result.body.content)


    def test_append_file_with_metadata(self):
        key = 'append_file-with_metadata' + random_str(6)
        data = b'hello world'
        data1 = b'hello oss'
        data2 = b'just for test'
        with self.client.append_file(self.bucket_name, key, create_parameter=oss.AppendObjectRequest(
            acl='public-read',
            storage_class='IA',
            content_type='plain/txt',
            metadata={'user':"test"}
        )) as f:
            n = f.write(data)
            self.assertEqual(len(data), n)

            n = f.write(data1)
            self.assertEqual(len(data1), n)

        result = self.client.head_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertEqual(len(data + data1), result.content_length)
        self.assertEqual('Appendable', result.object_type)
        self.assertEqual('IA', result.storage_class)
        self.assertEqual('test', result.metadata.get('user'))
        self.assertEqual('plain/txt', result.content_type)

        with self.client.append_file(self.bucket_name, key, create_parameter=oss.AppendObjectRequest(
            acl='public-read',
            storage_class='IA',
            content_type='plain/js',
            metadata={'user':"test"}
        )) as f:
            n = f.write(data2)
            self.assertEqual(len(data2), n)

        result = self.client.head_object(oss.GetObjectRequest(
            bucket=self.bucket_name,
            key=key
        ))
        self.assertEqual(len(data + data1 + data2), result.content_length)
        self.assertEqual('Appendable', result.object_type)
        self.assertEqual('IA', result.storage_class)
        self.assertEqual('test', result.metadata.get('user'))
        self.assertEqual('plain/txt', result.content_type)



class TestReadOnlyFile(TestIntegration):
    def test_open_file_baisc(self):
        data_size = 1234
        key = 'check_member-' + random_str(6)
        data = random_str(data_size).encode()
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        rf: oss.ReadOnlyFile = None
        with self.client.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            rf = f
            self.assertEqual(0, f.tell())
            self.assertEqual(True, f.seekable())
            self.assertEqual(True, f.readable())
            self.assertEqual(False, f.closed)
            self.assertEqual(f'oss://{self.bucket_name}/{key}', f.name)
            self.assertEqual('rb', f.mode)

            #seek, tell
            f.seek(0, os.SEEK_SET)
            self.assertEqual(0, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(1, os.SEEK_SET)
            self.assertEqual(1, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(data_size, os.SEEK_SET)
            self.assertEqual(data_size, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(-data_size, os.SEEK_END)
            self.assertEqual(0, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(-1, os.SEEK_END)
            self.assertEqual(data_size - 1, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[data_size -1:], b)

            f.seek(0, os.SEEK_END)
            self.assertEqual(data_size, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(b'', b)
            
            f.seek(123, os.SEEK_SET)
            self.assertEqual(123, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

            f.seek(123, os.SEEK_CUR)
            self.assertEqual(248, f.tell())
            offset = f.tell()
            b = f.read(2)
            self.assertEqual(data[offset:offset + 2], b)

        self.assertEqual(True, rf.closed)
        self.assertEqual(None, rf._read_buf)
        self.assertEqual(None, rf._stream_reader)
        self.assertEqual(None, rf._stream_iter)

        #call close many times
        rf.close()
        rf.close()

        rf = self.client.open_file(self.bucket_name, key)
        self.assertIsNotNone(rf)
        self.assertEqual(False, rf.closed)
        with rf as f:
            self.assertEqual(False, f.closed)
        self.assertEqual(True, rf.closed)


    def test_open_file_read_size(self):
        key = 'read_size-' + random_str(6)
        data = random_str(100*1024*5 + 1234).encode()

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # read with size
        rf: oss.ReadOnlyFile = None
        with self.client.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            rf = f
            end = 129
            for i in range(0, end):
                size = 200*1024 + 12345 - i
                f.seek(i, 0)
                self.assertEqual(i, f.tell())
                got = f.read(size)
                self.assertEqual(size, len(got))
                self.assertEqual(data[i:i+size], got)
                self.assertEqual(i + size, f.tell())

        self.assertEqual(True, rf.closed)

    def test_open_file_readall(self):
        key = 'readall-' + random_str(6)
        data = random_str(100*1024*5 + 1234).encode()

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # read all
        with self.client.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            f.seek(123)
            self.assertEqual(123, f.tell())
            got = f.readall()
            self.assertEqual(data[123:], got)
            self.assertEqual(len(data), f.tell())

            f.seek(1234)
            got1 = f.read(17)
            self.assertEqual(1234 + 17, f.tell())
            self.assertEqual(data[1234:1234 + 17], got1)
            got2 = f.read()
            self.assertEqual(len(data), f.tell())
            self.assertEqual(data[1234 + 17:], got2)
            self.assertEqual(data[1234:], got1 + got2)

            f.seek(12345)
            got1 = f.read(172)
            self.assertEqual(12345 + 172, f.tell())
            self.assertEqual(data[12345:12345 + 172], got1)
            got2 = f.readall()
            self.assertEqual(len(data), f.tell())
            self.assertEqual(data[12345 + 172:], got2)
            self.assertEqual(data[12345:], got1 + got2)

    def test_open_file_readinto(self):
        key = 'readinto-' + random_str(6)
        data = random_str(100*1024*5 + 1234).encode()

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # read into bytearray
        with self.client.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            b = bytearray(11)
            self.assertEqual(0, f.tell())
            n = f.readinto(b)
            self.assertEqual(11, n)
            self.assertEqual(data[0:11], b)
            self.assertEqual(11, f.tell())
            
            b = bytearray(9)
            n = f.readinto(b)
            self.assertEqual(9, n)
            self.assertEqual(data[11:20], b)
            self.assertEqual(20, f.tell())

            b = bytearray(len(data))
            f.seek(12345)
            n = f.readinto(b)
            self.assertEqual(len(data) - 12345, n)
            self.assertEqual(len(data), f.tell())

            b = bytearray(len(data) * 2)
            f.seek(1234)
            n = f.readinto(b)
            self.assertEqual(len(data) - 1234, n)
            self.assertEqual(len(data), f.tell())
            self.assertEqual(data[1234:], b[:len(data)-1234])

        # read into blob = memoryview(bytearray(size))
        with self.client.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            blob = memoryview(bytearray(len(data)))
            self.assertEqual(0, f.tell())
            n = f.readinto(blob[0:11])
            self.assertEqual(11, n)
            self.assertEqual(data[0:11], blob[0:11])
            self.assertEqual(11, f.tell())

            n = f.readinto(blob[11:20])
            self.assertEqual(9, n)
            self.assertEqual(data[11:20], blob[11:20])
            self.assertEqual(20, f.tell())

            #remains
            n = f.readinto(blob)
            self.assertEqual(len(data) - 20, n)
            self.assertEqual(data[20:], blob[0:n])
            self.assertEqual(len(data), f.tell())

    def test_open_file_fail(self):
        key = 'fail-test-' + random_str(6)
        nokey = key + 'no-key'
        data = random_str(1234).encode()

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        # open fail
        try:
            with self.client.open_file(self.bucket_name, nokey) as f:
                self.assertIsNotNone(f)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('stat_object', str(err))
            self.assertIn(f'oss://{self.bucket_name}/{nokey}', str(err))

        # seek fail
        try:
            with self.client.open_file(self.bucket_name, key) as f:
                f.seek(len(data) + 1, os.SEEK_SET)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('offset is unavailable', str(err))

        try:
            with self.client.open_file(self.bucket_name, key) as f:
                f.seek(-1, os.SEEK_SET)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('negative seek position', str(err))

        try:
            with self.client.open_file(self.bucket_name, key) as f:
                f.seek(0, 3)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('unsupported whence value', str(err))

        try:
            with self.client.open_file(self.bucket_name, key) as f:
                f.seek('123', 3)
            self.fail('should not here')
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('is not an integer', str(err))

        # call after close
        rf: oss.ReadOnlyFile = None
        with self.client.open_file(self.bucket_name, key) as f:
            self.assertIsNotNone(f)
            rf = f

        try:
            rf.read()
        except oss.PathError as err:
            self.assertIn('read', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.readall()
        except oss.PathError as err:
            self.assertIn('read', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.readinto(bytearray(123))
        except oss.PathError as err:
            self.assertIn('read', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.seek(0, os.SEEK_CUR)
        except oss.PathError as err:
            self.assertIn('seek', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.tell()
        except oss.PathError as err:
            self.assertIn('tell', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.readable()
        except oss.PathError as err:
            self.assertIn('readable', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

        try:
            rf.seekable()
        except oss.PathError as err:
            self.assertIn('seekable', str(err))
            self.assertIn('I/O operation on closed file.', str(err))


        try:
            with rf as f:
                pass
        except oss.PathError as err:
            self.assertIn('enter', str(err))
            self.assertIn('I/O operation on closed file.', str(err))

    def test_open_file_resume_read(self):
        key = 'resume_read-' + random_str(6)
        data = random_str(200*1024 + 1234).encode()

        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        with self.client.open_file(self.bucket_name, key) as f:
            b1 = f.read(1234)
            # wait stream close
            f._stream_iter = None
            #time.sleep(120)
            b2 = f.read()
            self.assertEqual(data, b1 + b2)

    def test_open_file_source_changed(self):
        key = 'source_changed-' + random_str(6)
        data1 = random_str(200*1024 + 1234).encode()
        data2 = random_str(201*1024 + 1234).encode()
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data1
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        with self.client.open_file(self.bucket_name, key) as f:
            b1 = f.read(1234)
            self.assertEqual(data1[0:len(b1)], b1)

            #change file
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=data2
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)

            try:
                f.seek(0)
                f.readall()
            except oss.PathError as err:
                self.assertIn('get_object', str(err))
                self.assertIn('Source file is changed, origin info', str(err))

    def test_open_file_prefetch_read(self):
        key = 'prefetch-' + random_str(6)
        data_len = 11*200*1024 + 1234
        data = random_str(data_len).encode()
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        rf: oss.ReadOnlyFile = None    
        with self.client.open_file(
            self.bucket_name, key, 
            enable_prefetch=True,
            prefetch_num=3, 
            chunk_size=2*200*1024, 
            prefetch_threshold = 0) as f:

            rf = f
            self.assertEqual(True, f._enable_prefetch)
            self.assertEqual(3, f._prefetch_num)
            self.assertEqual(2*200*1024, f._chunk_size)
            self.assertEqual(0, f._prefetch_threshold)

            # size
            start = f.seek(0, os.SEEK_SET)
            end = f.seek(0, os.SEEK_END)
            self.assertEqual(data_len, end - start)

            #print('\nreadall')
            # readall
            f.seek(0, os.SEEK_SET)
            b = f.readall()
            self.assertEqual(data, b)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)
            self.assertEqual(3, f._executor._max_workers)

            b = f.readall()
            self.assertEqual(b'', b)

            #print('seek readN')
            # seek readN
            for _ in range(0, 64):
                offset = random.randint(0, data_len // 5)
                n = random.randint(0, data_len // 4) + 3*200*1024
                begin = f.seek(offset, os.SEEK_SET)
                f._num_ooo_read = 0
                self.assertEqual(offset, begin)
                #print(f'seek readN {offset} {n}')
                b = f.read(n)
                self.assertEqual(n, len(b))
                self.assertEqual(data[offset:offset + n], b)
                if n % f._chunk_size > 0:
                    self.assertGreater(len(f._prefetch_readers), 1)
                self.assertIsNone(f._stream_reader)
                self.assertIsNone(f._stream_iter)
                self.assertIsNotNone(f._generator)

            #print('seek read from offset to end')
            # seek read from offset to end
            for _ in range(0, 64):
                offset = random.randint(0, data_len // 5)
                begin = f.seek(offset, os.SEEK_SET)
                f._num_ooo_read = 0
                self.assertEqual(offset, begin)
                b = f.read()
                self.assertEqual(data_len - offset, len(b))
                self.assertEqual(data[offset:], b)
                self.assertEqual(0, len(f._prefetch_readers))
                self.assertIsNone(f._stream_reader)
                self.assertIsNone(f._stream_iter)
                self.assertIsNotNone(f._generator)

            #print('seek readInto N')
            # seek readInto N
            for _ in range(0, 64):
                offset = random.randint(0, data_len // 5)
                n = random.randint(0, data_len // 4) + 3*200*1024
                begin = f.seek(offset, os.SEEK_SET)
                f._num_ooo_read = 0
                self.assertEqual(offset, begin)
                blob = memoryview(bytearray(n))
                got = f.readinto(blob)
                self.assertEqual(n, got)
                self.assertEqual(data[offset:offset + n], blob[0:])
                if n % f._chunk_size > 0:
                    self.assertGreater(len(f._prefetch_readers), 1)
                self.assertIsNotNone(f._generator)
                self.assertIsNone(f._stream_reader)
                self.assertIsNone(f._stream_iter)

            #print('seek readInto from offset to end')
            # seek readInto from offset to end
            bloball = memoryview(bytearray(data_len))
            for _ in range(0, 64):
                offset = random.randint(0, data_len // 5)
                begin = f.seek(offset, os.SEEK_SET)
                f._num_ooo_read = 0
                self.assertEqual(offset, begin)
                got = f.readinto(bloball)
                self.assertEqual(data_len - offset, got)
                self.assertEqual(data[offset:], bloball[0:got])
                self.assertEqual(0, len(f._prefetch_readers))
                self.assertIsNone(f._stream_reader)
                self.assertIsNone(f._stream_iter)
                self.assertIsNotNone(f._generator)
        
        self.assertEqual(None, rf._read_buf)
        self.assertEqual(None, rf._stream_reader)
        self.assertEqual(None, rf._prefetch_readers)
        self.assertEqual(None, rf._generator)
        self.assertEqual(None, rf._executor)

        #call close many times
        rf.close()
        rf.close()

    def test_open_file_mix_read(self):
        key = 'mix-' + random_str(6)
        data_len = 11*200*1024 + 12345
        data = random_str(data_len).encode()
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        rf: oss.ReadOnlyFile = None
        with self.client.open_file(
            self.bucket_name, key, 
            enable_prefetch=True,
            prefetch_num=3, 
            chunk_size=1*200*1024, 
            prefetch_threshold = 5*200*1024) as f:

            rf = f
            self.assertEqual(True, f._enable_prefetch)
            self.assertEqual(3, f._prefetch_num)
            self.assertEqual(1*200*1024, f._chunk_size)
            self.assertEqual(5*200*1024, f._prefetch_threshold)
            
            # read some
            some1 = 3 * 100 * 1024 + 123
            f.seek(0, os.SEEK_SET)
            b1 = f.read(some1)
            self.assertEqual(data[0:some1], b1)
            self.assertIsNotNone(f._stream_reader)
            self.assertIsNotNone(f._stream_iter)
            self.assertIsNone(f._generator)
            self.assertIsNone(f._executor)

            # read some
            some2 = 8 * 100 * 1024 + 123
            self.assertGreater(some1 + some2, f._prefetch_threshold)
            b2 = f.read(some2)
            self.assertEqual(data[some1:some1 + some2], b2)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)
            self.assertEqual(3, f._executor._max_workers)

            # read last
            b3 = f.readall()
            self.assertEqual(data, b1 + b2 + b3)

        self.assertEqual(None, rf._read_buf)
        self.assertEqual(None, rf._stream_reader)
        self.assertEqual(None, rf._prefetch_readers)
        self.assertEqual(None, rf._generator)
        self.assertEqual(None, rf._executor)

        # seq read, seek, read all 
        with self.client.open_file(
            self.bucket_name, key, 
            enable_prefetch=True,
            prefetch_num=3, 
            chunk_size=1*200*1024, 
            prefetch_threshold = 5*200*1024) as f:

            self.assertEqual(True, f._enable_prefetch)
            self.assertEqual(3, f._prefetch_num)
            self.assertEqual(1*200*1024, f._chunk_size)
            self.assertEqual(5*200*1024, f._prefetch_threshold)
            
            # read some
            off1 = 1
            some1 = 3 * 100 * 1024 + 123
            f.seek(off1, os.SEEK_SET)
            b1 = f.read(some1)
            self.assertEqual(data[off1:off1 + some1], b1)
            self.assertIsNotNone(f._stream_reader)
            self.assertIsNotNone(f._stream_iter)
            self.assertIsNone(f._generator)
            self.assertIsNone(f._executor)

            # read some
            off2 = 100
            some2 =  15 * 100 * 1024 + 123
            self.assertGreater(some2, f._prefetch_threshold)
            f.seek(off2, os.SEEK_SET)
            b2 = f.read(some2)
            self.assertEqual(data[off2:off2 + some2], b2)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)
            self.assertEqual(3, f._executor._max_workers)

    def test_open_file_prefetch_source_changed(self):
        key = 'prefetch_source_changed-' + random_str(6)
        data1 = random_str(11*200*1024 + 12345).encode()
        data2 = random_str(11*200*1024 + 12345).encode()
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data1
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        with self.client.open_file(
            self.bucket_name, key, 
            enable_prefetch=True,
            prefetch_num=3, 
            chunk_size=2*200*1024, 
            prefetch_threshold = 0) as f:

            len1 = 3 * 200 * 1024 + 12
            b1 = f.read(len1)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)
            self.assertEqual(data1[0:len1], b1)

            #change file
            result = self.client.put_object(oss.PutObjectRequest(
                bucket=self.bucket_name,
                key=key,
                body=data2
            ))
            self.assertEqual(200, result.status_code)
            self.assertEqual('OK', result.status)

            # read data saved in the buffer
            len2 = 1 * 200 * 1024
            b2 = f.read(len2)
            self.assertEqual(data1[len1:len1 + len2], b2)

            # read remains
            try:
                f.readall()
            except oss.PathError as err:
                self.assertIn('get_object', str(err))
                self.assertIn('Source file is changed, origin info', str(err))

    def test_open_file_mix_read2(self):
        key = 'prefetch-' + random_str(6)
        data_len = 6*100*1024 + 1234
        data = random_str(data_len).encode()
        result = self.client.put_object(oss.PutObjectRequest(
            bucket=self.bucket_name,
            key=key,
            body=data
        ))
        self.assertEqual(200, result.status_code)
        self.assertEqual('OK', result.status)

        with self.client.open_file(
            self.bucket_name, key, 
            enable_prefetch=True,
            prefetch_num=2, 
            chunk_size=1*200*1024, 
            prefetch_threshold = 1*200*1024) as f:

            self.assertEqual(True, f._enable_prefetch)
            self.assertEqual(2, f._prefetch_num)
            self.assertEqual(1*200*1024, f._chunk_size)
            self.assertEqual(1*200*1024, f._prefetch_threshold)

            len1 = 12345
            b1 = f.read(len1)
            self.assertEqual(data[0:len1], b1)
            self.assertIsNotNone(f._stream_reader)
            self.assertIsNotNone(f._stream_iter)
            self.assertIsNone(f._generator)
            self.assertIsNone(f._executor)

            len2 = 1*200*1024
            b2 = f.read(len2)
            self.assertEqual(data[len1:len1 + len2], b2)
            self.assertIsNone(f._stream_reader)
            self.assertIsNone(f._stream_iter)
            self.assertIsNotNone(f._generator)
            self.assertIsNotNone(f._executor)

            # set reader fail
            f._prefetch_readers[0]._failed = True
            len3 = 1*100*1024
            b3 = f.read(len3)
            self.assertEqual(data[:len1 + len2 + len3], b1 + b2 + b3)
            self.assertIsNotNone(f._stream_reader)
            self.assertIsNotNone(f._stream_iter)
            self.assertIsNone(f._generator)
            self.assertIsNotNone(f._executor)
