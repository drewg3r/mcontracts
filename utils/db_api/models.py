from peewee import *

from loader import db
from utils.db_api.statuses import InvoiceStatus


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    telegram_id = IntegerField()
    locale = CharField(max_length=2)


class Contract(BaseModel):
    type = IntegerField()
    date_created = DateField(null=True)
    _status = IntegerField(column_name="status")
    description = IntegerField()

    @property
    def invoice(self):
        return self.invoice_set.get()

    @property
    def status(self):
        if self.type == 1:
            if self._status == 1:
                return InvoiceStatus.SignNeeded
            if self._status == 2:
                return InvoiceStatus.Active
            if self._status == 3:
                return InvoiceStatus.Done

    @status.setter
    def status(self, new_status):
        if type(new_status) is int:
            self._status = new_status
        elif type(new_status) in [InvoiceStatus.SignNeeded,
                                  InvoiceStatus.Active, InvoiceStatus.Done]:
            self._status = new_status.status_id()


class UserToContractConnector(BaseModel):
    user = ForeignKeyField(User, backref="contracts")
    contract = ForeignKeyField(Contract, backref="users")
    is_creator = BooleanField()
    is_hidden = BooleanField()


class Invoice(BaseModel):
    contract = ForeignKeyField(Contract, unique=True)
    sum = CharField(10)
    money_from_creator = BooleanField()
