# Cisco HyperFlex API Token Manager

Cisco HyperFlex API Token Manager provides the ability to automate the creation, validation and renewal of HyperFlex API tokens. Basic management of HyperFlex API tokens, including obtain, refresh, validate and revoke actions are also available.

## Prerequisites:
1. Python 3 installed, which can be downloaded from [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Clone or download the Cisco HyperFlex API Token Manager repository by using the ![GitHub Clone or download](./assets/GitHub_Clone_or_download_link_button.png "GitHub Clone or download") link on the main repository web page or by running the following command:
    ```
    git clone https://github.com/ugo-emekauwa/hx-api-token-manager
    ```
3. Install the required Python modules **requests** and **urllib3**. The requirements.txt file in the repository can be used by running the following command:
    ```
    python -m pip install -r requirements.txt
    ```
4. The IP address of the targeted Cisco HyperFlex system.
5. User credentials with administrative rights on the targeted Cisco HyperFlex system.

After fulfilling the requirements listed in the [**Prerequisites**](https://github.com/ugo-emekauwa/hx-api-token-manager#prerequisites) section, **hx_api_token_manager.py** can be ran directly from your IDE or imported into another module.

## How to Use:

### Basic Functions
The Cisco HyperFlex API Token Manager module contains seven functions for managing HyperFlex API tokens. Here are four core basic functions that provide the ability to obtain, refresh, validate and revoke API tokens.


- ### Obtain Access Tokens - `obtain_token(ip,username,password)`
  This is a function that obtains a HyperFlex API access token.
  - **The Available Function Arguments**
    - **ip**: The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **username**: The username credentials that will be used to log into HyperFlex. The value must be a string.
    - **password**: The passsword credentials that will be used to log into HyperFlex. The value must be a string.
      
  - **What the Function Returns**
  
    A HyperFlex API access token, refresh token and token type that have been granted as key-value pairs in a dictionary.


- ### Refresh Access Tokens - `refresh_token(ip,hx_api_token)`
  This is a function that refreshes a HyperFlex API access token.
  - **The Available Function Arguments**
    - **ip**: The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **hx_api_token**: A dictionary value for a granted HyperFlex AAA token containing the following keys:
      - **"access_token"**: An access token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize API operations by properly authenticated users.
      - **"refresh_token"**: A refresh token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize users for any API operations. The refresh token can be used to obtain a new access token without the need to re-provide HyperFlex username and password credentials.
      - **"token_type"**: A token type obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize users for any API operations. This token type value should be of type "Bearer".

  - **What the Function Returns**
  
    A HyperFlex API access token, refresh token and token type that have been granted as key-value pairs in a dictionary.


- ### Validate Access Tokens - `validate_token(ip,hx_api_token,scope="READ")`
  This is a function that validates a HyperFlex API access token.
  - **The Available Function Arguments**
    - **ip**: The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **hx_api_token**: A dictionary value for a granted HyperFlex AAA token containing the following keys:
      - **"access_token"**: An access token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize API operations by properly authenticated users.
      - **"refresh_token"**: A refresh token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize users for any API operations. The refresh token can be used to obtain a new access token without the need to re-provide HyperFlex username and password credentials.
      - **"token_type"**: A token type obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize users for any API operations. This token type value should be of type "Bearer".
    - **scope**: The scope of the validate access token operation. The value must be a string. The options are "READ" or "MODIFY". The default value is "READ".

  - **What the Function Returns**
  
    The boolean value "True" is returned for a successful validation. The boolean value "False" is returned if the validation fails.


- ### Revoke Tokens - `revoke_token(ip,hx_api_token)`
  This is a function that revokes a HyperFlex API access token.
  - **The Available Function Arguments**
    - **ip**: The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **hx_api_token**: A dictionary value for a granted HyperFlex AAA token containing the following keys:
      - **"access_token"**: An access token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize API operations by properly authenticated users.
      - **"refresh_token"**: A refresh token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize users for any API operations. The refresh token can be used to obtain a new access token without the need to re-provide HyperFlex username and password credentials.
      - **"token_type"**: A token type obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize users for any API operations. This token type value should be of type "Bearer".
  
  - **What the Function Returns**  
    
    The boolean value True is returned for a successful revocation. The boolean value False is returned if the revocation fails.




### Advanced Functions
The Cisco HyperFlex API Token Manager module contains three additional functions that provide the ability to automate the creation, validation and renewal of access tokens. Offline token use is also provided among other features.

- ### Automated Management of Token Files


- ### Creation of Token Files


- ### Loading Token Files


## Related Tools:
Here are similar tools to help manage Cisco HyperFlex training, demonstration and development environments.
- [Cisco HyperFlex Datastore Safeguard](https://github.com/ugo-emekauwa/hx-datastore-safeguard)
- [Cisco HyperFlex Datastore Cleanup](https://github.com/ugo-emekauwa/hx-datastore-cleanup)
- [HyperFlex Notification Tool for Cisco Intersight](https://github.com/ugo-emekauwa/hyperflex-notification-tool)

## Author:
Ugo Emekauwa

## Contact Information:
uemekauw@cisco.com or uemekauwa@gmail.com
