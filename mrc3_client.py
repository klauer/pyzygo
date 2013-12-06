from ctypes import *

# Callback function type.
# While running a script for a remote client, a server can call back to the client to indicate a status change.
# This typedef specifies the prototype for the callback function.
# \param callback_id
# Input: integer equal to the value passed to function mrc3_run_script().
# \param status
# Input: integer, one of the MRC_CALLBACK_STATUS_XXX status codes defined in mrc_common.h.
# \sa mrc3_set_status_callback_function().
mrc3_callback_type = WINFUNCTYPE(None, c_int, c_int)

# Opens a diagnostic log file.
# This function opens a log file to receive diagnostic messages.
# Overwrites any existing file of the same name.
# \param pathname
# Input: specifies the file path.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# Only a single log file is supported.
mrc3_open_log_file = WINFUNCTYPE(c_int, c_char_p)

# Closes a diagnostic log file.
# This function closes the diagnostic log file that was opened by OpenLogFile().
mrc3_close_log_file = WINFUNCTYPE(None)

# Writes a message to a diagnostic log file.
# This function writes a message to a diagnostic log file that was opened by OpenLogFile().
# This function does nothing if there is no open log file.
mrc3_log_message = WINFUNCTYPE(None, c_char_p)

# Get the GUID (Globally Unique Identifier) for the RPC interface.
# \param result
# Output: char array to receive the GUID string.
# \param size
# Input: Size of result[] array.\n
# This function gets a string representation of the GUID (Globally Unique Identifier) for the RPC interface.
# For successful communication with MetroPro, the GUID must match MetroPro's GUID.
# This is useful as a diagnostic to determine if the client DLL version and the MetroPro version are compatible.
mrc3_get_interface_guid = WINFUNCTYPE(None, c_char_p, c_int)

# Create a new interface for communication with a server.
# \param handle
# Output: Integer handle for the new interface.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# This function creates a new interface for communication with a server.
# The output is a handle that is a required input parameter to most of the functions in this DLL.
# Therefore this is normally the first function a client program should call.
# Note that this function does not perform any communication with a server.
# Before the interface can be used to communicate with a server, function
# mrc3_open_interface() must be called.\n
# \remarks
# This function allocates memory associated with the handle.
# When the interface is no longer needed, the client program should call function mrc3_free_interface().\n
# This function fails if:
# - The handle is a NULL pointer.
# - Memory could not be allocated.
mrc3_new_interface = WINFUNCTYPE(c_int, POINTER(c_int))

# Free an interface previously created by function mrc3_new_interface().
# \param handle
# Input/Output: Integer handle obtained from function mrc3_new_interface().
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# This function frees an interface that was created by function mrc3_new_interface().
# It closes the interface if it was open and frees associated memory.
# The handle is set to MRC_INVALID_HANDLE.
# \remarks
# When an interface is no longer needed, the client program should call this function
# to free associated memory.
# This function fails if:
# - The handle is a NULL pointer.
# - The handle is invalid.
mrc3_free_interface = WINFUNCTYPE(c_int, POINTER(c_int))

# Set interface parameters for communication with a server.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param protocol_sequence
# Input: string specifying a communication protocol, typically "ncalrpc" or "ncacn_ip_tcp".
# This parameter cannot be NULL or an empty string.
# \param network_address 
# Input string identifying the server computer.
# Pass NULL or an empty string when using the ncalrpc protocol.
# Otherwise, specify the host name or IP address as a string.
# \param end_point
# Input: string specifying the server end point.
# This parameter cannot be NULL or an empty string.
# Use "localhost" with the ncalrpc protocol.
# Specify a port number (e.g. "5000") when using the ncacn_ip_tcp protocol.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# This function opens an interface for communication with a server.
# This function must be called before an interface can be use to communicate with a server.
# Note that this function does not perform any communication with the server.\n
# This function fails if:
# - The handle is invalid.
# - The interface parameters are invalid or inconsistent.
# .
mrc3_set_interface_params = WINFUNCTYPE(c_int, c_int, c_char_p, c_char_p,  c_char_p)

# Ping a server.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# This function performs a do-nothing call to a server.
# An error is generated if the server is not responsive.
# This function is useful to test whether the server is available.\n
# This function fails if:
# - The handle is invalid.
# - The server MetroPro is not available.
# - There is a communication error.
# .
mrc3_ping_server = WINFUNCTYPE(c_int, c_int)

