class UserNotFoundException(Exception):
    pass


class ContractNotFoundException(Exception):
    pass


class ContractAlreadySignedException(Exception):
    pass


class SigningOwnContractException(Exception):
    pass


class UserIsUnregisteredException(Exception):
    pass


class InvalidCallbackDataException(Exception):
    pass


class InvalidContractIDException(Exception):
    pass


class ContractAccessDeniedException(Exception):
    pass


class InvalidContractStatusException(Exception):
    pass


class FinishIsNotAvailableException(Exception):
    pass


class PageOutOfBoundsException(Exception):
    pass