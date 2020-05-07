# Cisco HyperFlex API Token Manager

Cisco HyperFlex API Token Manager provides the ability to automate the creation, validation and renewal of HyperFlex API tokens. Basic administration of HyperFlex API tokens is also available with easy to use Python functions that simplify obtaining, refreshing, revoking, and validating tokens.

The Cisco HyperFlex API Token Manager can be used as a solution to work with the HyperFlex AAA (Authentication, Authorization and Accounting) API rate limit introduced in HyperFlex 4.0(2a).

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

### _Basic Functions_
The Cisco HyperFlex API Token Manager module contains seven functions for managing HyperFlex API tokens. Here are four core basic functions that provide the ability to obtain, refresh, validate and revoke HyperFlex API tokens.


- ### Obtain Access Tokens
  ```py
  obtain_token(ip,username,password)
  ```
  The function **_obtain_token()_** obtains a new HyperFlex API access token. A HyperFlex API access token authorizes API operations on a HyperFlex cluster.
  - **The Available Function Arguments:**
    - **ip** - The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **username** - The username credentials that will be used to log into HyperFlex. The value must be a string.
    - **password** - The password credentials that will be used to log into HyperFlex. The value must be a string.
      
  - **What the Function Returns:**
  
    A HyperFlex API access token, refresh token and token type that have been granted as key-value pairs in a dictionary.
    
  - **Example Usage:**
  
    **(1).** First let's create variables to hold the values for the **_obtain_token()_** function arguments. Using variables is not required, but provides for easier readability and the variables can be re-used again at a later time if needed.
      ![Figure 1 - Argument Variables for obtain_token() Function](./assets/Figure_1-Argument_Variables_for_obtain_token_Function.png "Figure 1 - Argument Variables for obtain_token() Function")
    
    **(2).** Now let's run the **_obtain_token()_** function with the variables as the arguments. Here we can see that a dictonary containing a new HyperFlex API token has been returned as highlighted.
      ![Figure 2 - Results from obtain_token() Function - Return Highlighted](./assets/Figure_2-Results_from_obtain_token_Function-Return_Highlighted.png "Figure 2 - Results from obtain_token() Function - Return Highlighted")
      
    **(3).** Another option is to assign the **_obtain_token()_** function to a variable. The returned HyperFlex API token will be directly held by the variable for easy reusability later with other functions.
      ![Figure 3 - Assign obtain_token() Function to Variable](./assets/Figure_3-Assign_obtain_token_Function_to_Variable.png "Figure 3 - Assign obtain_token() Function to Variable")
      
    **(4).** Here we can see that the **token1** variable now holds the returned HyperFlex API token dictionary.
      ![Figure 4 - Assign obtain_token() Function to Variable - Value Returned](./assets/Figure_4-Assign_obtain_token_Function_to_Variable-Value_Returned.png "Figure 4 - Assign obtain_token() Function to Variable - Value Returned")


- ### Refresh Access Tokens
  ```py
  refresh_token(ip,hx_api_token)
  ```
  The function **_refresh_token()_** refreshes or renews a HyperFlex API access token. A new HyperFlex API access token is obtained without the need to provide username and password credentials.
  - **The Available Function Arguments:**
    - **ip** - The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **hx_api_token** - A dictionary value for a granted HyperFlex AAA token containing the following keys:
      - `"access_token"` - An access token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize API operations by properly authenticated users.
      - `"refresh_token"` - A refresh token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The refresh token can be used to obtain a new access token without the need to re-provide HyperFlex username and password credentials.
      - `"token_type"` - A token type obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The token type value is `"Bearer"`.

  - **What the Function Returns:**
  
    A HyperFlex API access token, refresh token and token type that have been granted as key-value pairs in a dictionary.

  - **Example Usage:**
  
    **(1).** First let's create variables to hold the values for the **_refresh_token()_** function arguments. Using variables is not required, but provides for easier readability and the variables can be re-used again at a later time if needed.
      ![Figure 5 - Argument Variables for refresh_token() Function](./assets/Figure_5-Argument_Variables_for_refresh_token_Function.png "Figure 5 - Argument Variables for refresh_token() Function")
    
    **(2).** Now let's run the **_refresh_token()_** function with the variables as the arguments. Here we can see that a dictonary containing a new HyperFlex API token has been returned as highlighted.
      ![Figure 6 - Results from refresh_token() Function - Return Highlighted](./assets/Figure_6-Results_from_refresh_token_Function-Return_Highlighted.png "Figure 6 - Results from refresh_token() Function - Return Highlighted")
      
    **(3).** Here is a comparison of the older HyperFlex API token held by the **token1** variable and the new replacement HyperFlex API token returned by the **_refresh_token()_** function.
      ![Figure 7 - Results from refresh_token() Function Comparison - Values Highlighted](./assets/Figure_7-Results_from_refresh_token_Function_Comparison-Values_Highlighted.png "Figure 7 - Results from refresh_token() Function Comparison - Values Highlighted")


