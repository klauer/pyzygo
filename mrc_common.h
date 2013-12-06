/// \file mrc_common.h
/// Header file containing defined constants that are common to MRC client programs and MetroPro.

#ifndef MRC_COMMON_INCLUDED
#define MRC_COMMON_INCLUDED

	/// \defgroup server_state_codes Server State Codes
	/// Codes indicating the state of the server MetroPro.
	/// MetroPro has no real "connected-to-a-client" state.
	/// It simply executes remote commands one at a time from one or more clients.
	/// Between commands, client programs can be stopped and started at will.
	/// There are three fundamental MetroPro states associated with acting as a server:
	/// STOPPED, IDLE and ACTIVE.
	/*@{*/
	/// Integer code for the UNKNOWN server state.
#define MRC_SERVER_STATE_UNKNOWN					-1

	/// Integer code for the STOPPED server state.
	/// STOPPED is the normal initial state.
	/// In the STOPPED state:
	/// - The MetroPro GUI appears normal and responds normally to the operator.
	/// - MetroPro is not acting as a server; it is not listening for remote commands.
	/// - A potential client gets an error if it tries to issue a remote command.
	/// - If MRC is enabled, the F11 hot key causes a transition to the IDLE state.
	/// .
#define MRC_SERVER_STATE_STOPPED					0

	/// Integer code for the IDLE server state.
	/// In the IDLE state:
	/// - The MetroPro main window title is set to: MetroPro – Remote Control – Idle
	/// - The MetroPro GUI reponds normally to the operator.
	/// - MetroPro accepts and executes remote commands, if no other operation is pending. See note 1 below.
	/// - Certain remote commands causes a transition to the ACTIVE state.
	/// - The F11 hot key causes a transition to the ACTIVE state.
	/// - The Ctrl-F11 hot key combination causes a transition back to the STOPPED state.
	/// .
	/// MetroPro can be configured to automatically enter the IDLE state at startup.
#define MRC_SERVER_STATE_IDLE						1

	/// Integer code for the ACTIVE server state.
	/// In the ACTIVE state:
	/// - The MetroPro main window title is set to: MetroPro – Remote Control – Active
	/// - MetroPro is nominally “remote controlled”.
	/// - MetroPro accepts and executes remote commands.
	/// - The MetroPro GUI displays the hour-glass cursor and ignores operator input, except for the Esc or Ctrl-C key or Window Close.
	/// - The Esc key has two effects: abort a Script command or cause a transition back to the IDLE state. See note 2 below.
	/// - Either the Ctrl-C key combination or clicking the Window Close icon generates the “Do you want to Quit?” dialog.
	/// - A remote command can request a transition back to the IDLE state.
	/// .
	/// Note 1:\n
	/// In the IDLE state, MetroPro can only accept a remote command if no operator-initiated processing is pending.
	/// Examples of such processing include: performing a measurement, running a script, waiting for the operator to respond to a dialog.\n
	/// Note 2:\n
	/// In the ACTIVE state, if the Esc key is pressed while a Script command is being executed, the script is aborted
	/// (unless “on error” handling prevents it).
	/// If the script is aborted, the message “Processing aborted” is returned as output to the client.
	/// If the Esc key is pressed while waiting for a remote command, it causes a transition back to the IDLE state.
#define MRC_SERVER_STATE_ACTIVE						2
	/*@}*/

	/// Invalid handle value.
#define MRC_INVALID_HANDLE	-1

	/// Size of the characters arrays that receive script output returned by MetroPro to a client.
#define MRC_SCRIPT_OUTPUT_BUFSIZ					512

	/// \defgroup script_context_codes Script Context Codes
	/// A script can be executed by MetroPro in either of two contexts.
	/// A script can be executed by MetroPro in either of two contexts:
	/// - The desktop (outside of any loaded app) or
	/// - The front-most open app
	/// .
	/// \remarks
	/// In order to perform an operation such as switching apps, a script must run in the context of the MetroPro desktop.\n
	/// In order to perform an operation involving an instrument, a script must run in the context of the MetroPro front-most open app.
	/*@{*/
	/// Integer code to specify that a script is to run in the context of the MetroPro desktop.
