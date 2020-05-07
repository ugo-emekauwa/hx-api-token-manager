"""
Cisco HyperFlex API Token Manager, v1
Author: Ugo Emekauwa
Contact: uemekauw@cisco.com, uemekauwa@gmail.com
Summary: Cisco HyperFlex API Token Manager provides the ability to
         automate the creation, validation and renewal of HyperFlex API tokens.
         Basic administration of HyperFlex API tokens is also available with
         easy to use Python functions that simplify obtaining, refreshing,
         revoking and validating tokens.
Notes: Tested on HyperFlex 4.0(1b), 4.0(2a), and 4.0(2b).
"""

# Import needed modules
import os
import requests
import json
import urllib3
import datetime
import xml.etree.ElementTree as et
import collections

# Suppress InsecureRequestWarning
urllib3.disable_warnings()

# Establish HyperFlex API Token Manager Functions

def obtain_token(ip,username,password):
    """This is a function that obtains a HyperFlex API access token.
    A HyperFlex API access token authorizes API operations on a HyperFlex
    cluster.

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            The value must be a string.
        username: The username credentials that will be used to log into
            HyperFlex. The value must be a string.
        password: The password credentials that will be used to log into
            HyperFlex. The value must be a string.

    Returns:
        A HyperFlex API access token, refresh token and token type that have
        been granted as key-value pairs in a dictionary.

    Raises:
        Exception: There was an error obtaining a HyperFlex API access token.
            The status code or error message will be specified.
    """

    # Set the Request headers
    request_headers = {"Content-Type": "application/json"}
    # Set the Request URL
    request_url = "https://{}/aaa/v1/auth?grant_type=password".format(ip)
    # Set the POST body
    post_body = {
        "username": username,
        "password": password,
        "client_id": "HxGuiClient",
        "client_secret": "Sunnyvale",
        "redirect_uri": "http://localhost:8080/aaa/redirect"
        }

    try:
        print("Attempting to obtain a HyperFlex API access token...")
        # Send the POST request
        obtain_hx_api_token = requests.post(request_url,
                                            headers=request_headers,
                                            data=json.dumps(post_body),
                                            verify=False
                                            )
        # Handle POST request response
        if obtain_hx_api_token.status_code == 201:
            hx_api_token = obtain_hx_api_token.json()
            print("A HyperFlex API access token was successfully obtained.")
            return hx_api_token
        else:
            print("There was an error obtaining a HyperFlex API access token: ")
            print("Status Code: {}".format(str(obtain_hx_api_token.status_code)))
            print("{}".format(str(obtain_hx_api_token.json())))
            return
    except Exception as exception_message:
        print("There was an error obtaining a HyperFlex API access token: ")
        print("{}".format(str(exception_message)))
        return


def refresh_token(ip,hx_api_token):
    """This is a function that refreshes or renews a HyperFlex API access
    token. A new HyperFlex API access token is obtained without the need to
    provide username and password credentials.

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            The value must be a string.
        hx_api_token: A dictionary value for a granted HyperFlex AAA token
            containing the following keys:
            1. "access_token": An access token obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The
                access token is used to authorize API operations by properly
                authenticated users.
            2. "refresh_token": A refresh token obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The
                refresh token can be used to obtain a new access token without
                the need to re-provide HyperFlex username and password
                credentials.
            3. "token_type": A token type obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The
                token type value is "Bearer".

    Returns:
        A HyperFlex API access token, refresh token and token type that have
        been granted as key-value pairs in a dictionary.

    Raises:
        Exception: There was an error refreshing the HyperFlex API access
            token. The status code or error message will be specified.
        ValueError: There was an invalid argument provided for the HyperFlex
            API token. A recommendation on how to resolve the error will be
            displayed.
    """

    # Verify the hx_api_token argument
    if not isinstance(hx_api_token, collections.abc.Mapping):
        raise ValueError("The argument provided for the HyperFlex API token "
                         "is not valid. Please provide a valid dictionary "
                         "for the 'hx_api_token' argument.")
    
    # Set the Request headers
    request_headers = {"Content-Type": "application/json"}
    # Set the Request URL
    request_url = "https://{}/aaa/v1/token?grant_type=refresh".format(ip)
    # Set the POST body
    post_body = {
        "access_token": hx_api_token["access_token"],
        "refresh_token": hx_api_token["refresh_token"],
        "token_type": hx_api_token["token_type"]
        }

    try:
        print("Attempting to refresh the HyperFlex API access token...")
        # Send the POST request
        refresh_hx_api_token = requests.post(request_url,
                                             headers=request_headers,
                                             data=json.dumps(post_body),
                                             verify=False
                                             )
        # Handle POST request response
        if refresh_hx_api_token.status_code == 201:
            hx_api_token = refresh_hx_api_token.json()
            print("The HyperFlex API access token was successfully refreshed.")
            return hx_api_token
        else:
            print("There was an error refreshing the HyperFlex API access token: ")
            print("Status Code: {}".format(str(refresh_hx_api_token.status_code)))
            print("{}".format(str(refresh_hx_api_token.json())))
            return
    except Exception as exception_message:
        print("There was an error refreshing the HyperFlex API access token: ")
        print("{}".format(str(exception_message)))
        return