- ### Validate Access Tokens
  ```py
  validate_token(ip,hx_api_token,scope="READ")
  ```
  The function **_validate_token()_** validates a HyperFlex API access token. A newly issued HyperFlex API access token is valid for 18 days from the point of creation. The **_validate_token()_** function can be used to check if an issued HyperFlex API access token is still valid.
  - **The Available Function Arguments:**
    - **ip** - The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **hx_api_token** - A dictionary value for a granted HyperFlex AAA token containing the following keys:
      - `"access_token"` - An access token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize API operations by properly authenticated users.
      - `"refresh_token"` - A refresh token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The refresh token can be used to obtain a new access token without the need to re-provide HyperFlex username and password credentials.
      - `"token_type"` - A token type obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The token type value is `"Bearer"`.
    - **scope** - (Optional) The scope of the validate access token operation. Providing this argument is optional. The value must be a string. The options are `"READ"` or `"MODIFY"`. The default value is `"READ"`.

  - **What the Function Returns:**
  
    The Boolean value `True` is returned for a successful validation. The Boolean value `False` is returned if the validation fails.

  - **Example Usage:**
  
    **(1).** First let's create variables to hold the values for the **_validate_token()_** function arguments. Using variables is not required, but provides for easier readability and the variables can be re-used again at a later time if needed.
      ![Figure 8 - Argument Variables for validate_token() Function](./assets/Figure_8-Argument_Variables_for_validate_token_Function.png "Figure 8 - Argument Variables for validate_token() Function")
    
    **(2).** Now let's run the **_validate_token()_** function with the variables as the arguments. Here we can see that a successful validation has occurred and the Boolean value `True` been returned as highlighted.
      ![Figure 9 - Results from validate_token() Function - Return Highlighted](./assets/Figure_9-Results_from_validate_token_Function-Return_Highlighted.png "Figure 9 - Results from validate_token() Function - Return Highlighted")
      

- ### Revoke Tokens
  ```py
  revoke_token(ip,hx_api_token)
  ```
  The function **_revoke_token()_** revokes a HyperFlex API access token. A newly issued HyperFlex API access token is valid for 18 days from the point of creation. The **_revoke_token()_** function can be used to revoke a previously issued HyperFlex API access token for any reason (e.g. security, etc.).
  - **The Available Function Arguments:**
    - **ip** - The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **hx_api_token** - A dictionary value for a granted HyperFlex AAA token containing the following keys:
      - `"access_token"` - An access token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The access token is used to authorize API operations by properly authenticated users.
      - `"refresh_token"` - A refresh token obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The refresh token can be used to obtain a new access token without the need to re-provide HyperFlex username and password credentials.
      - `"token_type"` - A token type obtained from the HyperFlex API AAA (Authorization, Accounting and Authentication). The token type value is `"Bearer"`.
  
  - **What the Function Returns:**
    
    The Boolean value `True` is returned for a successful revocation. The Boolean value `False` is returned if the revocation fails.

  - **Example Usage:**
  
    **(1).** First let's create variables to hold the values for the **_revoke_token()_** function arguments. Using variables is not required, but provides for easier readability and the variables can be re-used again at a later time if needed.
      ![Figure 10 - Argument Variables for revoke_token() Function](./assets/Figure_10-Argument_Variables_for_revoke_token_Function.png "Figure 10 - Argument Variables for revoke_token() Function")
    
    **(2).** Now let's run the **_revoke_token()_** function with the variables as the arguments. Here we can see that a successful revocation has occurred and the Boolean value `True` been returned as highlighted.
      ![Figure 11 - Results from revoke_token() Function - Return Highlighted](./assets/Figure_11-Results_from_revoke_token_Function-Return_Highlighted.png "Figure 11 - Results from revoke_token() Function - Return Highlighted")