#define MRC_SCRIPT_CONTEXT_DESKTOP					0
	/// Integer code to specify that a script is to run in the context of the MetroPro front-most open app.
#define MRC_SCRIPT_CONTEXT_FRONTMOST_APP			1
	/*@}*/

	/// \defgroup error_codes Error Codes
	/// Error codes returned by MRC client DLL functions.
	/// Many of the MRC client DLL functions return integer error codes.
	/// In the case of the mrc5_client DLL (a .NET assembly),
	/// most of the functions throw structured exceptions instead of returning error codes.
	/// \cond mrc5_exceptions
	/// \sa group_mrc5_exceptions
	/// \endcond
	/// A return value of zero indicates success; a return value of non-zero indicates failure. 
	/// Values greater than or equal to \ref MRC_ERR_BASE are defined here; other values are defined in winerror.h.
	/*@{*/
	/// No error occurred.
	/// This return code indicates that no error occurred.
#define MRC_ERR_NONE								0

	/// Error return code base value.
	/// This is the base value for error codes returned by the MRC client DLL functions.
	/// The functions may return lower error code values defined in winerror.h.
#define MRC_ERR_BASE								0x20000000

	/// A run-script command failed.
	/// A run-script command failed.
	/// This code indicates that either a script could not be run,
	/// or the script ran but exited with an error.
#define MRC_ERR_RUN_SCRIPT_FAILED					0x20000000

	/// MetroPro is busy executing a remote command.
	/// MetroPro is busy executing a remote command.
	/// This code indicates that MetroPro cannot accept a remote command
	/// because it is busy executing a previous remote command.
	/// MetroPro can only accept one remote command at a time.
#define MRC_ERR_SERVER_BUSY							0x20000001

	/// MetroPro could not accept a command within a time limit.
	/// MetroPro could not accept a command within a time limit.
	/// This error can occur when MetroPro is in the MRC_SERVER_STATE_IDLE state and a user-initiated operation is pending.
	/// This error cannot occur when MetroPro is in the MRC_SERVER_STATE_ACTIVE state.
#define MRC_ERR_COMMAND_TIMEOUT						0x20000002

	/// MetroPro could not transition from the MRC_SERVER_STATE_IDLE state
	/// to the MRC_SERVER_STATE_ACTIVE state.
	/// MetroPro could not transition from the MRC_SERVER_STATE_IDLE state
	/// to the MRC_SERVER_STATE_ACTIVE state.
#define MRC_ERR_REQUEST_CONTROL_FAILED				0x20000003

	/// MetroPro could not transition from the MRC_SERVER_STATE_ACTIVE state
	/// to the MRC_SERVER_STATE_IDLE state.
	/// MetroPro could not transition from the MRC_SERVER_STATE_ACTIVE state
	/// to the MRC_SERVER_STATE_IDLE state.
#define MRC_ERR_RELEASE_CONTROL_FAILED				0x20000004

	/// MetroPro could not run a script because there is no open app.
	/// MetroPro could not run a script because there is no open app.
	/// This error occurs if \ref MRC_SCRIPT_CONTEXT_FRONTMOST_APP is specified as the script context but there is no app open.
#define MRC_ERR_SCRIPT_CONTEXT_NO_APP				0x20000005

	/// A passed parameter value is invalid.
	/// A passed parameter value is invalid.
#define MRC_ERR_INVALID_PARAM						0x20000006

	/// MetroPro could not write a required temporary file.
	/// MetroPro could not write a required temporary file.
#define MRC_ERR_CANT_WRITE_TEMP_FILE				0x20000007

	/// The passed handle value is invalid.
	/// The passed handle value is invalid.
#define MRC_ERR_INVALID_HANDLE						0x20000008

	/// The client RPC binding could not be created.
	/// The client RPC binding could not be created.
#define MRC_ERR_RPC_BINDING_CREATE					0x20000009

	/// The client RPC binding could not be freed.
	/// The client RPC binding could not be freed.
#define MRC_ERR_RPC_BINDING_FREE					0x2000000A

	/// A memory allocation failed.
	/// A memory allocation failed.
#define MRC_ERR_NO_MEM								0x2000000B

	/// The client interface is busy.
	/// The client interface is busy.
	/// The requested operation is not allowed if the client interace is busy.