def validate_token(ip,hx_api_token,scope="READ"):
    """This is a function that validates a HyperFlex API access token.
    A newly issued HyperFlex API access token is valid for 18 days from the
    point of creation. The validate_token() function can be used to check if
    an issued HyperFlex API access token is still valid.

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            The value must be a string.
        hx_api_token: A dictionary value for a granted HyperFlex AAA token
            containing the following keys:
            1. "access_token": An access token obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The access
                token is used to authorize API operations by properly
                authenticated users.
            2. "refresh_token": A refresh token obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The
                refresh token can be used to obtain a new access token without
                the need to re-provide HyperFlex username and password
                credentials.
            3. "token_type": A token type obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The
                token type value is "Bearer".
        scope: (Optional) The scope of the validate access token operation.
            Providing this argument is optional. The value must be a string.
            The options are "READ" or "MODIFY". The default value is "READ".

    Returns:
        The Boolean value True is returned for a successful validation. The
        Boolean value False is returned if the validation fails.

    Raises:
        Exception: There was an error performing the validation of the
            HyperFlex API access token. The status code or error message will
            be specified.
        ValueError: There was an invalid argument provided for the HyperFlex
            API token or desired scope operation. A recommendation on how to
            resolve the error will be displayed.
    """

    # Verify the hx_api_token argument
    if not isinstance(hx_api_token, collections.abc.Mapping):
        raise ValueError("The argument provided for the HyperFlex API token "
                         "is not valid. Please provide a valid dictionary "
                         "for the 'hx_api_token' argument.")

    # Verify the scope argument
    if scope not in ("READ", "MODIFY"):
        raise ValueError("The argument provided for the scope operation is "
                         "not valid. Please provide either the value 'READ' "
                         "or 'MODIFY' in string format for the 'scope' "
                         "argument.")
    
    # Set the Request headers
    request_headers = {"Content-Type": "application/json"}
    # Set the Request URL
    request_url = "https://{}/aaa/v1/validate".format(ip)
    # Set the POST body
    post_body = {
        "access_token": hx_api_token["access_token"],
        "scope": scope,
        "token_type": hx_api_token["token_type"]
        }

    try:
        print("Attempting to validate the HyperFlex API access token...")
        # Send the POST request
        validate_hx_api_token = requests.post(request_url,
                                              headers=request_headers,
                                              data=json.dumps(post_body),
                                              verify=False
                                              )
        # Handle POST request response
        if validate_hx_api_token.status_code == 200:
            print("The HyperFlex API access token was successfully validated.")
            return True
        else:
            print("There was an error validating the HyperFlex API access token: ")
            print("Status Code: {}".format(str(validate_hx_api_token.status_code)))
            print("{}".format(str(validate_hx_api_token.json())))
            return False
    except Exception as exception_message:
        print("There was an error validating the HyperFlex API access token: ")
        print("{}".format(str(exception_message)))
        return False


