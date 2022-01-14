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
        return "%s->%s" % (",".join(self.left), self.right)


class BackwardChaining:
    def __init__(self, file_name):
        self.output = ""
        self.output_file_name = None
        self.iteration = 0
        
        self.current_goals = []
        self.found_facts = []
        self.road = []

        self.output += "PARTE 1. Dados\n"
        self.rules, self.facts, self.goal = self.read_data(file_name)
        print(self.rules[0])
        self.print_data(self.rules, self.facts, self.goal)

        self.output += "PARTE 2. Execução\n"
        result = self.do_backward_chaining(self.goal)

        self.output += "\n" + "PARTE 3. Resultados\n"
        self.print_result(result)
        print(self.output)

    def do_backward_chaining(self, goal, indent=""):

        if goal in self.facts:
            self.print_step(goal, indent,
                            "Fato existente por causa do dado %s. Retornando sucesso." % ", ".join(self.facts))
            return True

        if goal in self.current_goals:
            self.print_step(goal, indent, "Ciclo. Retornando falha")
            return False

        if goal in self.found_facts:
            self.print_step(goal, indent, "Fato foi dado por causa dos dados %s e %s. Retornando sucesso." % (
                ", ".join(self.facts), ", ".join(self.found_facts)))
            return True

        results_count = len(self.road)

        for rule in self.rules:
            if rule.right == goal:

                is_satisfied = False
                self.print_step(goal, indent, "Encontrado %s. Novo objetivo %s." % (
                    "R" + str(self.rules.index(rule) + 1) + ":" + str(rule), ", ".join(rule.left)))

                for new_goal in rule.left:
                    self.current_goals.append(goal)
                    is_satisfied = self.do_backward_chaining(new_goal, indent + "-")
                    self.current_goals.pop()

                    if self.goal in self.found_facts:
                        # self.output += ("statisfied")
                        return True

                if is_satisfied:
                    self.road.append("R" + str(self.rules.index(rule) + 1))
                    self.found_facts.append(rule.right)
                    self.print_step(goal, indent, "Fato agora adicionado. Fatos %s e %s. Retornando sucesso." % (
                        ", ".join(self.facts), ", ".join(self.found_facts)))
                    return True

            while len(self.road) > results_count:
                self.road.pop()

        self.print_step(goal, indent, "Sem regras para derivar. Retornando falha.")
        return False

    def print_step(self, goal, indent, msg):
        self.iteration += 1
        self.output += str(self.iteration).rjust(3, " ") + ") %sObjetivo %s. " % (indent, goal) + msg + "\n"

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
            line = line.split(" ")

            if line[0] == '#':
                continue

            if read_state == 0:
                right = line[0]
                left = line[1:]
                rules.append(Rule(left, right))

            if read_state == 1:
                facts = line

            if read_state == 2:
                goal = line[0]

        return rules, facts, goal

    def print_data(self, rules, facts, goal):
        self.output += "  1) Regras\n"
        for rule in rules:
            self.output += "    R%i: %s\n" % (rules.index(rule) + 1, str(rule))
        self.output += "\n  2) Fatos\n    %s.\n\n" % ", ".join(facts)
        self.output += "  3) Objetivo\n    %s.\n\n" % goal

    def print_result(self, result):
        if result is not False:

            if len(self.road) == 0:
                self.output += "  1) Objetivo %s entre os fatos.\n" % self.goal
                self.output += "  2) Caminho vazio.\n"
            else:
                self.output += "  1) Objetivo %s derivado.\n" % self.goal
                self.output += "  2) Caminho: %s.\n" % ", ".join(self.road)
        else:
            self.output += "  1) Objetivo %s inalcançável.\n" % self.goal
