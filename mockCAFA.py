from peewee import *

database = MySQLDatabase('mockCAFA', **{'password': 'password', 'user': 'root'})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Go(BaseModel):
    ai_go = PrimaryKeyField(db_column='AI_GO')
    go_domain = CharField(db_column='GO_Domain', null=True)
    go_term = CharField(db_column='GO_Term', null=True)
    go = CharField(db_column='GO_id', null=True)

    class Meta:
        db_table = 'GO'

class Protein(BaseModel):
    ai_protein = PrimaryKeyField(db_column='AI_Protein')
    accession = CharField(db_column='Accession', null=True)
    cafa = CharField(db_column='CAFA_ID', null=True)
    entryname = CharField(db_column='EntryName', null=True)

    class Meta:
        db_table = 'Protein'

class ProteinGo(BaseModel):
    ai_protein_go = IntegerField(db_column='AI_Protein_GO')
    fk_go = ForeignKeyField(db_column='FK_GO', rel_model=Go, to_field='ai_go')
    fk_protein = ForeignKeyField(db_column='FK_Protein', rel_model=Protein, to_field='ai_protein')

    class Meta:
        db_table = 'Protein_GO'
        primary_key = CompositeKey('ai_protein_go', 'fk_go', 'fk_protein')

class Evidence(BaseModel):
    ai_evidence = IntegerField(db_column='AI_Evidence')
    evidencecode = CharField(db_column='EvidenceCode', null=True)
    fk_protein_go = ForeignKeyField(db_column='FK_Protein_GO', rel_model=ProteinGo, to_field='ai_protein_go')
    ondate = DateField(db_column='OnDate', null=True)

    class Meta:
        db_table = 'Evidence'
        primary_key = CompositeKey('ai_evidence', 'fk_protein_go')

class Exp(BaseModel):
    date = DateField(db_column='Date', null=True)
    entryname = CharField(db_column='EntryName', null=True)
    evidence = CharField(db_column='Evidence', null=True)
    go = CharField(db_column='GO_id', null=True)

    class Meta:
        db_table = 'exp'

class Nonexp(BaseModel):
    date = DateField(db_column='Date', null=True)
    entryname = CharField(db_column='EntryName', null=True)
    evidence = CharField(db_column='Evidence', null=True)
    go = CharField(db_column='GO_id', null=True)

    class Meta:
        db_table = 'nonexp'

class Type1(BaseModel):
    entryname = CharField(db_column='EntryName', null=True)
    evidenceafter = CharField(db_column='EvidenceAfter', null=True)
    evidencebefore = CharField(db_column='EvidenceBefore', null=True)
    go = CharField(db_column='GO_id', null=True)

    class Meta:
        db_table = 'type1'

