class InvoiceStatus:
    class SignNeeded:
        @staticmethod
        def status_id():
            return "1"

    class Active:
        @staticmethod
        def status_id():
            return "2"

    class Done:
        @staticmethod
        def status_id():
            return "3"
