class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.flag1 = False
        self.flag2 = False

    def follows(self, facts):
        for fact in self.left:
            if fact not in facts:
                return fact
        return None

    def __str__(self):
        return ",".join(self.left) + "->" + self.right


class ForwardChaining:
    def __init__(self, file_name):
        self.iteration = 0
        self.output = ""
        self.output_file_name = None

        self.output += "PARTE 1. Dados\n"
        rules, facts, goal = self.read_data(file_name)
        self.print_data(rules, facts, goal)

        self.output += "PARTE 2. Execução\n"
        result, road = self.forward_chaining(rules, facts, goal)

        self.output += "PARTE 3. Resultados\n"
        self.print_results(result, road, goal)
        print(self.output)

    def forward_chaining(self, rules, facts, goal):
        ir = len(facts)
        iteration = 0
        road = []

        while goal not in facts:
            rule_applied = False
            iteration += 1
            self.output += "%i".rjust(4, " ") % iteration + " ITERAÇÃO\n"

            for rule in rules:
                self.output += "    R%i:%s " % ((rules.index(rule) + 1), str(rule))

                if rule.flag1:
                    self.output += "pulando, porque flag1 foi levantada.\n"
                    continue

                if rule.flag2:
                    self.output += "pulando, porque flag2 foi levantada.\n"
                    continue

                if rule.right in facts:
                    self.output += "não aplicado, porque %s está entre os fatos. Levantando flag2.\n" % rule.right
                    rule.flag2 = True
                    continue

                missing = rule.follows(facts)

                if missing is None:
                    rule_applied = True
                    rule.flag1 = True
                    facts.append(rule.right)
                    road.append("R" + str(rules.index(rule) + 1))
                    self.output += "aplicado. Levantando flag1. Fatos %s implica %s.\n" % (
                        ", ".join(facts[:ir]), ", ".join(facts[ir:]))
                    break
                else:
                    self.output += "não aplicado, porque fato está faltando: %s\n" % missing
            self.output += "\n"

            if not rule_applied:
                return False, []

        return True, road

    def read_data(self, file_name):
        rules = []
        facts = []
        goal = None

        file = open(file_name, "r")
        read_state = 0

        for line in file:
            line = line.replace("\n", "")

            if line == "":
                read_state += 1
                continue
            if line[0] == '#':
                continue

            line = line.split(" ")

            if read_state == 0:
                right = line[0]
                left = line[1:]
                rules.append(Rule(left, right))

            if read_state == 1:
                facts = line

            if read_state == 2:
                goal = line[0]

            if read_state > 2:
                self.output += "Formatação incorreta do arquivo. Por favor, tente novamente."
                return [], [], None

        return rules, facts, goal

    def print_data(self, rules, facts, goal):

        self.output += "  1) Regras\n"
        for rule in rules:
            self.output += "    R%i: %s\n" % (rules.index(rule) + 1, str(rule))
        self.output += "\n  2) Fatos %s.\n" % ", ".join(facts)
        self.output += "\n  3) Objetivo %s\n\n" % goal

    def print_results(self, result, road, goal):

        if result:
            if len(road) == 0:
                self.output += "  1) Objetivo %s entre os fatos.\n" % goal
                self.output += "  2) Caminho vazio.\n"
            else:
                self.output += "  1) Objetivo %s derivado.\n" % goal
                self.output += "  2) Caminho: %s.\n" % ", ".join(road)
        else:
            self.output += "  1) Objetivo %s inalcançável.\n" % goal