To programmatically create an AWS session using Okta and AWS Federation (SAML-based authentication), you can use the following approach:

1. **Prerequisites:**
   - Access to Okta.
   - Configured Okta AWS App for SAML-based authentication.
   - An API token for Okta.
   - Python installed with required libraries (`boto3`, `requests`, and `xmltodict`).

2. **Steps Overview:**
   - Authenticate with Okta to get a SAML response.
   - Parse the SAML response for AWS roles.
   - Assume an AWS role using the SAML response.
   - Use the temporary AWS credentials for AWS operations.

3. **Python Script Example:**

```python
import boto3
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

def authenticate_with_okta(okta_domain, okta_username, okta_password, aws_app_url):
    # URL for Okta authentication
    auth_url = urljoin(okta_domain, '/api/v1/authn')

    # Authenticate with Okta
    response = requests.post(auth_url, json={
        'username': okta_username,
        'password': okta_password
    })
    response.raise_for_status()
    auth_data = response.json()

    # Get session token
    session_token = auth_data.get('sessionToken')
    if not session_token:
        raise Exception("Failed to retrieve session token from Okta.")

    # Get SAML Response from AWS App
    saml_response = requests.post(aws_app_url, params={
        'sessionToken': session_token
    }, allow_redirects=True).text

    return saml_response

def parse_saml_response(saml_response):
    # Parse the SAML Response XML
    root = ET.fromstring(saml_response)
    aws_roles = []
    for attr in root.findall('.//{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
        if attr.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role':
            for value in attr.findall('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                aws_roles.append(value.text)

    return aws_roles

def assume_role_with_saml(aws_roles, saml_response, region='us-east-1'):
    # Select the role to assume (if multiple roles are available)
    role_arn, principal_arn = aws_roles[0].split(',')

    # Use boto3 STS to assume the role
    sts_client = boto3.client('sts', region_name=region)
    assumed_role = sts_client.assume_role_with_saml(
        RoleArn=role_arn,
        PrincipalArn=principal_arn,
        SAMLAssertion=saml_response
    )

    # Extract temporary credentials
    credentials = assumed_role['Credentials']
    return {
        'AccessKeyId': credentials['AccessKeyId'],
        'SecretAccessKey': credentials['SecretAccessKey'],
        'SessionToken': credentials['SessionToken']
    }

def main():
    okta_domain = "https://<your_okta_domain>"
    okta_username = "<your_username>"
    okta_password = "<your_password>"
    aws_app_url = "https://<your_okta_domain>/app/<aws_app_id>/sso/saml"

    saml_response = authenticate_with_okta(okta_domain, okta_username, okta_password, aws_app_url)
    aws_roles = parse_saml_response(saml_response)
    credentials = assume_role_with_saml(aws_roles, saml_response)

    print("Temporary AWS Credentials:")
    print(f"Access Key: {credentials['AccessKeyId']}")
    print(f"Secret Key: {credentials['SecretAccessKey']}")
    print(f"Session Token: {credentials['SessionToken']}")

if __name__ == '__main__':
    main()
```

4. **How it Works:**
   - The `authenticate_with_okta` function authenticates with Okta and retrieves a SAML response.
   - The `parse_saml_response` function extracts AWS roles from the SAML response.
   - The `assume_role_with_saml` function uses the AWS STS service to assume the desired role and fetch temporary credentials.
   - The credentials can be used with the AWS SDK (boto3) to perform operations.

5. **Setup:**
   - Replace `<your_okta_domain>`, `<your_username>`, `<your_password>`, and `<aws_app_id>` with your Okta and AWS application details.
   - Install required dependencies using:
     ```bash
     pip install boto3 requests xmltodict
     ```

Let me know if you need further assistance!