def revoke_token(ip,hx_api_token):
    """This is a function that revokes a HyperFlex API access token.
    A newly issued HyperFlex API access token is valid for 18 days from the
    point of creation. The revoke_token() function can be used to revoke a
    previously issued HyperFlex API access token for any reason (e.g. security,
    etc.).

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            The value must be a string.
        hx_api_token: A dictionary value for a granted HyperFlex AAA token
            containing the following keys:
            1. "access_token": An access token obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The
                access token is used to authorize API operations by properly
                authenticated users.
            2. "refresh_token": A refresh token obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The
                refresh token can be used to obtain a new access token without
                the need to re-provide HyperFlex username and password
                credentials.
            3. "token_type": A token type obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The
                token type value is "Bearer".

    Returns:
        The Boolean value True is returned for a successful revocation. The
        Boolean value False is returned if the revocation fails.

    Raises:
        Exception: There was an error performing the revocation of the
            HyperFlex API access token. The status code or error message will
            be specified.
        ValueError: There was an invalid argument provided for the HyperFlex
            API token. A recommendation on how to resolve the error will be
            displayed.
    """

    # Verify the hx_api_token argument
    if not isinstance(hx_api_token, collections.abc.Mapping):
        raise ValueError("The argument provided for the HyperFlex API token "
                         "is not valid. Please provide a valid dictionary "
                         "for the 'hx_api_token' argument.")

    # Set the Request headers
    request_headers = {"Content-Type": "application/json"}
    # Set the Request URL
    request_url = "https://{}/aaa/v1/revoke".format(ip)
    # Set the POST body
    post_body = {
        "access_token": hx_api_token["access_token"],
        "refresh_token": hx_api_token["refresh_token"],
        "token_type": hx_api_token["token_type"]
        }

    try:
        print("Attempting to revoke the HyperFlex API access token...")
        # Send the POST request
        revoke_hx_api_token = requests.post(request_url,
                                            headers=request_headers,
                                            data=json.dumps(post_body),
                                            verify=False
                                            )
        # Handle POST request response
        if revoke_hx_api_token.status_code == 200:
            print("The HyperFlex API access token was successfully revoked.")
            return True
        else:
            print("There was an error revoking the HyperFlex API access token: ")
            print("Status Code: {}".format(str(revoke_hx_api_token.status_code)))
            print("{}".format(str(revoke_hx_api_token.json())))
            return False
    except Exception as exception_message:
        print("There was an error revoking the HyperFlex API access token: ")
        print("{}".format(str(exception_message)))
        return False


def create_token_file(ip,username,password,file_path,overwrite=True):
    r"""This is a function that creates an XML file containing a newly issued
    HyperFlex API token.

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            The value must be a string.
        username: The username credentials that will be used to log into
            HyperFlex. The value must be a string.
        password: The password credentials that will be used to log into
            HyperFlex. The value must be a string.
        file_path: The file name and storage location to write a HyperFlex API
            token file. The value must be a string. An example value is
            "c:\\folder\\file.xml".
        overwrite: (Optional) The option to overwrite any pre-existing file at
            the provided file path value given to the 'file_path' argument.
            Providing this argument is optional. If the argument is set to the
            Boolean value True, any pre-exiting token file will be
            automatically overwritten. If the argument is set to the Boolean
            value False, the create_token_file() function will stop and not
            proceed with creating a new token file if a pre-existing token
            file is already in place at the given file path location. The
            default value is True.

    Returns:
        The file path of the new HyperFlex API token file in XML format is
        returned if creation was successful. The value None is returned if
        creating a HyperFlex API token file failed.

    Raises:
        Exception: An exception occurred while creating a HyperFlex API token
            file. The exact error will be specified.
        ValueError: There was an invalid argument provided for the overwrite
            setting. A recommendation on how to resolve the error will be
            displayed.
    """

    # Verify the overwrite argument
    if not isinstance(overwrite, bool):
        raise ValueError("The overwrite setting is not valid. Please provide "
                         "a Boolean value of True or False for the "
                         "'overwrite' argument.")
    
    # Start the HyperFlex API token file creation process
    print("Starting the HyperFlex API token file creation process...")
    # Check the overwrite argument setting
    if not overwrite:
        # Check for the presence of a pre-existing HyperFlex API token file
        if os.path.isfile(file_path):
            print("A HyperFlex API token file already exists at the given "
                  "file path location. No changes have been made.")
            print("To overwrite the pre-existing file, set the 'overwrite' "
                  "argument to the Boolean value True.")
            return
    # Obtain a new HyperFlex API token
    hx_api_token = obtain_token(ip,username,password)
    try:
        # Establish XML file tree nodes
        hx_api_token_xml_data = et.Element("hx_api_token")
        token_xml_data = et.SubElement(hx_api_token_xml_data, "token")
        access_token_xml_data = et.SubElement(token_xml_data, "access_token")
        refresh_token_xml_data = et.SubElement(token_xml_data, "refresh_token")
        token_type_xml_data = et.SubElement(token_xml_data, "token_type")
        creation_time_format_xml_data = et.SubElement(hx_api_token_xml_data,
                                                      "creation_time_format"
                                                      )
        human_readable_time_xml_data = et.SubElement(creation_time_format_xml_data,
                                                     "human_readable_time"
                                                     )
        unix_timestamp_time_xml_data = et.SubElement(creation_time_format_xml_data,
                                                     "unix_timestamp_time"
                                                     )
        source_module_xml_data = et.SubElement(hx_api_token_xml_data,
                                               "source_module"
                                               )
        # Map HyperFlex API token data to XML entries
        access_token_xml_data.text = hx_api_token["access_token"]
        refresh_token_xml_data.text = hx_api_token["refresh_token"]
        token_type_xml_data.text = hx_api_token["token_type"]
        human_readable_time_xml_data.text = datetime.datetime.utcnow().strftime(
            "%A, %B %d, %Y at %I:%M:%S %p UTC")
        unix_timestamp_time_xml_data.text = str(int(datetime.datetime.utcnow(
            ).timestamp()))
        if __file__:
            source_module_xml_data.text = __file__
        else:
            source_module_xml_data.text = "N/A"
        # Establish XML file tree
        hx_api_token_xml = et.ElementTree(hx_api_token_xml_data)
        # Write XML file
        hx_api_token_xml.write(file_path)
        print("A HyperFlex API token file has been created at {}.".format(
            file_path)
              )
        return file_path
    except Exception as exception_message:
        print("There was an error creating a HyperFlex API token file: ")
        print("{}".format(str(exception_message)))
        return


