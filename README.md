# PiQA

Pitchdeck key information extractor using the latest LLMs and LangChain

# Setup

## Install Dependencies

To ensure this package can be run on any machine that supports Python, the following steps should be followed:

1. Create a virtual env. One way to do so is with; `python -m venv venv-piqa`
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

```md
# Name of the Product

SEOmoz

# Team

- Rand Fishkin: CEO & Co-founder
- Gillian Muessig: Co-founder

# Traction

- Over 30,000 customers in 100+ countries
- $18 million in funding
- Revenue growth of 100% YoY

# Problem

- Difficulty in understanding and implementing SEO strategies
- Lack of reliable SEO software

# Solution

- SEO software that provides actionable insights and recommendations
- Educational resources and community support

# Market

- Digital marketing industry
- Specifically, the SEO market

# Market Size

- $80 billion digital marketing industry
- $65 billion SEO market

# Product-Market Fit

- High customer retention rate
- Positive customer feedback and reviews

# Go-to-Market (GTM) Strategy

- Inbound marketing
- Content marketing
- Referral marketing

# Target Customers

- Small to medium-sized businesses
- Digital marketing agencies

# Competition

- SEMrush
- Ahrefs
- Majestic

# Business Model

- Subscription-based model
- Tiered pricing based on features and usage

# Revenue Model

- Monthly and annual subscriptions

## Concise Summary

SEOmoz is a leading SEO software company that provides actionable insights and recommendations to help businesses improve their search engine rankings. With over 30,000 customers in 100+ countries and $18 million in funding, SEOmoz has a strong market presence and revenue growth of 100% YoY. The company's GTM strategy includes inbound, content, and referral marketing, and its target customers are small to medium-sized businesses and digital marketing agencies. The company faces competition from SEMrush, Ahrefs, and Majestic, but has a high customer retention rate and positive customer feedback.

## Longer Summary

SEOmoz is a Seattle-based SEO software company that was founded in 2004 by Rand Fishkin and Gillian Muessig. The company's mission is to help businesses improve their search engine rankings by providing actionable insights and recommendations. SEOmoz has over 30,000 customers in 100+ countries and has raised $18 million in funding. The company's revenue has grown 100% YoY, and it has a high customer retention rate and positive customer feedback.

SEOmoz's GTM strategy includes inbound, content, and referral marketing. The company's target customers are small to medium-sized businesses and digital marketing agencies. SEOmoz faces competition from SEMrush, Ahrefs, and Majestic, but differentiates itself by providing educational resources and community support.

SEOmoz's business model is subscription-based, with tiered pricing based on features and usage. The company's revenue model includes monthly and annual subscriptions.

## How to Assess the Risks of Investing in SEOmoz

1. Market Risk: The digital marketing industry is highly competitive, and SEOmoz faces competition from established players like SEMrush, Ahrefs, and Majestic. Assess the company's ability to differentiate itself and capture market share.
2. Customer Acquisition Risk: SEOmoz's GTM strategy relies heavily on inbound, content, and referral marketing. Assess the effectiveness of these strategies and the company's ability to acquire new customers.
3. Revenue Risk: SEOmoz's revenue is based on subscriptions, which can be affected by customer churn and pricing pressure. Assess the company's ability to retain customers and maintain pricing power.
4. Technology Risk: SEOmoz's software relies on data and algorithms, which can be affected by changes in search engine algorithms and data availability. Assess the company's ability to adapt to these changes and maintain the accuracy and relevance of its software.
5. Team Risk: Assess the experience and track record of the management team, particularly Rand Fishkin and Gillian Muessig, who are the co-founders of the company.

## Recommendation

Based on the information provided, I would recommend investing in SEOmoz. The company has a strong market presence, revenue growth, and customer retention rate. Its GTM strategy is effective, and it has a differentiated product offering with educational resources and community support. While there are risks associated with investing in the digital marketing industry, I believe that SEOmoz has a strong team and is well-positioned to capture market share.
```

# Running tests

In the root folder run `python -m pytest tests -c pytest.ini`

# Roadmap

TBD.