#define MRC_ERR_CLIENT_INTERFACE_BUSY				0x2000000C

	/// The client interface is already open.
	/// The client interface is already open.
	/// The requested operation is not allowed if the client interface is already open.
#define MRC_ERR_CLIENT_INTERFACE_OPEN				0x2000000D

	/// The client interface is not open.
	/// The client interface is not open.
	/// The requested operation is not allowed if the client interface is not open.
#define MRC_ERR_CLIENT_INTERFACE_NOT_OPEN			0x2000000E

	/// No script filename or text was specified.
	/// No script filename or text was specified.
#define MRC_ERR_NO_SCRIPT_FILENAME_OR_TEXT			0x2000000F

	/// A log file could not be created.
	/// A log file could not be created.
#define MRC_ERR_CANT_CREATE_LOG_FILE				0x20000010

	/// Timeout waiting for the interface to become idle.
	/// Timeout waiting for the interface to become idle.
#define MRC_ERR_TIMEOUT_WAITING_FOR_IDLE			0x20000011

	/// Timeout waiting for script done.
	/// Timeout waiting for script done.
#define MRC_ERR_TIMEOUT_WAITING_FOR_SCRIPT			0x20000012
	/*@}*/

	/// \defgroup enable_status_callback_bitmasks Enable Status Callback Bitmasks
	/// Integer bitmasks used to specify which status callbacks are required.
	/// While MetroPro is running a script, the client program can receive status callbacks
	/// that indicate progress of the script or the status of MetroPro.
	/// These integer bitmasks are used to specify which status callbacks are required.
	/// The values can be combined using a bit-wise-OR.
	/// \sa callback_status_codes
	/*@{*/
	/// Bitmask value to enable a callback when acquisition begins.
#define MRC_ENABLE_STATUS_CALLBACK_BEGIN_ACQUIRE	0x0001
	/// Bitmask value to enable a callback when acquisition ends.
#define MRC_ENABLE_STATUS_CALLBACK_END_ACQUIRE		0x0002
	/// Bitmask value to enable a callback when FDA begins.
#define MRC_ENABLE_STATUS_CALLBACK_BEGIN_FDA		0x0004
	/// Bitmask value to enable a callback when FDA ends.
#define MRC_ENABLE_STATUS_CALLBACK_END_FDA			0x0008
	/// Bitmask value to enable a callback by MetroScript "mrcstatus".
#define MRC_ENABLE_STATUS_CALLBACK_SCRIPT			0x0010
	/// Bitmask value to enable a callback when the script is done executing.
#define MRC_ENABLE_STATUS_CALLBACK_END_SCRIPT		0x0020
	/// Bitmask value to enable a callback containing the scan offset.
#define MRC_ENABLE_STATUS_CALLBACK_SCAN_OFFSET		0x0040
	/// Bitmask value to enable all callbacks.
#define MRC_ENABLE_STATUS_CALLBACK_ALL				0xFFFF
	/// Bitmask value to disable all callbacks.
#define MRC_ENABLE_STATUS_CALLBACK_NONE				0x0000
	/*@}*/

	/// \defgroup callback_status_codes Callback Status Codes
	/// Codes passed to status callback function.
	/// While MetroPro is running a script, the client program can receive status callbacks
	/// that indicate progress of the script or the status of MetroPro.
	/// If the client progam is written using a .NET language and the mrc5_client DLL, callbacks generate events.
	/// For other languages, the client program must register a callback function.
	/// Callbacks are not supported for the VB6 language.\n
	/// These integer codes are passed to the callback function to indicate the status.\n
	/// The client program must also enable one or more callbacks by specifying an integer bitmask.
	/// \sa enable_status_callback_bitmasks
	/*@{*/
	/// Beginning of acquisition.
#define MRC_CALLBACK_STATUS_BEGIN_ACQUIRE			1
	/// End of acquisition.
#define MRC_CALLBACK_STATUS_END_ACQUIRE				2
	/// Beginning of FDA.
#define MRC_CALLBACK_STATUS_BEGIN_FDA				3
	/// End of FDA.
#define MRC_CALLBACK_STATUS_END_FDA					4
	/// End of script execution.
#define MRC_CALLBACK_STATUS_END_SCRIPT				5
	/*@}*/

#endif