# Request control of a server.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# This function requests that the server enter the \ref MRC_SERVER_STATE_ACTIVE state,
# which is the nominal "remote controlled" state.
# In this state, MetroPro ignores operator input (except for the Esc key).
# An error is generated if the server is not available or if it cannot transition to \ref MRC_SERVER_STATE_ACTIVE.
# No error is generated if the server is already in the \ref MRC_SERVER_STATE_ACTIVE state.\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# - The server MetroPro is not available.
# - There is a communication error.
# - MetroPro cannot transition to the active state.
# .
mrc3_request_control = WINFUNCTYPE(c_int, c_int)

# Release control of a server.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# This function requests that the server return to the \ref MRC_SERVER_STATE_IDLE state.
# In this state, MetroPro responds normally to the operator while continuing to listen for remote commands.
# An error is generated if the server is not available or if it cannot transition to \ref MRC_SERVER_STATE_IDLE.
# No error is generated if the server is already in the \ref MRC_SERVER_STATE_IDLE state.\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# - The server MetroPro is not available.
# - There is a communication error.
# .
mrc3_release_control = WINFUNCTYPE(c_int, c_int)

# Get the state of a server.
# \param handle
# Input: Integer handle obtained from function mrc3_new_interface().
# \param result
# Output: Integer state code.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# This function gets the current state of a server, either \ref MRC_SERVER_STATE_IDLE or \ref MRC_SERVER_STATE_ACTIVE.
# An error is generated if the server is not available.\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# - The server MetroPro is not available.
# - There is a communication error.
# .
mrc3_get_server_state = WINFUNCTYPE(c_int, c_int, POINTER(c_int))

# Sets a script filename.
# This function sets the name of a MetroScript file that can be subsequently run by the server MetroPro.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param filename
# Input: Name of a MetroScript file that exists on the server computer.
# This parameter may be NULL or an empty string.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# Either this function or mrc3_set_script_text() must be called before calling mrc3_run_script()
# or mrc3_start_script().\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# .
mrc3_set_script_filename = WINFUNCTYPE(c_int, c_int, c_char_p)

# Sets script text.
# This function sets MetroScript text that can be subsequently run by the server MetroPro.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param text
# Input: MetroScript text of arbitrary length.
# This parameter may be NULL or an empty string.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# Either this function or mrc3_set_script_filename() must be called before calling mrc3_run_script()
# or mrc3_start_script().\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# .
mrc3_set_script_text = WINFUNCTYPE(c_int, c_int, c_char_p)

# Sets the script context.
# This function sets the context in which a script will run.
# A script can run in the context of the MetroPro desktop (the default) or in the context of the front-most app.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param context
# Input: integer code, one of the \ref script_context_codes defined in \ref mrc_common.h.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# The default value is \ref MRC_SCRIPT_CONTEXT_FRONTMOST_APP.\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# .
mrc3_set_script_context = WINFUNCTYPE(c_int, c_int, c_int)

# Assigns a status callback function.
# This function assigns a function that can be called to indicate a change
# in the status of the server MetroPro while it is running a script for the client.
# Use of a status callback function is optional.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param function
# Input: Pointer to a function or NULL.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# To utilize status callbacks, it is also necessary to call mrc3_set_status_callback_mask().\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# .
# \sa mrc3_set_status_callback_mask() and mrc3_set_status_callback_id().
mrc3_set_status_callback_function = WINFUNCTYPE(c_int, c_int, POINTER(mrc3_callback_type))

# Enables or disables specific callbacks.
# While running a script for a client, a server can call back to the client to indicate a status change.
# This function specifies which status callbacks are required.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param bitmask
# Input: The logical OR of bits specified by the \ref enable_status_callback_bitmasks defined in \ref mrc_common.h.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# To utilize status callbacks, it is also necessary to call mrc3_set_status_callback_function().\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# .
mrc3_set_status_callback_mask = WINFUNCTYPE(c_int, c_int, c_int)

# Sets a status callback ID.
# This function assigns an integer value that will be passed to the
# status callback function.
# Use of a callback ID is optional.
# The value can be used by the callback function to identify the context
# if a client program is receiving callbacks from multiple servers.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param callback_id
# Input: Any integer value.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# .
# \sa mrc3_set_status_callback_function() and mrc3_set_status_callback_mask().
mrc3_set_status_callback_id = WINFUNCTYPE(c_int, c_int, c_int) 