### _Advanced Functions_
The Cisco HyperFlex API Token Manager module contains three additional functions that provide the ability to automate the creation, validation and renewal of access tokens. Offline token use is also provided among other features.

- ### Automated Management of Token Files
  ```py
  manage_token_file(ip,username,password,file_path,data="token",overwrite=True)
  ```
  The function **_manage_token_file()_** creates or loads an XML file containing a HyperFlex API token and then validates the loaded token data. If the loaded HyperFlex API access token is not valid, a new access token will be automatically obtained. If there is a no HyperFlex API token file present in the provided file path, a new token file will be automatically created.
  - **The Available Function Arguments:**
    - **ip** - The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **username** - The username credentials that will be used to log into HyperFlex. The value must be a string.
    - **password** - The password credentials that will be used to log into HyperFlex. The value must be a string.
    - **file_path** - The file name and storage location to write a HyperFlex API token file. The value must be a string. An example value is `"c:\\folder\\file.xml"`.
    - **data** - (Optional) The data from a HyperFlex API token file that is returned by the **_manage_token_file()_** function. Providing this argument is optional. The default value of `"token"` is set, which returns the access token, refresh token, and token type as a dictionary. The user provided value must be a string. See the following list for the options available for the **data** argument and the returned value:
      - `"token"` - Returns a dictionary with the access token, refresh token, and token type.
      - `"access_token"` - Returns a string value of only the access token.
      - `"refresh_token"` - Returns a string value of only the refresh token.
      - `"token_type"` - Returns a string value of only the token type.
      - `"human_readable_time"` - Returns a string value of the HyperFlex API token file creation time in a human-readable format.
      - `"unix_timestamp_time"` - Returns a string value of the HyperFlex API token file creation time in Unix timestamp format.
      - `"source_module"` - Returns a string value of the source module used to create the HyperFlex API token file.
    
      **`NOTE:`** For automatic validation and renewals of HyperFlex API tokens to occur, the data argument must be set to `"token"` (default), `"access_token"`, or `"refresh_token"`.
    - **overwrite** - (Optional) The option to overwrite any pre-existing file at the provided file path value given to the **file_path** argument. Providing this argument is optional. If the argument is set to the Boolean value `True`, any pre-exiting token file will be automatically overwritten. If the argument is set to the Boolean value `False`, the **_manage_token_file()_** function will stop and not proceed with creating a new token file if a pre-existing token file is already in place at the given file path location. The default value is `True`.
    
      **`NOTE:`** For automatic validation and renewals of HyperFlex API tokens to occur, the **overwrite** argument must be set to the Boolean value `True` (default). Setting the **overwrite** argument to the Boolean value `False` will disable the ability to update pre-existing HyperFlex API token files.
    
  - **What the Function Returns:**
    
    The return is based on the value of the **data** argument. If the default value of `"token"` is set, the access token, refresh token, and token type will be returned as a dictionary. See the following list to see the options available for the **data** argument and the returned value:
      - `"token"` - Returns a dictionary with the access token, refresh token, and token type.
      - `"access_token"` - Returns a string value of only the access token.
      - `"refresh_token"` - Returns a string value of only the refresh token.
      - `"token_type"` - Returns a string value of only the token type.
      - `"human_readable_time"` - Returns a string value of the HyperFlex API token file creation time in a human-readable format.
      - `"unix_timestamp_time"` - Returns a string value of the HyperFlex API token file creation time in the Unix timestamp format.
      - `"source_module"` - Returns a string value of the source module used to create the HyperFlex API token file.


