import getpass
import sys

from data.project.handler import CSVHandler, JSONHandler, XLSXHandler
from data.project.model import Cash


def help_message() -> str:
    """
    Returns a help message which can be displayed for the users.
    :return: the message
    """

    return """
Welcome to our fantastic data handling software which deals with data of trips. In this example, you can generate,
read, write and query a schema which belongs to a car-rental company and contains four types of records:
people, cars, airports and transactions.

Commands:
    help
        You can display this message whenever you want to.

    exit
        Terminates the program.

    generate <count-of-people> <count-of-cars> <count-of-airports> <count-of-transactions>
        Generates a dataset which contains a given number of people, cars, airports and transactions. Also generates their relationships.

    read <format> <path>
        Reads the dataset in a given format, from a given place of your file system.
        <format> is one of the following parameters: csv, json, xlsx, sql
        <path> is a path of a folder which contains the needed file(s). The parameter must be omitted when you select sql as the format.

    write <format> <path>
        Writes the dataset in a given format, to a given place of your file system.
        <format> is one of the following parameters: csv, json, xlsx, sql
        <path> is a path of a folder which will contain the generated file(s). The parameter must be omitted when you select sql as the format.
"""


def get_connection():
    """
    Reads properties of a MySQL connection, then creates the connection.
    :return: the connection
    """

    print("Enter db user:")
    print("$", end=" ")
    user = input()

    print("Enter db password:")
    print("$", end=" ")
    password = getpass.getpass(stream=sys.stdin, prompt="")


def main() -> None:
    """
    Starts an interactive shell.

    :return: nothing
    """
    print(help_message())

    dataset = None
    dataset_type = Cash  # TODO: change this to your own type

    writers = {
        "csv": lambda t: CSVHandler.write_dataset(dataset, t[2]),
        "xlsx": lambda t: XLSXHandler.write_dataset(dataset, t[2]),
        "json": lambda t: JSONHandler.write_dataset(dataset, t[2])
    }

    readers = {
        "csv": lambda t: CSVHandler.read_dataset(dataset_type, t[2]),
        "xlsx": lambda t: XLSXHandler.read_dataset(dataset_type, t[2]),
        "json": lambda t: JSONHandler.read_dataset(dataset_type, t[2])
    }

    while True:
        print("$", end=" ")
        line = input()
        tokens = line.split(" ")
        match tokens:
            case ["exit"]:
                break
            case ["help"]:
                print(help_message())
            case ["generate", _, _]:
                dataset = dataset_type.generate(int(tokens[1]), int(tokens[2]))
            case ["write", ("csv" | "xlsx" | "json") as doc_type, _]:
                writers[doc_type](tokens)
            case ["write", "sql"]:
                writers[tokens[1]](tokens)
            case ["read", ("csv" | "xlsx" | "json" | "sql") as doc_type, _]:
                dataset = readers[doc_type](tokens)
            case [*o]:
                print("unknown command", file=sys.stderr)


if __name__ == "__main__":
    main()
