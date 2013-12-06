"""
zygo mrc3 python interface
"""

from __future__ import print_function
import ctypes
import time
import os

import mrc_common
import mrc3_client
import _mrc3_callbacks

class MRC3ClientError(Exception): pass
class MRC3ClientNotInitializedError(MRC3ClientError): pass
class MRC3ClientScriptError(MRC3ClientError): pass
class MRC3Client(object):
    BUFSIZE = 512
    def __init__(self, path='.', dllname='mrc3_client.dll',
                 user=None, password=None, end_point='localhost', 
                 host='', protocol='ncalrpc', connect=True,
                 debug=False, callbacks=True, callback_mask=None):
        self._handle = None
        self._debug = debug
        self._callbacks = {
            mrc_common.MRC_ENABLE_STATUS_CALLBACK_BEGIN_ACQUIRE : [self.acquire_started],
            mrc_common.MRC_ENABLE_STATUS_CALLBACK_END_ACQUIRE : [self.acquire_ended],
            mrc_common.MRC_ENABLE_STATUS_CALLBACK_BEGIN_FDA : [self.fda_started],
            mrc_common.MRC_ENABLE_STATUS_CALLBACK_END_FDA : [self.fda_ended],
            mrc_common.MRC_ENABLE_STATUS_CALLBACK_SCRIPT : [self.script_started],
            mrc_common.MRC_ENABLE_STATUS_CALLBACK_END_SCRIPT : [self.script_ended],
            mrc_common.MRC_ENABLE_STATUS_CALLBACK_SCAN_OFFSET : [self.scan_offset],
        }

        self._dll = ctypes.CDLL(os.path.join(path, dllname))
        kernel32 = ctypes.windll.kernel32
        def wrap_function(name, function):
            def do_function(*args):
                if self._debug: print('* calling %s%s' % (name, tuple(args)), end=': ')
                ret = function(*args)
                if self._debug: print('<- returned: %s' % ret)
                if name != 'get_error_message':
                    if isinstance(ret, int) and ret != mrc_common.MRC_ERR_NONE:
                        msg = self.get_error_message(ret)
                        raise MRC3ClientError('Error code %x: %s' % (ret, msg))
                return ret

            return do_function

        for name in mrc3_client.__all__:
            function = getattr(mrc3_client, name)
            if self._debug:
                pass
                #print(name, function)
            if hasattr(function, '__call__'):
                addr = kernel32.GetProcAddress(self._dll._handle, name)
                if name.startswith('mrc3_'):
                    name = name[5:]

                setattr(self, '_%s' % name, wrap_function(name, function(addr)))

        if connect:
            self.open_(user=user, password=password, end_point=end_point,
                     host=host, protocol=protocol)

        if callbacks:
            self.enable_callbacks(mask=callback_mask)

    def run_script(self, script_filename='', script_text='', wait_done=True,
                   callback=None, poll_completion=False, poll_rate=0.1):
        self._check_handle()

        if script_text:
            self._set_script_filename(self._handle, '')
            self._set_script_text(self._handle, str(script_text))
        elif script_filename:
            self._set_script_text(self._handle, '')
            self._set_script_filename(self._handle, str(script_filename))

        if wait_done:
            if poll_completion:
                self._run_script(self._handle, False)
                while self.script_running:
                    time.sleep(poll_rate)
            else:
                self._run_script(self._handle, True) # TODO
                #self._run_script(self._handle, False)
                #time.sleep(1)
        elif callback:
            # TODO
            self._run_script(self._handle, False)

        err, err_str = self.script_error
        if err != mrc_common.MRC_ERR_NONE:
            raise MRC3ClientScriptError('Error code %x: %s' % (err, err_str))

        buf = self._create_buffer()
        self._get_script_output(self._handle, buf, self.BUFSIZE)
        return buf.value

    @property
    def interface_guid(self):
        guid = self._create_buffer()
        self._get_interface_guid(guid, self.BUFSIZE)
        return guid.value

    @property
    def script_stop_float(self):
        return self.get_script_stop_value()

    @property
    def script_stop_str(self):
        return self.get_script_stop_value(str)

    def get_script_stop_value(self, type_=float):
        self._check_handle()

        if type_ == float:
            val = ctypes.c_double()
            self._get_script_stop_num_val(self._handle, ctypes.byref(val))
        else:
            val = self._create_buffer()
            self._get_script_stop_str_val(self._handle, val, self.BUFSIZE)

        return val.value
        
    def _create_buffer(self, size=BUFSIZE):
        return ctypes.create_string_buffer(size)

    def request_control(self):
        return self._request_control(self._handle)

    def release_control(self):
        return self._release_control(self._handle)

    def _check_handle(self):
        if self._handle is None:
            raise MRC3ClientNotInitializedError()

    @property
    def script_error(self):
        self._check_handle()

        err = ctypes.c_int()
        self._get_script_error(self._handle, ctypes.byref(err))
        return err.value, self.get_error_message(err)

    def get_error_message(self, errno):
        self._check_handle()

        buf = self._create_buffer()
        self._get_error_message(errno, buf, self.BUFSIZE)
        return buf.value

    @property
    def script_running(self):
        running = ctypes.c_int()
        self._get_script_running(self._handle, ctypes.byref(running))
        return (running.value == 1)

    @property
    def state(self):
        state = ctypes.c_int()
        self._get_server_state(self._handle, ctypes.byref(state))
        return state.value

    def open_(self, user=None, password=None, end_point='localhost', 
                 host='', protocol='ncalrpc'):
        self._handle = ctypes.c_int()
        self._new_interface(ctypes.byref(self._handle))
        
        if self._handle == mrc_common.MRC_INVALID_HANDLE:
             raise MRC3ClientError('Invalid handle returned')

        self._set_interface_params(self._handle, protocol, host, end_point)
        return self._ping_server(self._handle)

    def log(self, text, filename='test.log', open_close=True):
        # NOTE: no real reason to use this that I can see. Just use Python's
        # file handling. Also, note that _open_log_file does not append.
        if open_close:
            self._open_log_file(filename)

        try:
            self._log_message(text)
        finally:
            if open_close:
                self._close_log_file()

    def acquire_started(self, id_):
        if self._debug:
            print('acquire started', id_)

    def acquire_ended(self, id_):
        if self._debug:
            print('acquire ended', id_)

    def fda_started(self, id_):
        if self._debug:
            print('fda started', id_)

    def fda_ended(self, id_):
        if self._debug:
            print('fda ended', id_)

    def script_started(self, id_):
        if self._debug:
            print('script started', id_)

    def script_ended(self, id_):
        if self._debug:
            print('script ended', id_)

    def scan_offset(self, id_):
        if self._debug:
            print('scan offset', id_)

    def remove_callback_function(self, callback_id, callable_):
        assert(callback_id in self._callbacks)
        
        if callable_ in self._callbacks[callback_id]:
            self._callbacks[callback_id].remove(callable_)

    def add_callback_function(self, callback_id, callable_):
        assert(callback_id in self._callbacks)
        
        if callable_ not in self._callbacks[callback_id]:
            self._callbacks[callback_id].append(callable_)

    def clear_callbacks(self, callback_id):
        assert(callback_id in self._callbacks)
        
        self._callbacks[callback_id] = []

    def _main_callback(self, callback_id, status_code):
        if self._debug:
            print('\n\n!! main callback', callback_id, status_code)

        if status_code in self._callbacks:
            for fcn in self._callbacks[status_code]:
                try:
                    fcn(callback_id)
                except Exception as ex:
                    if self._debug:
                        print('Callback failed: %s %s' % (ex.__class__, ex))
        else:
            if self._debug:
                print('Unhandled callback (?) status_code=%x callback_id=%d' % 
                        (status_code, callback_id))

    def enable_callbacks(self, begin_acquire=True, end_acquire=True, 
                         begin_fda=True, end_fda=True, script=True, 
                         end_script=True, scan_offset=True, mask=None,
                         id_=None):
        if mask is None:
            values = [
                [begin_acquire, mrc_common.MRC_ENABLE_STATUS_CALLBACK_BEGIN_ACQUIRE],
                [end_acquire, mrc_common.MRC_ENABLE_STATUS_CALLBACK_END_ACQUIRE],
                [begin_fda, mrc_common.MRC_ENABLE_STATUS_CALLBACK_BEGIN_FDA],
                [end_fda, mrc_common.MRC_ENABLE_STATUS_CALLBACK_END_FDA],
                [script, mrc_common.MRC_ENABLE_STATUS_CALLBACK_SCRIPT],
                [end_script, mrc_common.MRC_ENABLE_STATUS_CALLBACK_END_SCRIPT],
                [scan_offset, mrc_common.MRC_ENABLE_STATUS_CALLBACK_SCAN_OFFSET],
            ]

            mask = 0x0
            for set_, mask_ in values:
                if set_:
                    mask |= mask_

        if id_ is None:
            id_ = self._handle.value

        self._set_status_callback_mask(self._handle, mask)

        cb_type = mrc3_client.mrc3_callback_type
        self._cb_fcn = cb_type(self._main_callback)

        #self._set_status_callback_function(self._handle, ctypes.byref(self._cb_fcn))
        print(self._dll._handle, id_)
        _mrc3_callbacks.set_callback(self._dll._handle, id_, self._main_callback)

        self._set_status_callback_id(self._handle, id_)

    def close(self):
        self._check_handle()

        self.release_control()
        self._free_interface(ctypes.byref(self._handle))
        self._handle = None

def test():
    client = None
    try:
        #client = MRC3Client(debug=True, dllname='mrc3_client_d.dll') #, callbacks=False)
        client = MRC3Client(debug=False)

        for i in range(5):
            print('guid', client.interface_guid)
            ret = client.run_script(script_text='\t print "the square root of 2 is", sqrt(2)')
            print('%d: script output 0: "%s"' % (i, ret))
        #try:
        #    ret = client.run_script(script_filename='test')
        #    print('script output 1: "%s"' % ret)
        #except:
        #    pass

        #print(client.script_error)
        #ret = client.run_script(script_text='\t print "the square root of 2 is", sqrt(2)')
        #print('script output 2: "%s"' % ret)
        print('server state: ', client.state)
    finally:
        if client is not None:
            print('... cleanup')
            client.close()
            print('Done')

if __name__ == '__main__':
    test()

