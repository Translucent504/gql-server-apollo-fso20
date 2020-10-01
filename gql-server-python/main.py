import graphene
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from random import random

# gql = type Query {
# allNames: [String!]!} is equivalent to
# class Query :
#     allNames = graphene.NonNull(graphene.List(graphene.String(required=True)))
persons = [
    {
        "name": "Arto Hellas",
        "phone": "040-123543",
        "street": "Tapiolankatu 5 A",
        "city": "Espoo",
        "id": "3d594650-3436-11e9-bc57-8b80ba54c431",
    },
    {
        "name": "Matti Luukkainen",
        "phone": "040-432342",
        "street": "Malminkaari 10 A",
        "city": "Helsinki",
        "id": "3d599470-3436-11e9-bc57-8b80ba54c431",
    },
    {
        "name": "Venla Ruuska",
        "street": "Nallemäentie 22 C",
        "city": "Helsinki",
        "id": "3d599471-3436-11e9-bc57-8b80ba54c431",
    },
]


class Address(graphene.ObjectType):
    street = graphene.String(required=True)
    city = graphene.String(required=True)


class Person(graphene.ObjectType):
    name = graphene.String(required=True)
    phone = graphene.String()
    address = graphene.Field(Address)
    id = graphene.ID()

    def resolve_address(parent, info):
        return Address(street=parent["street"], city=parent["city"])


class YesNo(graphene.Enum):
    YES = "YES"
    NO = "NO"


class Query(graphene.ObjectType):
    personCount = graphene.Int(required=True)
    allPersons = graphene.List(graphene.NonNull(Person), phone=YesNo(), required=True)
    findPerson = Person(name=graphene.String(required=True))

    def resolve_personCount(self):
        return len(persons)

    def resolve_allPersons(parent, root, phone=None):
        if not phone:
            return persons
        if phone == YesNo.YES:
            return filter(lambda person: "phone" in person, persons)
        elif phone == YesNo.NO:
            return filter(lambda person: "phone" not in person, persons)


class addPerson(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        city = graphene.String(required=True)
        street = graphene.String(required=True)
        phone = graphene.String()

    Output = Person

    def mutate(root, info, name, city, street, phone=None):
        id =  f'{random()*1500}'
        persons.append({"name": name, "phone": phone, "city": city, "street": street, 'id':id})
        return Person(name, phone, id, address=Address(city, street))

class Mutation(graphene.ObjectType):
    add_person = addPerson.Field()

app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))