- ### Creation of Token Files
  ```py
  create_token_file(ip,username,password,file_path,overwrite=True)
  ```
  The function **_create_token_file()_** creates an XML file containing a newly issued HyperFlex API token.
  
  **`NOTE:`** For automated creation, validation and renewal of HyperFlex API token files, the [**_manage_token_file()_**](https://github.com/ugo-emekauwa/hx-api-token-manager#automated-management-of-token-files) function should be used. The **_create_token_file()_** function will only create new HyperFlex API token files.
  
  - **The Available Function Arguments:**
    - **ip** - The targeted HyperFlex Connect or Cluster Management IP address. The value must be a string.
    - **username** - The username credentials that will be used to log into HyperFlex. The value must be a string.
    - **password** - The password credentials that will be used to log into HyperFlex. The value must be a string.
    - **file_path** - The file name and storage location to write a HyperFlex API token file. The value must be a string. An example value is `"c:\\folder\\file.xml"`.
    - **overwrite** - (Optional) The option to overwrite any pre-existing file at the provided file path value given to the **file_path** argument. Providing this argument is optional. If the argument is set to the Boolean value `True`, any pre-exiting token file will be automatically overwritten. If the argument is set to the Boolean value `False`, the **_create_token_file()_** function will stop and not proceed with creating a new token file if a pre-existing token file is already in place at the given file path location. The default value is `True`.
    
  - **What the Function Returns:**
    
    The file path of the new HyperFlex API token file in XML format is returned if creation was successful. The value `None` is returned if creating a HyperFlex API token file failed.


- ### Loading Token Files
  ```py
  load_token_file(file_path,data="token")
  ```
  The function **_load_token_file()_** loads data from an XML file containing a HyperFlex API token.
  
  **`NOTE:`** For automated creation, validation and renewal of HyperFlex API token files, the [**_manage_token_file()_**](https://github.com/ugo-emekauwa/hx-api-token-manager#automated-management-of-token-files) function should be used. The **_load_token_file()_** function will only load data from pre-exisiting HyperFlex API token files.
  
  - **The Available Function Arguments:**
    - **file_path** - The file name and storage location from which to load a HyperFlex API token file. The value must be a string. An example value is `"c:\\folder\\file.xml"`.
    - **data** - (Optional) The data from a HyperFlex API token file that is returned by the **_load_token_file()_** function. Providing this argument is optional. The default value of `"token"` is set, which returns the access token, refresh token, and token type as a dictionary. The user provided value must be a string. See the following list for the options available for the **data** argument and the returned value:
      - `"token"` - Returns a dictionary with the access token, refresh token, and token type.
      - `"access_token"` - Returns a string value of only the access token.
      - `"refresh_token"` - Returns a string value of only the refresh token.
      - `"token_type"` - Returns a string value of only the token type.
      - `"human_readable_time"` - Returns a string value of the HyperFlex API token file creation time in a human-readable format.
      - `"unix_timestamp_time"` - Returns a string value of the HyperFlex API token file creation time in Unix timestamp format.
      - `"source_module"` - Returns a string value of the source module used to create the HyperFlex API token file.

  - **What the Function Returns:**
    
    The return is based on the value of the **data** argument. If the default value of `"token"` is set, the access token, refresh token, and token type will be returned as a dictionary. See the following list to see the options available for the **data** argument and the returned value:
      - `"token"` - Returns a dictionary with the access token, refresh token, and token type.
      - `"access_token"` - Returns a string value of only the access token.
      - `"refresh_token"` - Returns a string value of only the refresh token.
      - `"token_type"` - Returns a string value of only the token type.
      - `"human_readable_time"` - Returns a string value of the HyperFlex API token file creation time in a human-readable format.
      - `"unix_timestamp_time"` - Returns a string value of the HyperFlex API token file creation time in Unix timestamp format.
      - `"source_module"` - Returns a string value of the source module used to create the HyperFlex API token file.


## Related Tools:
Here are similar tools to help manage Cisco HyperFlex training, demonstration and development environments.
- [Cisco HyperFlex Datastore Safeguard](https://github.com/ugo-emekauwa/hx-datastore-safeguard)
- [Cisco HyperFlex Datastore Cleanup](https://github.com/ugo-emekauwa/hx-datastore-cleanup)
- [HyperFlex Notification Tool for Cisco Intersight](https://github.com/ugo-emekauwa/hyperflex-notification-tool)

## Author:
Ugo Emekauwa

## Contact Information:
uemekauw@cisco.com or uemekauwa@gmail.com
