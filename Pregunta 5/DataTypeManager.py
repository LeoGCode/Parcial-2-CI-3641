class DataTypeManager:
    def __init__(self):
        self.atomics = {}
        self.structs = {}
        self.unions = {}

    def begin_program(self):
        print("Welcome to the Data Type Manager!")
        while True:
            action = input("Please enter an action: ")
            param = action.split(" ")
            type_action = param.pop(0).lower()

            if type_action == "atomic" or type_action == "atomico" or type_action == "1":
                if len(param) != 3:
                    print("Error: Invalid number of parameters.")
                    continue
                if not param[1].isdigit() or not param[2].isdigit():
                    print("Error: <representation> and <alignment> must be positive integers.")
                    continue
                self.create_atomic(param[0], int(param[1]), int(param[2]))

            elif type_action == "struct" or type_action == "2":
                if len(param) < 2:
                    print("Error: Invalid number of parameters.")
                    continue
                name = param.pop(0)
                self.create_struct(name, param)

            elif type_action == "union" or type_action == "3":
                if len(param) < 2:
                    print("Error: Invalid number of parameters.")
                    continue
                name = param.pop(0)
                self.create_union(name, param)

            elif type_action == "describe" or type_action == "describir" or type_action == "4":
                if len(param) != 1:
                    print("Error: Invalid number of parameters.")
                    continue
                self.describe_type(param[0])

            elif type_action == "exit" or type_action == "salir" or type_action == "5":
                print("Thank you for using the Data Type Manager!")
                break

            elif type_action == "help" or type_action == "ayuda":
                print("ATOMIC <name> <representation> <alignment>")
                print("STRUCT <name> [<type>]")
                print("UNION <name> [<type>]")
                print("DESCRIBE <name>")
                print("EXIT")

            else:
                print("Invalid action. Please try again.")
                print("Typed help to see the available actions.")

    def create_atomic(self, name, representation, alignment):
        if name in self.atomics or name in self.structs or name in self.unions:
            print("Error: The type name already exists.")
            return

        self.atomics[name] = self.Atomic(name, representation, alignment)
        print("New atomic type created successfully.")

    def create_struct(self, name, types):
        if name in self.structs or name in self.unions or name in self.atomics:
            print("Error: The type name already exists.")
            return

        packaging_size = 0  # implicit wasted bytes
        max_align = 0
        unpackaging_size = 0
        wasted_bytes = 0

        for name_type in types:
            if name_type in self.atomics:
                packaging_size += self.atomics[name_type].representation
                if self.atomics[name_type].alignment > max_align:
                    max_align = self.atomics[name_type].alignment
                if unpackaging_size % self.atomics[name_type].alignment == 0:
                    unpackaging_size += self.atomics[name_type].representation
                else:
                    wasted_bytes += unpackaging_size % self.atomics[name_type].alignment
                    unpackaging_size += unpackaging_size % self.atomics[name_type].alignment
                    unpackaging_size += self.atomics[name_type].representation

            elif name_type in self.structs:
                packaging_size += self.structs[name_type].size
                if self.structs[name_type].alignment > max_align:
                    max_align = self.structs[name_type].alignment
                if unpackaging_size % self.structs[name_type].alignment == 0:
                    unpackaging_size += self.structs[name_type].size
                else:
                    wasted_bytes += unpackaging_size % self.structs[name_type].alignment
                    unpackaging_size += unpackaging_size % self.structs[name_type].alignment
                    unpackaging_size += self.structs[name_type].size

            elif name_type in self.unions:
                packaging_size += self.unions[name_type].size
                if self.unions[name_type].alignment > max_align:
                    max_align = self.unions[name_type].alignment
                if unpackaging_size % self.unions[name_type].alignment == 0:
                    unpackaging_size += self.unions[name_type].size
                else:
                    wasted_bytes += unpackaging_size % self.unions[name_type].alignment
                    unpackaging_size += unpackaging_size % self.unions[name_type].alignment
                    unpackaging_size += self.unions[name_type].size

            else:
                print("Error: The type name does not exist.")
                return

        self.structs[name] = self.Struct(name, types, [unpackaging_size, packaging_size], [max_align, 1], wasted_bytes)
        print("Type struct created successfully.")

    def create_union(self, name, types):
        if name in self.unions or name in self.structs or name in self.atomics:
            print("Error: The type name already exists.")
            return
        max_size = 0
        max_align = 0
        for name_type in types:
            if name_type in self.atomics:
                if self.atomics[name_type].representation > max_size:
                    max_size = self.atomics[name_type].representation
                    max_align = self.atomics[name_type].alignment
            elif name_type in self.structs:
                if self.structs[name_type].size[1] > max_size:
                    max_size = self.structs[name_type].size[1]
                    max_align = self.structs[name_type].alignment[1]
            elif name_type in self.unions:
                if self.unions[name_type].size > max_size:
                    max_size = self.unions[name_type].size
                    max_align = self.unions[name_type].alignment
            else:
                print("Error: The type name does not exist.")
                return

        self.unions[name] = self.Union(name, types, max_size, max_align)
        print("Type union created successfully.")

    def describe_type(self, name):
        if name in self.atomics:
            print(self.atomics[name].describe())
        elif name in self.structs:
            print(self.structs[name].describe())
        elif name in self.unions:
            print(self.unions[name].describe())
        else:
            print("Error: The type name does not exist.")

    class Atomic:

        def __init__(self, name: str, representation: int, alignment: int):
            self.name = name
            self.representation = representation
            self.alignment = alignment

        def describe(self):
            str_to_prt = ""
            str_to_prt += "Name: " + self.name + "\n"
            str_to_prt += "Size: " + str(self.representation) + "\n"
            str_to_prt += "Alignment: " + str(self.alignment) + "\n"
            str_to_prt += "Bytes wasted: " + str(self.representation % self.alignment) + "\n"
            return str_to_prt

    class Struct:

        def __init__(self, name: str, types: list, size: list, alignment: list, wasted_bytes: int):
            self.name = name
            self.types = types
            self.size = size
            self.alignment = alignment
            self.wasted_bytes = wasted_bytes

        def describe(self):
            str_to_prt = ""
            str_to_prt += "Name: " + self.name + "\n" \
                        + "UnPackaging\n" \
                        + "     Size: " + str(self.size[0]) + "\n" \
                        + "     Alignment: " + str(self.alignment[0]) + "\n" \
                        + "     Bytes wasted: " + str(self.wasted_bytes) + "\n" \
                        + "Packaging\n" \
                        + "     Size: " + str(self.size[1]) + "\n" \
                        + "     Alignment: 1\n" \
                        + "     Bytes wasted: 0\n"
            return str_to_prt

    class Union:

        def __init__(self, name: str, types: list, size: int, alignment: int):
            self.name = name
            self.types = types
            self.size = size
            self.alignment = alignment

        def describe(self):

            str_to_prt = ""
            str_to_prt += "Name: " + self.name + "\n"
            str_to_prt += "Size: " + str(self.size) + "\n"
            str_to_prt += "Alignment: " + str(self.alignment) + "\n"
            str_to_prt += "Bytes wasted: " + str(self.size % self.alignment) + "\n"

            return str_to_prt