def load_token_file(file_path,data="token"):
    r"""This is a function that loads data from an XML file containing a
    HyperFlex API token.

    Args:
        file_path: The file name and storage location from which to load a
            HyperFlex API token file. The value must be a string. An example
            value is "c:\\folder\\file.xml".
        data: (Optional) The data from a HyperFlex API token file that is
            returned by the load_token_file() function. Providing this
            argument is optional. The default value of "token" is set, which
            returns the access token, refresh token, and token type as a
            dictionary. The user provided value must be a string. See the
            following list for the options available for the 'data' argument and
            the returned value:
            1. "token": Returns a dictionary with the access token, refresh
                token, and token type.
            2. "access_token": Returns a string value of only the access
                token.
            3. "refresh_token": Returns a string value of only the refresh
                token.
            4. "token_type": Returns a string value of only the token type.
            5. "human_readable_time": Returns a string value of the HyperFlex API
                token file creation time in a human-readable format.
            6. "unix_timestamp_time": Returns a string value of the HyperFlex API
                token file creation time in Unix timestamp format.
            7. "source_module": Returns a string value of the source module
                used to create the HyperFlex API token file.
    
    Returns:
        The return is based on the value of the 'data' argument. If the default
        value of "token" is set, the access token, refresh token, and token
        type will be returned as a dictionary. See the following list to see
        the options available for the 'data' argument and the returned value:
            1. "token": Returns a dictionary with the access token, refresh
                token, and token type.
            2. "access_token": Returns a string value of only the access token.
            3. "refresh_token": Returns a string value of only the refresh token.
            4. "token_type": Returns a string value of only the token type.
            5. "human_readable_time": Returns a string value of the HyperFlex
                API token file creation time in a human-readable format.
            6. "unix_timestamp_time": Returns a string value of the HyperFlex
                API token file creation time in Unix timestamp format.
            7. "source_module": Returns a string value of the source module
                used to create the HyperFlex API token file.

    Raises:
        Exception: An exception occurred while loading the HyperFlex API token
            file. The exact error will be specified.
        ValueError: There was an invalid argument provided for the file path
            or data setting. A recommendation on how to resolve the error will
            be displayed.
    """

    # Verify the file_path argument
    if not os.path.isfile(file_path):
        raise ValueError(r"The file at the provided file path does not exist. "
                         "Please provide the file path to a valid file in "
                         "string format for the 'file_path' argument. An "
                         "example value is 'c:\\folder\\file.xml'.")

    # Verify the data argument
    if data not in ("token",
                    "access_token",
                    "refresh_token",
                    "token_type",
                    "human_readable_time",
                    "unix_timestamp_time",
                    "source_module"
                    ):
        raise ValueError("The argument provided for the requested data type "
                         "is not valid. Run 'help(load_token_file)' for "
                         "available options.")

    # Start the HyperFlex API token file loading process
    print("Starting the HyperFlex API token file loading process...")
    # Verify the presence of the HyperFlex API token file and load data
    print("Verifying the presence of the HyperFlex API token file...")
    try:
        if not os.path.isfile(file_path):
            print("The HyperFlex API token file was not found.")
            return
        else:
            print("The HyperFlex API token file was found, proceeding with "
                  "loading data from the file...")
            # Load and parse the XML data in the HyperFlex API token file
            hx_api_token_xml_data = et.parse(file_path)
            # Map the XML data to the potential return data values
            access_token_data = hx_api_token_xml_data.find(
                "token/access_token").text
            refresh_token_data = hx_api_token_xml_data.find(
                "token/refresh_token").text
            token_type_data = hx_api_token_xml_data.find(
                "token/token_type").text
            human_readable_time_data = hx_api_token_xml_data.find(
                "creation_time_format/human_readable_time").text
            unix_timestamp_time_data = hx_api_token_xml_data.find(
                "creation_time_format/unix_timestamp_time").text
            source_module_data = hx_api_token_xml_data.find(
                "source_module").text
            token_data = {"access_token": access_token_data,
                          "refresh_token": refresh_token_data,
                          "token_type": token_type_data
                          }
        print("The HyperFlex API token file has been loaded.")
        # Return the value mapped to the data argument setting
        if data == "token":
            print("The requested token data has been returned.")
            return token_data
        elif data == "access_token":
            print("The requested access token data has been returned.")
            return access_token_data
        elif data == "refresh_token":
            print("The requested refresh token data has been returned.")
            return refresh_token_data
        elif data == "token_type":
            print("The requested token type data has been returned.")
            return token_type_data
        elif data == "human_readable_time":
            print("The requested human readable time data has been returned.")
            return human_readable_time_data
        elif data == "unix_timestamp_time":
            print("The requested Unix timestamp data has been returned.")
            return unix_timestamp_time_data
        elif data == "source_module":
            print("The requested source module data has been returned.")
            return source_module_data
        else:
            print("No data has been returned, a valid value for the 'data' "
                  "argument needs to be provided.",
                  """
                  Please provide one of the following options in string
                  format for the 'data' argument:
                      1. "token": Returns a dictionary with the access
                          token, refresh token, and token type.
                      2. "access_token": Returns a string value of
                          only the access token.
                      3. "refresh_token": Returns a string value of
                          only the refresh token.
                      4. "token_type": Returns a string value of only
                          the token type.
                      5. "human_readable_time": Returns a string value
                          of the HyperFlex API token file creation time
                          in a human-readable format.
                      6. "unix_timestamp_time": Returns a string value
                          of the HyperFlex API token file creation time
                          in Unix timestamp format.
                      7. "source_module": Returns a string value of
                          the source module used to create the
                          HyperFlex API token file.
                  """
                  )
            return
    except Exception as exception_message:
        print("There was an error loading a HyperFlex API token file: ")
        print("{}".format(str(exception_message)))
        return
        

