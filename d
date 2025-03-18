[1mdiff --git a/.vscode/settings.json b/.vscode/settings.json[m
[1mdeleted file mode 100644[m
[1mindex 8bc1ad0..0000000[m
[1m--- a/.vscode/settings.json[m
[1m+++ /dev/null[m
[36m@@ -1,32 +0,0 @@[m
[31m-{[m
[31m-  "editor.rulers": [100],[m
[31m-  "[python]": {[m
[31m-    "editor.defaultFormatter": "ms-python.black-formatter",[m
[31m-    "editor.codeActionsOnSave": {[m
[31m-      "source.organizeImports": "always",[m
[31m-      "source.fixAll": "explicit"[m
[31m-    }[m
[31m-  },[m
[31m-  "editor.formatOnSave": true,[m
[31m-  "files.insertFinalNewline": true,[m
[31m-  "black-formatter.args": ["--line-length=100"],[m
[31m-  "isort.args": [[m
[31m-    "--line-length=100",[m
[31m-    "--wrap-length=100",[m
[31m-    "--multi-line=3",[m
[31m-    "--trailing-comma",[m
[31m-    "--profile=black"[m
[31m-  ],[m
[31m-  "python.testing.pytestArgs": ["tests"],[m
[31m-  "python.testing.unittestEnabled": false,[m
[31m-  "python.testing.pytestEnabled": true,[m
[31m-  "pylint.importStrategy": "fromEnvironment",[m
[31m-  "pylint.args": ["--rcfile=.pylintrc"],[m
[31m-  "python.analysis.typeCheckingMode": "basic",[m
[31m-  "python.analysis.useLibraryCodeForTypes": true,[m
[31m-  "python.analysis.diagnosticSeverityOverrides": {[m
[31m-    "reportGeneralTypeIssues": "error",[m
[31m-    "reportTypeVarUsage": "error",[m
[31m-    "reportUnknownMemberType": "none"[m
[31m-  }[m
[31m-}[m
[1mdiff --git a/README.md b/README.md[m
[1mindex d40e9a2..776c50f 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -1,10 +1,26 @@[m
 # Online Commerce[m
 [m
[31m-## Install Poetry[m
[32m+[m[32m## Overview of Project[m
[32m+[m
[32m+[m[32m### Team Members[m
[32m+[m
[32m+[m[32mJin Yang Chen (development engineer)[m
[32m+[m
[32m+[m[32m### Description of Tests[m
[32m+[m
[32m+[m[32mUtilised the `pytest` framework for testing, focusing on unit testing the cart functionality, and database retrieval logic. Tests related to the business logic of `category`, `product` and `supplier` have also been included.[m
[32m+[m
[32m+[m[32m### Notable implementation details[m
[32m+[m
[32m+[m[32mClear segregation of concerns among `services`, `models` and `routes`. `routes` are purely responsible for rendering the HTML templates, offloading all business logic to the corresponding service in `services`. All data structures are centrally managed in the `models` module.[m
[32m+[m
[32m+[m[32m## Quick Start[m
[32m+[m
[32m+[m[32m### Install Poetry[m
 [m
 Please follow the official [installation guide](https://python-poetry.org/docs/#installation) to install Poetry.[m
 [m
[31m-## Install dependencies[m
[32m+[m[32m### Install dependencies[m
 [m
 It is recommended to use Python virtual environment, so you don't pollute your system Python environment.[m
 [m
[36m@@ -13,50 +29,52 @@[m [mIt is recommended to use Python virtual environment, so you don't pollute your s[m
 poetry install[m
 ```[m
 [m
[31m-## Mac/Linux[m
[32m+[m[32m### Mac/Linux[m
 [m
 ```bash[m
 # Activate Python virtual environment[m
 eval "$(poetry env activate)"[m
 ```[m
 [m
[31m-## Windows/Powershell[m
[32m+[m[32m### Windows/Powershell[m
 [m
 ```bash[m
 # Activate Python Virtual Environment[m
 & .venv\Scripts\Activate.ps1[m
 ```[m
 [m
[31m-## Add dependencies[m
[31m-[m
[31m-If you want to add a new dependency, please use `poetry add` command.[m
[31m-[m
[31m-For example, to add `python-dotenv` dependency, run:[m
[32m+[m[32m### Set up environment variables[m
 [m
 ```bash[m
[31m-poetry add python-dotenv[m
[32m+[m[32m# Create .env file (by copying from .env.example)[m
[32m+[m[32mcp .env.example .env[m
 ```[m
 [m
[31m-## Set up environment variables[m
[32m+[m[32m## Commands[m
 [m
 ```bash[m
[31m-# Create .env file (by copying from .env.example)[m
[31m-cp .env.example .env[m
[32m+[m[32m# Quick Start at root directory[m
[32m+[m[32mflask run[m
[32m+[m
[32m+[m[32m# To verify that the app is running, g