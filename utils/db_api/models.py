from peewee import *

from loader import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    telegram_id = IntegerField()
    locale = CharField(max_length=2)


class Contract(BaseModel):
    type = IntegerField()
    date_created = DateField(null=True)
    status = IntegerField()
    description = IntegerField()

    @property
    def invoice(self):
        return self.invoice_set.get()


class UserToContractConnector(BaseModel):
    user = ForeignKeyField(User, backref="contracts")
    contract = ForeignKeyField(Contract, backref="users")
    is_creator = BooleanField()
    is_hidden = BooleanField()


class Invoice(BaseModel):
    contract = ForeignKeyField(Contract, unique=True)
    sum = CharField(10)
    money_from_creator = BooleanField()
