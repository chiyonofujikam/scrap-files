# scrap-files

## Setting Up the Virtual Environment and Running the Application

1- Ensure you're in the `./tz-project` directory, then run the following commands:

```bash
py -m pip cache purge
py -m venv .\.venv
.\.venv\Scripts\activate
.\.venv\Scripts\python.exe -m pip cache purge
.\.venv\Scripts\python.exe -m pip install --upgrade pip wheel build setuptools
.\.venv\Scripts\python.exe -m pip --no-cache-dir install --use-pep517 -e .
```

2- Cleaning "__pycache__" from the project:

```powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```

or

```bash
for /d /r %i in (__pycache__) do rmdir /s /q "%i"
```

3- Launching the Application, execute:

```bash
scraping
```

4- Managing Dependencies: When a new package is required, simply add it to the install_requires section in the setup.cfg file, specifying the desired version.
