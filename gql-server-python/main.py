import graphene
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


class YesNo(graphene.Enum):
    YES = "YES"
    NO = "NO"


class Query(graphene.ObjectType):
    personCount = graphene.Int(required=True)
    allPersons = graphene.List(graphene.NonNull(Person), phone=YesNo(), required=True)
    findPerson = graphene.Field(Person, name=graphene.String(required=True))

    def resolve_personCount(self):
        return len(persons)

    def resolve_allPersons(parent, info, phone=None):
        if not phone:
            return list(
                map(
                    lambda p: Person(
                        name=p["name"],
                        phone=p.get("phone"),
                        address=Address(city=p["city"], street=p["street"]),
                        id=p.get("id"),
                    ),
                    persons,
                )
            )
        if phone == YesNo.YES:
            filtered_persons = filter(lambda person: "phone" in person, persons)
            return list(
                map(
                    lambda p: Person(
                        name=p["name"],
                        phone=p.get("phone"),
                        address=Address(city=p["city"], street=p["street"]),
                        id=p.get("id"),
                    ),
                    filtered_persons,
                )
            )
        elif phone == YesNo.NO:
            filtered_persons = filter(lambda person: "phone" not in person, persons)
            return list(
                map(
                    lambda p: Person(
                        name=p["name"],
                        phone=p.get("phone"),
                        address=Address(city=p["city"], street=p["street"]),
                        id=p.get("id"),
                    ),
                    filtered_persons,
                )
            )

    def resolve_findPerson(parent, info, name):
        person = next(filter(lambda person: person["name"] == name, persons), None)
        if person:
            return Person(
                name=person["name"],
                phone=person.get("phone"),
                address=Address(city=person["city"], street=person["street"]),
                id=person["id"],
            )
        return None


class addPerson(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        city = graphene.String(required=True)
        street = graphene.String(required=True)
        phone = graphene.String()

    Output = Person

    def mutate(self, info, name, city, street, phone=None):
        id = f"{random()*1500}"
        persons.append(
            {"name": name, "phone": phone, "city": city, "street": street, "id": id}
        )
        return Person(
            name=name, phone=phone, address=Address(city=city, street=street), id=id
        )


class editPhone(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        phone = graphene.String(required=True)

    Output = Person

    def mutate(self, info, name, phone):
        personToUpdateIndex = next(
            (i for i, person in enumerate(persons) if person["name"] == name), None
        )
        if personToUpdateIndex == None:
            return None
        else:
            newPerson = persons[personToUpdateIndex]
            newPerson["phone"] = phone
            return Person(
                name=name,
                phone=phone,
                address=Address(city=newPerson["city"], street=newPerson["street"]),
                id=newPerson["id"],
            )


class Mutation(graphene.ObjectType):
    add_person = addPerson.Field()
    edit_phone = editPhone.Field()


app = FastAPI()
origins = [
    "*"
]  # This should be something like ["http://localhost:3000"] because using * prevents the use of cookies and some auth stuff
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query, mutation=Mutation)))