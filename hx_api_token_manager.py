"""
Cisco HyperFlex API Token Manager, v1
Author: Ugo Emekauwa
Contact: uemekauw@cisco.com, uemekauwa@gmail.com
Summary: The Cisco HyperFlex API Token Manager provides the ability to
         automate the creation, validation and renewal of HyperFlex API tokens.
         Basic management of HyperFlex API tokens, including obtain, refresh,
         validate and revoke actions are also available.
Notes: Tested on HyperFlex 4.0(1b) and 4.0(2a).
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

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            The value must be a string.
        username: The username credentials that will be used to log into
            HyperFlex. The value must be a string.
        password: The passsword credentials that will be used to log into
            HyperFlex. The value must be a string.

    Returns:
        A HyperFlex API access token, refresh token and token type that have
        been granted as key-value pairs in a dictionary.

    Raises:
        Exception: There was an error obtaining a HyperFlex API access token.
            The status code or error message will be specified.
    """

    request_headers = {"Content-Type": "application/json"}
    request_url = "https://{}/aaa/v1/auth?grant_type=password".format(ip)
    post_body = {
        "username": username,
        "password": password,
        "client_id": "HxGuiClient",
        "client_secret": "Sunnyvale",
        "redirect_uri": "http://localhost:8080/aaa/redirect"
        }

    try:
        print("Attempting to obtain a HyperFlex API access token...")
        obtain_hx_api_token = requests.post(request_url,
                                            headers=request_headers,
                                            data=json.dumps(post_body),
                                            verify=False
                                            )
        if obtain_hx_api_token.status_code == 201:
            hx_api_token = obtain_hx_api_token.json()
            print("A HyperFlex API access token was sucessfully obtained.")
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
    """This is a function that refreshes a HyperFlex API access token.

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
                AAA (Authorization, Accounting and Authentication). The access
                token is used to authorize users for any API operations. The
                refresh token can be used to obtain a new access token without
                the need to re-provide HyperFlex username and password
                credentials.
            3. "token_type": A token type obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The access
                token is used to authorize users for any API operations. This
                token type value should be of type "Bearer".

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

    # Verify hx_api_token argument
    if not isinstance(hx_api_token, collections.abc.Mapping):
        raise ValueError("The argument provided for the HyperFlex API token "
                         "is not valid. Please provide a valid dictionary "
                         "for the 'hx_api_token' argument.")
    
    request_headers = {"Content-Type": "application/json"}
    request_url = "https://{}/aaa/v1/token?grant_type=refresh".format(ip)
    post_body = {
        "access_token": hx_api_token["access_token"],
        "refresh_token": hx_api_token["refresh_token"],
        "token_type": hx_api_token["token_type"]
        }

    try:
        print("Attempting to refresh the HyperFlex API access token...")
        refresh_hx_api_token = requests.post(request_url,
                                             headers=request_headers,
                                             data=json.dumps(post_body),
                                             verify=False
                                             )
        if refresh_hx_api_token.status_code == 201:
            hx_api_token = refresh_hx_api_token.json()
            print("The HyperFlex API access token was sucessfully refreshed.")
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
                AAA (Authorization, Accounting and Authentication). The access
                token is used to authorize users for any API operations. The
                refresh token can be used to obtain a new access token without
                the need to re-provide HyperFlex username and password
                credentials.
            3. "token_type": A token type obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The access
                token is used to authorize users for any API operations. This
                token type value should be of type "Bearer".
        scope: The scope of the validate access token operation. The value must
            be a string. The options are "READ" or "MODIFY". The default value
            is "READ".

    Returns:
        The boolean value True is returned for a successful validation. The
        boolean value False is returned if the validation fails.

    Raises:
        Exception: There was an error performing the validation of the
            HyperFlex API access token. The status code or error message will
            be specified.
        ValueError: There was an invalid argument provided for the HyperFlex
            API token or desired scope operation. A recommendation on how to
            resolve the error will be displayed.
    """

    # Verify hx_api_token argument
    if not isinstance(hx_api_token, collections.abc.Mapping):
        raise ValueError("The argument provided for the HyperFlex API token "
                         "is not valid. Please provide a valid dictionary "
                         "for the 'hx_api_token' argument.")

    # Verify scope argument
    if scope not in ("READ", "MODIFY"):
        raise ValueError("The argument provided for the scope operation is "
                         "not valid. Please provide either the value 'READ' "
                         "or 'MODIFY' in string format for the 'scope' "
                         "argument.")
    
    request_headers = {"Content-Type": "application/json"}
    request_url = "https://{}/aaa/v1/validate".format(ip)
    post_body = {
        "access_token": hx_api_token["access_token"],
        "scope": scope,
        "token_type": hx_api_token["token_type"]
        }

    try:
        print("Attempting to validate the HyperFlex API access token...")
        validate_hx_api_token = requests.post(request_url,
                                              headers=request_headers,
                                              data=json.dumps(post_body),
                                              verify=False
                                              )
        if validate_hx_api_token.status_code == 200:
            print("The HyperFlex API access token was sucessfully validated.")
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
                AAA (Authorization, Accounting and Authentication). The access
                token is used to authorize users for any API operations. The
                refresh token can be used to obtain a new access token without
                the need to re-provide HyperFlex username and password
                credentials.
            3. "token_type": A token type obtained from the HyperFlex API
                AAA (Authorization, Accounting and Authentication). The access
                token is used to authorize users for any API operations. This
                token type value should be of type "Bearer".

    Returns:
        The boolean value True is returned for a successful revocation. The
        boolean value False is returned if the revocation fails.

    Raises:
        Exception: There was an error performing the revocation of the
            HyperFlex API access token. The status code or error message will
            be specified.
        ValueError: There was an invalid argument provided for the HyperFlex
            API token. A recommendation on how to resolve the error will be
            displayed.
    """

    # Verify hx_api_token argument
    if not isinstance(hx_api_token, collections.abc.Mapping):
        raise ValueError("The argument provided for the HyperFlex API token "
                         "is not valid. Please provide a valid dictionary "
                         "for the 'hx_api_token' argument.")

    request_headers = {"Content-Type": "application/json"}
    request_url = "https://{}/aaa/v1/revoke".format(ip)
    post_body = {
        "access_token": hx_api_token["access_token"],
        "refresh_token": hx_api_token["refresh_token"],
        "token_type": hx_api_token["token_type"]
        }

    try:
        print("Attempting to revoke the HyperFlex API access token...")
        revoke_hx_api_token = requests.post(request_url,
                                            headers=request_headers,
                                            data=json.dumps(post_body),
                                            verify=False
                                            )
        if revoke_hx_api_token.status_code == 200:
            print("The HyperFlex API access token was sucessfully revoked.")
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
    r"""This is a function that creates a HyperFlex API token file.

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            The value must be a string.
        username: The username credentials that will be used to log into
            HyperFlex. The value must be a string.
        password: The passsword credentials that will be used to log into
            HyperFlex. The value must be a string.
        file_path: The file name and storage location to write a HyperFlex API
            token file. The value must be a string. An example value is
            "c:\\folder\\file.xml".
        overwrite: The option to overwrite any pre-exisiting file at the
            provided file path value given to the 'file_path' argument. If the
            value is set to True, any pre-exiting token file will be
            automatically overwritten. If set to False, the create_token_file
            function will stop and not proceed with creating a new token file
            if a pre-existing token file already exists. The default value is
            True.

    Returns:
        The file path of the new HyperFlex API token file in XML format is
        returned if creation was successful. The value None is returned if
        creating a HyperFlex API token file failed.

    Raises:
        Exception: An exception occured while creating a HyperFlex API token
            file. The exact error will be specified.
        ValueError: There was an invalid argument provided for the overwrite
            setting. A recommendation on how to resolve the error will be
            displayed.
    """

    # Verify overwrite argument
    if not isinstance(overwrite, bool):
        raise ValueError("The overwrite setting is not valid. Please provide "
                         "a boolean value of True or False for the "
                         "'overwrite' argument.")
    
    print("Starting the HyperFlex API token file creation process...")
    if not overwrite:
        if os.path.isfile(file_path):
            print("A file already exists at the given file path location. No "
                  "changes have been made.")
            print("To overwrite the pre-exisiting file, set the 'overwrite' "
                  "argument to the boolean value True.")
            return
    hx_api_token = obtain_token(ip,username,password)
    try:
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
        hx_api_token_xml = et.ElementTree(hx_api_token_xml_data)
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
    r"""This is a function that loads data from a HyperFlex API token file.

    Args:
        file_path: The file name and storage location from which to load a
            HyperFlex API token file. The value must be a string. An example
            value is "c:\\folder\\file.xml".
        data: The data from a HyperFlex API token file that is returned by the
            load_token_file() function. The default value of "token" is set,
            which returns the the access token, refresh token, and token type
            as a dictionary. The user provided value must be a string. See the
            following list for the options available for the data argument and
            the returned data:
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
                token file creation time in unix timestamp format.
            7. "source_module": Returns a string value of the source module
                used to create the HyperFlex API token file.
    
    Returns:
        The return is based on the value of the data argument. If the default
        value of "token" is set, the access token, refresh token, and token
        type will be returned as a dictionary. See the following list to see
        the options available for the data argument and the returned value:
            1. "token": Returns a dictionary with the access token, refresh
                token, and token type.
            2. "access_token": Returns a string value of only the access token.
            3. "refresh_token": Returns a string value of only the refresh token.
            4. "token_type": Returns a string value of only the token type.
            5. "human_readable_time": Returns a string value of the HyperFlex
                API token file creation time in a human-readable format.
            6. "unix_timestamp_time": Returns a string value of the HyperFlex
                API token file creation time in unix timestamp format.
            7. "source_module": Returns a string value of the source module
                used to create the HyperFlex API token file.

    Raises:
        Exception: An exception occured while loading the HyperFlex API token
            file. The exact error will be specified.
        ValueError: There was an invalid argument provided for the file path
            or data setting. A recommendation on how to resolve the error will
            be displayed.
    """

    # Verify file_path argument
    if not os.path.isfile(file_path):
        raise ValueError(r"The file at the provided file path does not exist. "
                         "Please provide the file path to a valid file in "
                         "string format for the 'file_path' argument. An "
                         "example value is 'c:\\folder\\file.xml'.")

    # Verify data argument
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

    print("Starting the HyperFlex API token file loading process...")
    # Verify presence of HyperFlex API token file and load data
    print("Verifying the presence of the HyperFlex API token file...")
    try:
        if not os.path.isfile(file_path):
            print("The HyperFlex API token file was not found.")
            return
        else:
            print("The HyperFlex API token file was found, proceding with "
                  "loading data from the file...")
            hx_api_token_xml_data = et.parse(file_path)
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
            print("The requested refresh token data has been returned.")
            return token_type_data
        elif data == "human_readable_time":
            print("The requested human readable time data has been returned.")
            return human_readable_time_data
        elif data == "unix_timestamp_time":
            print("The requested unix timestamp data has been returned.")
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
                      1. 'token': Returns a dictionary with the access
                          token, refresh token, and token type.
                      2. 'access_token': Returns a string value of
                          only the access token.
                      3. 'refresh_token': Returns a string value of
                          only the refresh token.
                      4. 'token_type': Returns a string value of only
                          the token type.
                      5. 'human_readable_time': Returns a string value
                          of the HyperFlex API token file creation time
                          in a human-readable format.
                      6. 'unix_timestamp_time': Returns a string value
                          of the HyperFlex API token file creation time
                          in unix timestamp format.
                      7. 'source_module': Returns a string value of
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
    r"""This is a function that loads data from a HyperFlex API token file and
        then validates the loaded token. If the loaded token is not valid, a
        new token will be obtained. If there is a no token file present in the
        provided file path, a new token file will be created.

    Args:
        ip: The targeted HyperFlex Connect or Cluster Management IP address.
            Setting the ip, username, and password arguments will enable the
            manage_token_file() function to automatically generate a new
            HyperFlex API token and accompanying token file if the current
            token is expired or if the user provided file path is missing the
            token file. The default value is None. The user provided value
            must be a string.
        username: The username credentials that will be used to log into
            HyperFlex. Setting the ip, username, and password arguments will
            enable the manage_token_file() function to automatically generate
            a new HyperFlex API token and accompanying token file if the
            current token is expired or if the user provided file path is
            missing the token file. The default value is None. The user
            provided value must be a string.
        password: The passsword credentials that will be used to log into
            HyperFlex. Setting the ip, username, and password arguments will
            enable the manage_token_file() function to automatically generate
            a new HyperFlex API token and accompanying token file if the
            current token is expired or if the user provided file path is
            missing the token file. The default value is None. The user
            provided value must be a string.
        file_path: The file name and storage location to write a HyperFlex API
            token file. The value must be a string. An example value is
            "c:\\folder\\file.xml".
        data: The data from a HyperFlex API token file that is returned by the
            manage_token_file() function. The default value of "token" is set,
            which returns the the access token, refresh token, and token type
            as a dictionary. The user provided value must be a string. See the
            following list for the options available for the data argument and
            the returned data:
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
                    API token file creation time in unix timestamp format.
                7. "source_module": Returns a string value of the source
                    module used to create the HyperFlex API token file.
        overwrite: The option to overwrite any pre-exisiting file at the
            provided file path value given to the 'file_path' argument. If the
            value is set to True, any pre-exiting token file will be
            automatically overwritten. If set to False, the manage_token_file
            function will stop and not proceed with creating a new token file
            if a pre-existing token file already exists. The default value is
            True.
        
    Returns:
        The return is based on the value of the data argument. If the default
        value of "token" is set, the access token, refresh token, and token
        type will be returned as a dictionary. See the following list to see
        the options available for the data argument and the returned value:    
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
                API token file creation time in unix timestamp format.
            7. "source_module": Returns a string value of the source module
                used to create the HyperFlex API token file.

    Raises:
        Exception: An exception occured while managing the HyperFlex API token
            file. The exact error will be specified.
        ValueError: There was an invalid argument provided for the file path,
            data or overwrite settings. A recommendation on how to resolve the
            error will be displayed.
    """

    # Verify data argument
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
    
    # Verify overwrite argument
    if not isinstance(overwrite, bool):
        raise ValueError("The overwrite setting is not valid. Please provide "
                         "a boolean value of True or False for the "
                         "'overwrite' argument.")
    
    print("Starting the HyperFlex API token file managing process...")
    # Check for presence of HyperFlex API token file
    print("Checking for the presence of a HyperFlex API token file...")
    if not os.path.isfile(file_path):
        print("A HyperFlex API token file was not found.")
        # Create HyperFlex API token file
        new_hx_api_token_file = create_token_file(ip,username,password,file_path)
        loaded_new_hx_api_token_file = load_token_file(new_hx_api_token_file,data)
        print("A valid HyperFlex API token is ready.")
        return loaded_new_hx_api_token_file
    else:
        loaded_existing_hx_api_token_file = load_token_file(file_path,data)
        if data in ("token",
                    "access_token",
                    "refresh_token"
                    ):
            validate_loaded_existing_hx_api_token_file = validate_token(
                ip,loaded_existing_hx_api_token_file)
            if validate_loaded_existing_hx_api_token_file:
                print("A valid HyperFlex API token is ready.")
                return loaded_existing_hx_api_token_file
            else:
                print("The access token in the pre-existing HyperFlex API "
                      "token file has failed validation.")
                if overwrite:
                    print("The pre-existing HyperFlex API token file will now "
                          "be updated with a new valid token...")
                    new_hx_api_token_file = create_token_file(
                        ip,username,password,file_path)
                    loaded_new_hx_api_token_file = load_token_file(
                        new_hx_api_token_file,data)
                    print("A valid HyperFlex API token is ready.")
                    return loaded_new_hx_api_token_file
                else:
                    print("The overwrite argument is set to False, so the "
                          "pre-exisiting HyperFlex API token file will not be "
                          "updated.")
                    print("Exiting.")
                    return
        else:
            print("A pre-exiting HyperFlex API token file has been loaded. It "
                  "has not been validated.")
            print("Set the 'data' argument to 'token', 'access_token' or "
                  "'refresh_token' to enable automatic validation.")
            return loaded_existing_hx_api_token_file
