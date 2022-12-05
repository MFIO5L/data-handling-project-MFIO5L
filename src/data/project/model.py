from __future__ import annotations

import random
from dataclasses import field, dataclass
from typing import Type, cast

from faker import Faker

from data.project.base import Dataset, Entity


# TODO replace this module with your own types

@dataclass
class Cash(Dataset):
    people: list[Person]
    cryptocurrencies: list[Cryptocurrency]

    @staticmethod
    def entity_types() -> list[Type[Entity]]:
        return [Person, Cryptocurrency]

    @staticmethod
    def from_sequence(entities: list[list[Entity]]) -> Dataset:
        return Cash(
            cast(list[Person], entities[0]),
            cast(list[Cryptocurrency], entities[1])
        )

    def entities(self) -> dict[Type[Entity], list[Entity]]:
        res = dict()
        res[Person] = self.people
        res[Cryptocurrency] = self.cryptocurrencies

        return res

    @staticmethod
    def generate(
            count_of_customers: int,
            count_of_cryptocurrencies: int):

        def generate_people(n: int, male_ratio: float = 0.5, locale: str = "en_US",
                            unique: bool = False, min_age: int = 0, max_age: int = 100) -> list[Person]:
            """
            Generates people.
            """

            assert n > 0
            assert 0 <= male_ratio <= 1
            assert 0 <= min_age <= max_age

            fake = Faker(locale)
            people = []
            for i in range(n):
                male = random.random() < male_ratio
                generator = fake if not unique else fake.unique
                people.append(Person(
                    "P-" + (str(i).zfill(6)),
                    generator.name_male() if male else generator.name_female(),
                    random.randint(min_age, max_age),
                    male))

            return people

        def generate_cryptocurrency(n: int)->list[Cryptocurrency]:

            assert n > 0

            fake = Faker()
            cryptocurrencies = []

            for i in range(n):
                random_data = fake
                cryptocurrencies.append(Cryptocurrency(
                    random_data.currency_code(),
                    random_data.currency_name(),
                    random_data.currency_symbol()
                ))
            return cryptocurrencies

        people = generate_people(count_of_customers)
        cryptocurrencies = generate_cryptocurrency(count_of_cryptocurrencies)
        return Cash(people, cryptocurrencies)


@dataclass
class Person(Entity):
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(default=True, repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Person:
        return Person(seq[0], seq[1], int(seq[2]), seq[3] == "1")

    def to_sequence(self) -> list[str]:
        return [self.id, self.name, str(self.age), 0 if self.male else 1]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "name", "age", "male"]

    @staticmethod
    def collection_name() -> str:
        return "people"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Person.collection_name()} (
            ID VARCHAR2(8) PRIMARY KEY,
            NAME VARCHAR2(50),
            AGE NUMBER(5),
            MALE NUMBER(1)
        )
        """
@dataclass
class Cryptocurrency(Entity):
    code: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    symbol: str = field(repr=True, compare=False)


    @staticmethod
    def from_sequence(seq: list[str]) -> Cryptocurrency:
        return Cryptocurrency(seq[0], seq[1], (seq[2]))

    def to_sequence(self) -> list[str]:
        return [self.code, self.name, self.symbol]

    @staticmethod
    def field_names() -> list[str]:
        return ["code", "name", "symbol"]

    @staticmethod
    def collection_name() -> str:
        return "cryptocurrency"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Cryptocurrency.collection_name()} (
            ID VARCHAR2(8) PRIMARY KEY,
            NAME VARCHAR2(50),
            AGE NUMBER(5),
            MALE NUMBER(1)
        )
        """
