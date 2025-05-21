# Piglet example

Example how to implement a Python console application in Plain.

## Prerequisites

You need ***plain2code*** renderer set up. Please see [plain2code_client](https://github.com/Codeplain-ai/plain2code_client) repository for details how to set it up.

You need to set `PLAIN2CODE_RENDERER_DIR` environmental variable to the directory containing the plain2code.py script.

## Usage

To have the Piglet example application rendered to executable software code run

`sh render.sh -v`

The resulting software code will be stored to `build` folder (the folders `build.#` contain intermediary generated code). To run it execute

```
python build/piglet.py test.txt
```
