# tintin-sdk
SDK library for project tintin


#### Installation

```
pip install tintin-sdk
```

#### Example

##### Download files to `/tmp` from Assets `/testdata/1.jpg`

```python


from tintin.file.minio import FileManager as minioFileManager

debug = False
mgr = FileManager('', debug)

// download individual assets from /testdata/1.jpg to /tmp/testdata/1.jpg folder
mgr.download('/tmp',['/testdata/1.jpg'])

// download the entire objects with prefix /testdata into /tmp folder
mgr.download('/tmp',['/testdata'])
```

see more on testcase.
