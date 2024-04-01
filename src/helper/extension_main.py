from helper.gateway import portal
from helper.utils import pathfinder  
from helper.settings import conf, pnt, loglevel
from helper.extension_helper import get_exts

import logging
log = logging.getLogger(__name__)


pf = pathfinder()
p = portal()

class extension_manager():
    def __init__(self, **kargs) -> None:
        self.kargs = kargs
        exts : dict = get_exts()
        self.ext : dict = exts.get(self.kargs.get('extension', None), None)

    def verify_args(self) -> bool: 
        arg_ext = self.kargs.get("extension", None)
        arg_mode = self.kargs.get('mode', None)
        if self.ext is None:
            text = f'The supported extensions are:\n\t <{" ".join(self.exts.keys())}>.\n You entered method <{arg_ext}>'
            log.error(text)
            print(pnt.error(text))
            return False

        #check if specific extension support called method
        if self.kargs.get('mode', None) not in self.ext.get('modes', None):
            text = f'This API is configured and tested only with supported methods on extension <{arg_ext}> are <{self.ext.get("modes")}>. \n \
                You entered method <{arg_mode}>.\n \
                The program is not stoping however be ready for bumpy ride. \n'
            log.warning(text)
            print(pnt.warn(text))
        return True

    def start(self) -> None:
        if not self.verify_args():
            return
        e= self.ext.get('cls', None)(**self.kargs)
        match self.kargs.get('mode'):
            case 'get':
                e.get()
            case 'post':
                e.post()
            case 'patch':
                e.patch()
            case 'delete':
                e.delete()
        e.log_stats()