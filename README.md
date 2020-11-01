# Cisco HyperFlex API Token Manager

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/ugo-emekauwa/hx-api-token-manager)

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
    
    **(2).** Now let's run the **_obtain_token()_** function with the variables as the arguments. Here we can see that a dictionary containing a new HyperFlex API token has been returned as highlighted.
    
      ![Figure 2 - Results from obtain_token() Function - Return Highlighted](./assets/Figure_2-Results_from_obtain_token_Function-Return_Highlighted.png "Figure 2 - Results from obtain_token() Function - Return Highlighted")
      
    **(3).** Another option is to assign the **_obtain_token()_** function to a variable. The returned HyperFlex API token dictionary will be directly held by the variable for easy reusability later with other functions.
    
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
    
    **(2).** Now let's run the **_refresh_token()_** function with the variables as the arguments. Here we can see that a dictionary containing a new HyperFlex API token has been returned as highlighted.
    
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
    - **overwrite** - (Optional) The option to overwrite any pre-existing file at the provided file path value given to the **file_path** argument. Providing this argument is optional. If the argument is set to the Boolean value `True`, any pre-existing token file will be automatically overwritten. If the argument is set to the Boolean value `False`, the **_manage_token_file()_** function will stop and not proceed with creating a new token file if a pre-existing token file is already in place at the given file path location. The default value is `True`.
    
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
  
  - **Example Usage:**
  
    **(1).** First let's create variables to hold the values for the **_manage_token_file()_** function arguments. Using variables is not required, but provides for easier readability and the variables can be re-used again at a later time if needed.
    
      ![Figure 12 - Argument Variables for manage_token_file() Function](./assets/Figure_12-Argument_Variables_for_manage_token_file_Function.png "Figure 12 - Argument Variables for manage_token_file() Function")
    
    **(2).** Now let's run the **_manage_token_file()_** function with the variables as the arguments. Here we can see that a dictionary containing a new HyperFlex API token has been returned as highlighted.
    
      ![Figure 13 - Results from manage_token_file() Function - Return Highlighted](./assets/Figure_13-Results_from_manage_token_file_Function-Return_Highlighted.png "Figure 13 - Results from manage_token_file() Function - Return Highlighted")
      
    **(3).** Here we can see a sample HyperFlex API token file and the available data in XML format created by the **_manage_token_file()_** function. The XML file is held at the storage location given in the **file_path** argument.
    
      ![Figure 14 - Sample XML File Created by manage_token_file() Function](./assets/Figure_14-Sample_XML_File_Created_by_manage_token_file_Function.png "Figure 14 - Sample XML File Created by manage_token_file() Function")
      
    **(4).** Another option is to assign the **_manage_token_file()_** function to a variable. The returned HyperFlex API token dictionary will be directly held by the variable for easy reusability later with other functions.
    
      ![Figure 15 - Assign manage_token_file() Function to Variable](./assets/Figure_15-Assign_manage_token_file_Function_to_Variable.png "Figure 15 - Assign manage_token_file() Function to Variable")
      
    **(5).** Here we can see that the **token1** variable now holds the returned HyperFlex API token dictionary.
    
      ![Figure 16 - Assign manage_token_file() Function to Variable - Value Returned](./assets/Figure_16-Assign_manage_token_file_Function_to_Variable-Value_Returned.png "Figure 16 - Assign manage_token_file() Function to Variable - Value Returned")
      
    **(6).** Now let's run the **_manage_token_file()_** function with the **data** argument set to `"access_token"`. Here we can see that only the HyperFlex API access token has been returned as highlighted.
    
      ![Figure 17 - Results from manage_token_file() Function - access_token Returned](./assets/Figure_17-Results_from_manage_token_file_Function-access_token_Returned.png "Figure 17 - Results from manage_token_file() Function - access_token Returned")
    
    **(7).** Now let's run the **_manage_token_file()_** function with the **data** argument set to `"refresh_token"`. Here we can see that only the HyperFlex API refresh token has been returned as highlighted.
    
      ![Figure 18 - Results from manage_token_file() Function - refresh_token Returned](./assets/Figure_18-Results_from_manage_token_file_Function-refresh_token_Returned.png "Figure 18 - Results from manage_token_file() Function - refresh_token Returned")
      
    **(8).** Now let's run the **_manage_token_file()_** function with the **data** argument set to `"token_type"`. Here we can see that only the HyperFlex API token type has been returned as highlighted.
    
      ![Figure 19 - Results from manage_token_file() Function - token_type Returned](./assets/Figure_19-Results_from_manage_token_file_Function-token_type_Returned.png "Figure 19 - Results from manage_token_file() Function - token_type Returned")
      
    **(9).** Now let's run the **_manage_token_file()_** function with the **data** argument set to `"human_readable_time"`. Here we can see that only the HyperFlex API token creation time in a human-readable format has been returned as highlighted.
    
      ![Figure 20 - Results from manage_token_file() Function - human_readable_time Returned](./assets/Figure_20-Results_from_manage_token_file_Function-human_readable_time_Returned.png "Figure 20 - Results from manage_token_file() Function - human_readable_time Returned")
      
    **(10).** Now let's run the **_manage_token_file()_** function with the **data** argument set to `"unix_timestamp_time"`. Here we can see that only the HyperFlex API token creation time in the Unix timestamp format has been returned as highlighted.
    
      ![Figure 21 - Results from manage_token_file() Function - unix_timestamp_time Returned](./assets/Figure_21-Results_from_manage_token_file_Function-unix_timestamp_time_Returned.png "Figure 21 - Results from manage_token_file() Function - unix_timestamp_time Returned")

    **(11).** Now let's run the **_manage_token_file()_** function with the **data** argument set to `"source_module"`. Here we can see that only the source module from which the **_manage_token_file()_** function was called has been returned as highlighted.
    
      ![Figure 22 - Results from manage_token_file() Function - source_module Returned](./assets/Figure_22-Results_from_manage_token_file_Function-source_module_Returned.png "Figure 22 - Results from manage_token_file() Function - source_module Returned")


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
    - **overwrite** - (Optional) The option to overwrite any pre-existing file at the provided file path value given to the **file_path** argument. Providing this argument is optional. If the argument is set to the Boolean value `True`, any pre-existing token file will be automatically overwritten. If the argument is set to the Boolean value `False`, the **_create_token_file()_** function will stop and not proceed with creating a new token file if a pre-existing token file is already in place at the given file path location. The default value is `True`.
    
  - **What the Function Returns:**
    
    The file path of the new HyperFlex API token file in XML format is returned if creation was successful. The value `None` is returned if creating a HyperFlex API token file failed.
    
  - **Example Usage:**
  
    **(1).** First let's create variables to hold the values for the **_create_token_file()_** function arguments. Using variables is not required, but provides for easier readability and the variables can be re-used again at a later time if needed.
    
      ![Figure 23 - Argument Variables for create_token_file() Function](./assets/Figure_23-Argument_Variables_for_create_token_file_Function.png "Figure 23 - Argument Variables for create_token_file() Function")
    
    **(2).** Now let's run the **_create_token_file()_** function with the variables as the arguments. Here we can see that a new HyperFlex API token file has been created. The storage location of the new HyperFlex API token file has been returned as highlighted.
    
      ![Figure 24 - Results from create_token_file() Function - Return Highlighted](./assets/Figure_24-Results_from_create_token_file_Function-Return_Highlighted.png "Figure 24 - Results from create_token_file() Function - Return Highlighted")
      
    **(3).** Here we can see a sample HyperFlex API token file and the available data in XML format created by the **_create_token_file()_** function. The XML file is held at the storage location given in the **file_path** argument.
    
      ![Figure 25 - Sample XML File Created by create_token_file() Function](./assets/Figure_25-Sample_XML_File_Created_by_create_token_file_Function.png "Figure 25 - Sample XML File Created by create_token_file() Function")
      
    **(4).** Now let's run the **_manage_token_file()_** function with the **overwrite** argument set to `False`. Here we can see that the pre-existing HyperFlex API token file was not overwritten.
    
      ![Figure 26 - Results from create_token_file() Function - overwrite Argument Set to False](./assets/Figure_26-Results_from_create_token_file_Function-overwrite_Argument_Set_to_False.png "Figure 26 - Results from create_token_file() Function - overwrite Argument Set to False")


