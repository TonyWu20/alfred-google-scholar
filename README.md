# alfred-google-scholar

## Features

1. Display the first page results of google scholar.
2. Connect with the [alfred-download-url-from-scihub-workflow](https://github.com/TonyWu20/alfred-download-url-from-scihub-workflow), so you can directly access to the paper you want.

## Requirements

- Python 3
- [requests-html](https://github.com/psf/requests-html.git)

  To install requests-html, run this in command line

        $ pip3 install requests-html

  Or

        $ pip install requests-html

## Installations

Download the workflow file and import to alfred.

## Setup

You might need to change the python3 executable path in the setting of Script
Filter of the alfred workflow according to your settings.

The current setting is "/usr/local/opt/python@3.8/bin/python3". You should run
"which python3" in terminal to check your python3 executable path.

## Usage

Enter "gsc" to trigger the workflow and enter the keywords. The first page of
google-scholar results will be shown. Press enter on the result will open it in
your browser.

Hold **shift** then press enter will copy the url to clipboard
Hold **control** then press enter will pass the url to
[alfred-download-url-from-scihub-workflow](https://github.com/TonyWu20/alfred-download-url-from-scihub-workflow)
to get access to it on scihub.
