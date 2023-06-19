# PiQA

Pitchdeck key information extractor using the latest LLMs and LangChain

# Setup

## Install Dependencies

To ensure this package can be run on any machine that supports Python, the following steps should be followed:

1. Create a virtual env. One way to do so is with; `python venv venv-piqa`
2. Activate the virtual env; `active venv-piqa/bin/activate`
3. Install the required depencies; `pip install -r requirements.txt`
4. (Optional) If you'd also like to run the tests locally; `pip install -r requirements-test.txt`

Your environment is now setup to use the PiQa package.

## Setup credentials

Some credentials are required to interact with external services

### Adobe Credentials

Adobe's PDF Extract API is used to extract text from PDFs. To setup the credentials:

1. Go to https://developer.adobe.com/document-services/apis/pdf-extract/ and follow the steps to `Get Credentials`
2. Copy the `pdfservices-api-credentials.json` and `private.key` files to the `credentials` folder

### Other Credentials

Create a `.env` file in the root folder. See the `.env.example` for required environment variables. Please note that an OpenAI API key is required.

# Example code

See the `run_piqa_package.py` file to see an example of how to generate investor metrics from a PDF.

# Example output

For the `moz.pdf` file in the `data/documents` folder, the following output is generated:

# Running tests

In the root folder run `python -m pytest tests/`

# Roadmap

TBD.