# Runs a script on the server.
# This function causes the server MetroPro to start running a script and
# optionally waits for completion.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param wait_done
# Input: If wait_done is true, this function blocks the calling thread
# until the script is done running.
# If wait_done is false, this function starts the script running and returns.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# Before calling this function or mrc3_start_script(), either mrc3_set_script_filename() or
# mrc3_set_script_text() must have been called.\n
# If mrc3_set_script_filename() was called (passing a non-null script filename),
# then the script to be run is specified to the server as a filename.
# It refers to a file that exists on the server.\n
# Otherwise, if mrc3_set_script_text() was called (passing a non-null script text),
# then the script to be run is specified to the server as text.
# The text, which can be of arbitrary length, is transmitted from the client to the server
# each time the script is run.\n
# The script filename takes precedence if both mrc3_set_script_filename() and mrc3_set_script_text() were called.\n
# This function fails if:
# - The handle is invalid.
# - The client interface is not idle.
# - Both script text and filename are null.
# - The server MetroPro is not available.
# - There is a communication error.
# - MetroPro cannot transition to the active state.
# .
# \sa
# mrc3_start_script()
mrc3_run_script = WINFUNCTYPE(c_int, c_int, c_bool)

# Starts a script on the server.
# This function causes the server MetroPro to start running a script without waiting for completion.
# Equivalent to calling mrc3_run_script(false).
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# See the remarks for function mrc3_run_script().
mrc3_start_script = WINFUNCTYPE(c_int, c_int)

# Tests if the interface is currently running a script.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param result
# Output: 1 if a script is running, 0 if not.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# This function fails if:
# - The handle is invalid.
# .
mrc3_get_script_running = WINFUNCTYPE(c_int, c_int, POINTER(c_int))

# Waits until the client interface is idle.
# An idle client interface is neither running a script nor is in use by another thread.
# This function blocks the calling thread until the client interface is idle or
# the specified timeout period has elapsed.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param timeout_millisecs
# Input: Timeout period in milliseconds. If timeout_millisecs <= 0, the effective timeout is infinite.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# This function fails if:
# - The handle is invalid.
# - The timeout period is exceeded.
# .
mrc3_wait_idle = WINFUNCTYPE(c_int, c_int, c_int)

# Gets the error code from the last script run.
# \param handle
# Input: Integer handle obtained from function mrc3_new_interface().
# \param result
# Output: Integer error code resulting from the last script run.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# This function fails if:
# - The client interface is not idle.
# .
mrc3_get_script_error = WINFUNCTYPE(c_int, c_int, POINTER(c_int))

# Gets the text output from the last script run.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param result
# Output: char array to receive the text output by the script.
# \param size
# Input: Size of result[] array.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# This function fails if:
# - The client interface is not idle.
# .
mrc3_get_script_output = WINFUNCTYPE(c_int, c_int, c_char_p, c_int)

# Gets the stop string value from the last script run.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param result
# Output: char array to receive the stop string value from the script.
# \param size
# Input: Size of result[] array.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# This function fails if:
# - The client interface is not idle.
# .
# \sa script_stop_values
mrc3_get_script_stop_str_val = WINFUNCTYPE(c_int, c_int, c_char_p, c_int)

# Gets the stop numeric value from the last script run.
# \param handle
# Input: integer handle obtained from function mrc3_new_interface().
# \param result
# Output: double to receive the stop numeric value from the script.
# \return
# If successful, returns zero. Otherwise, returns a non-zero error code. See \ref error_codes.\n
# \remarks
# This function fails if:
# - The client interface is not idle.
# .
# \sa script_stop_values
mrc3_get_script_stop_num_val = WINFUNCTYPE(c_int, c_int, POINTER(c_double)) # NOTE: pointer wasn't specified?

# Get a message string corresponding to an error code.
# \param err
# Input: integer error code, e.g. a value returned by one of the functions in this DLL.
# \param result
# Output: char array to receive the message string.
# \param size
# Input: Size of result[] array.\n
# This function gets a message string corresponding to an integer error code.
mrc3_get_error_message = WINFUNCTYPE(None, c_int, c_char_p, c_int)

__all__ = [
    # callback type
    'mrc3_callback_type',

    # startup / cleanup
    'mrc3_get_interface_guid',
    'mrc3_new_interface',
    'mrc3_free_interface',
    'mrc3_set_interface_params',
    'mrc3_ping_server',

    # control
    'mrc3_request_control',
    'mrc3_release_control',
    'mrc3_wait_idle',

    # status
    'mrc3_get_server_state',
    'mrc3_get_error_message',

    # scripts
    'mrc3_set_script_filename',
    'mrc3_set_script_text',
    'mrc3_set_script_context',
    'mrc3_run_script',
    'mrc3_start_script',
    'mrc3_get_script_error',
    'mrc3_get_script_output',
    'mrc3_get_script_stop_str_val',
    'mrc3_get_script_stop_num_val',
    'mrc3_get_script_running',

    # callbacks
    'mrc3_set_status_callback_function',
    'mrc3_set_status_callback_mask',
    'mrc3_set_status_callback_id',

    # logging: (useless)
    'mrc3_open_log_file',
    'mrc3_close_log_file',
    'mrc3_log_message',

    ]