def manage_token_file(ip,username,password,file_path,data="token",overwrite=True):
    r"""This is a function that creates or loads an XML file containing a
    HyperFlex API token and then validates the loaded token data. If the
    loaded HyperFlex API access token is not valid, a new access token will be
    automatically obtained. If there is a no HyperFlex API token file present
    in the provided file path, a new token file will be automatically created.

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            The value must be a string.
        username: The username credentials that will be used to log into
            HyperFlex. The value must be a string.
        password: The password credentials that will be used to log into
            HyperFlex. The value must be a string.
        file_path: The file name and storage location to write a HyperFlex API
            token file. The value must be a string. An example value is
            "c:\\folder\\file.xml".
        data: (Optional) The data from a HyperFlex API token file that is
            returned by the manage_token_file() function. Providing this
            argument is optional. The default value of "token" is set, which
            returns the access token, refresh token, and token type as a
            dictionary. The user provided value must be a string. See the
            following list for the options available for the 'data' argument
            and the returned value:
                1. "token": Returns a dictionary with the access token,
                    refresh token, and token type.
                2. "access_token": Returns a string value of only the access
                    token.
                3. "refresh_token": Returns a string value of only the
                    refresh token.
                4. "token_type": Returns a string value of only the token
                    type.
                5. "human_readable_time": Returns a string value of the HyperFlex
                    API token file creation time in a human-readable format.
                6. "unix_timestamp_time": Returns a string value of the HyperFlex
                    API token file creation time in Unix timestamp format.
                7. "source_module": Returns a string value of the source
                    module used to create the HyperFlex API token file.
            NOTE: For automatic validation and renewals of HyperFlex API
            tokens to occur, the 'data' argument must be set to "token"
            (default), "access_token", or "refresh_token".
        overwrite: (Optional) The option to overwrite any pre-existing file at
            the provided file path value given to the 'file_path' argument.
            Providing this argument is optional. If the argument is set to the
            Boolean value True, any pre-exiting token file will be
            automatically overwritten. If the argument is set to the Boolean
            value False, the manage_token_file() function will stop and not
            proceed with creating a new token file if a pre-existing token
            file is already in place at the given file path location. The
            default value is True.
            NOTE: For automatic validation and renewals of HyperFlex API
            tokens to occur, the 'overwrite' argument must be set to the
            Boolean value True (default). Setting the 'overwrite' argument to
            the Boolean value False will disable the ability to update
            pre-existing HyperFlex API token files.
        
    Returns:
        The return is based on the value of the 'data' argument. If the default
        value of "token" is set, the access token, refresh token, and token
        type will be returned as a dictionary. See the following list to see
        the options available for the 'data' argument and the returned value:    
            1. "token": Returns a dictionary with the access token, refresh
                token, and token type.
            2. "access_token": Returns a string value of only the access
                token.
            3. "refresh_token": Returns a string value of only the refresh
                token.
            4. "token_type": Returns a string value of only the token type.
            5. "human_readable_time": Returns a string value of the HyperFlex
                API token file creation time in a human-readable format.
            6. "unix_timestamp_time": Returns a string value of the HyperFlex
                API token file creation time in Unix timestamp format.
            7. "source_module": Returns a string value of the source module
                used to create the HyperFlex API token file.

    Raises:
        Exception: An exception occurred while managing the HyperFlex API token
            file. The exact error will be specified.
        ValueError: There was an invalid argument provided for the file path,
            data or overwrite settings. A recommendation on how to resolve the
            error will be displayed.
    """

    # Verify the data argument
    if data not in ("token",
                    "access_token",
                    "refresh_token",
                    "token_type",
                    "human_readable_time",
                    "unix_timestamp_time",
                    "source_module"
                    ):
        raise ValueError("The argument provided for the requested data type "
                         "is not valid. Run 'help(manage_token_file)' for "
                         "available options.")
    
    # Verify the overwrite argument
    if not isinstance(overwrite, bool):
        raise ValueError("The overwrite setting is not valid. Please provide "
                         "a Boolean value of True or False for the "
                         "'overwrite' argument.")
    
    # Start the HyperFlex API token file management process
    print("Starting the HyperFlex API token file management process...")
    # Check for the presence of a pre-existing HyperFlex API token file
    print("Checking for the presence of a pre-existing HyperFlex API token "
          "file...")
    if not os.path.isfile(file_path):
        print("A HyperFlex API token file was not found.")
        # Create a new HyperFlex API token file
        new_hx_api_token_file = create_token_file(
            ip,username,password,file_path)
        # Load the new HyperFlex API token file
        loaded_new_hx_api_token_file = load_token_file(
            new_hx_api_token_file,data)
        print("A valid HyperFlex API token is ready.")
        return loaded_new_hx_api_token_file
    else:
        # Load the pre-existing HyperFlex API token file
        loaded_existing_hx_api_token_file = load_token_file(file_path,data)
        if data in ("token",
                    "access_token",
                    "refresh_token"
                    ):
            # Validate the pre-existing HyperFlex API token file
            print("Moving to validation of the requested {} data...".format(data))
            validate_loaded_existing_hx_api_token_file = validate_token(
                ip,load_token_file(file_path))
            if validate_loaded_existing_hx_api_token_file:
                print("A valid HyperFlex API token is ready.")
                return loaded_existing_hx_api_token_file
            else:
                print("The access token in the pre-existing HyperFlex API "
                      "token file has failed validation.")
                if overwrite:
                    print("The pre-existing HyperFlex API token file will now "
                          "be updated with a new valid token...")
                    # Create a new HyperFlex API token file
                    new_hx_api_token_file = create_token_file(
                        ip,username,password,file_path)
                    # Load the new HyperFlex API token file
                    loaded_new_hx_api_token_file = load_token_file(
                        new_hx_api_token_file,data)
                    print("A valid HyperFlex API token is ready.")
                    return loaded_new_hx_api_token_file
                else:
                    print("The 'overwrite' argument is set to False, so the "
                          "pre-existing HyperFlex API token file will not be "
                          "updated.")
                    print("Exiting.")
                    return
        else:
            print("The pre-exiting HyperFlex API token file has been loaded. It "
                  "has not been validated.")
            print("Set the 'data' argument to 'token', 'access_token' or "
                  "'refresh_token' to enable automatic validation and "
                  "renewals of HyperFlex API tokens.")
            return loaded_existing_hx_api_token_file
