
import os

class Url:
    """
        @description: 
    """

    def __init__(
        self, 
        full_url: str or None = None,
        protocol: str or None = None,
        host: str or None = None,
        pathname: str or None = None,
        queryParams: dict or None = None
    ) -> None:
        """
            @description:
            @param full_url:
        """
        self.validate_protocol(protocol)
        self.validate_host(host)
        self.validate_pathname(pathname)

        self.__full_url = full_url
        self.__protocol = protocol
        self.__host = host
        self.__pathname = pathname
        self.__queryParams = queryParams

    def validate_protocol(self, protocol) -> bool:
        """
            @description:
        """
        if protocol is None: return True
        index = [
            'http', 
            'https', 
            'ftp', 
            'ftps', 
            'ssh', 
            'ws',
            'wss',
            'sftp'
        ].index(protocol)
        if index < 0:
            raise Exception('Invalid protocol')
        return True
    
    def validate_host(self, host) -> bool:
        """
            @description: Validate the host
        """
        return True
    
    def validate_pathname(self, pathname) -> bool:
        """
            @description: Validate the pathname
        """
        return True

    def get_full_protocol(self) -> str:
        """
            @description:
        """
        return self.__protocol + '://'
    
    def get_asm_hostandpathname(self) -> str:
        """
            @description: Assemble the host and pathname
        """
        if self.__host is None:
            raise Exception('Host is not defined')
        if self.__pathname is None:
            return self.__host
        
        assembled = self.__host
        if self.__pathname[0] != '/':
            assembled += '/'
        assembled += self.__pathname
        return assembled
    
    def convert_query_params_to_string(self) -> str:
        """
            @description: Convert the query params to string
        """
        if self.__queryParams is None:
            return ''
        query_params_string = '?'
        for key in self.__queryParams:
            query_params_string += key + '=' + str(self.__queryParams[key]) + '&'
        return query_params_string[:-1]

    def get_full_url(self) -> str:
        """
            @description:
        """
        if self.__full_url is None:
            return self.compose_url()
        return self.__full_url

    def compose_url(self) -> str:
        """
            @description:
        """
        url = self.get_full_protocol()
        url += self.get_asm_hostandpathname()
        url += self.convert_query_params_to_string()
        return url