- ### Loading Token Files
  ```py
  load_token_file(file_path,data="token")
  ```
  The function **_load_token_file()_** loads data from an XML file containing a HyperFlex API token.
  
  **`NOTE:`** For automated creation, validation and renewal of HyperFlex API token files, the [**_manage_token_file()_**](https://github.com/ugo-emekauwa/hx-api-token-manager#automated-management-of-token-files) function should be used. The **_load_token_file()_** function will only load data from pre-existing HyperFlex API token files.
  
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
      
  - **Example Usage:**
  
    **(1).** First let's create variables to hold the values for the **_load_token_file()_** function arguments. Using variables is not required, but provides for easier readability and the variables can be re-used again at a later time if needed.
    
      ![Figure 27 - Argument Variables for load_token_file() Function](./assets/Figure_27-Argument_Variables_for_load_token_file_Function.png "Figure 27 - Argument Variables for load_token_file() Function")
    
    **(2).** Now let's run the **_load_token_file()_** function with the variables as the arguments. Here we can see that a dictionary containing a new HyperFlex API token has been returned as highlighted.
    
      ![Figure 28 - Results from load_token_file() Function - Return Highlighted](./assets/Figure_28-Results_from_load_token_file_Function-Return_Highlighted.png "Figure 28 - Results from load_token_file() Function - Return Highlighted")
      
    **`NOTE:`** For examples of the output from the various optional values of the **data** argument, see the **Example Usage** section for the [**_manage_token_file()_**](https://github.com/ugo-emekauwa/hx-api-token-manager#automated-management-of-token-files) function. The type of outputs are the same for the **_load_token_file()_** function.

## Notes:
- For setups where logging is desired, a version of the **Cisco HyperFlex API Token Manager** that has been modified to output to a log file is available in the [**logging-version**](https://github.com/ugo-emekauwa/hx-api-token-manager/tree/master/logging-version) folder of this repository as **hx_api_token_manager_logging.py**. Before use, manually edit the **hx_api_token_manager_logging.py** file to add a log file location or import **hx_api_token_manager_logging** into another module where the log file location has already been set.

## Use Cases:
The Cisco HyperFlex API Token Manager is part of the automation solution used to support and maintain the following Cisco Data Center product demonstrations on Cisco dCloud:

1. [_Cisco HyperFlex with Hyper-V v1_](https://dcloud2-rtp.cisco.com/content/instantdemo/cisco-hyperflex-with-hyper-v)

Cisco dCloud is available at [https://dcloud.cisco.com](https://dcloud.cisco.com), where product demonstrations and labs can be found in the Catalog.

## Related Tools:
Here are similar tools to help manage Cisco HyperFlex training, demonstration and development environments.
- [Cisco HyperFlex Datastore Safeguard](https://github.com/ugo-emekauwa/hx-datastore-safeguard)
- [Cisco HyperFlex Datastore Cleanup](https://github.com/ugo-emekauwa/hx-datastore-cleanup)
- [HyperFlex Notification Tool for Cisco Intersight](https://github.com/ugo-emekauwa/hyperflex-notification-tool)
- [HyperFlex Edge Automated Deployment Tool for Cisco Intersight](https://github.com/ugo-emekauwa/hx-auto-deploy)

## Author:
Ugo Emekauwa

## Contact Information:
uemekauw@cisco.com or uemekauwa@gmail.com
