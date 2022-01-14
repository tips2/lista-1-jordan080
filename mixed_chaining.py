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

class MixedChaining:

    def __init__(self, file_name):
        self.iteration = 0
        self.output = ""

        self.current_goals = []
        self.found_facts = []
        self.road = []

        self.output += "PARTE 1. Dados\n"
        self.rules, self.facts, self.goal = self.read_data(file_name)
        self.print_data(self.rules, self.facts, self.goal)

        self.output += "PARTE 2. Execução\n"
        result, self.road = self.controller(self.rules, self.facts, self.goal)

        self.output += "PARTE 3. Resultados\n"
        self.print_results(result, self.road, self.goal)
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

        #self.print_step(goal, indent, "No productions for deduction. Returning, FAIL.")
        all_facts = self.facts + self.found_facts
        rule_list = []
        for rule in self.rules:
            for atom in rule.left:
                rule_list.append(atom)

        rule_list = [x for x in rule_list if x not in all_facts]
        rule_list = list(dict.fromkeys(rule_list))

        new_info = self.get_new_info(rule_list)
        if new_info == True:
            self.print_step(goal, indent, "Novo dado {} adicionado depois de consulta com o usuário.".format(self.facts[-1]))
            return True
        else:
            return False

    def get_new_info(self, rules):
        while True:
            new_fact = input("Isto é verdade?: {} ".format(rules[0]))
            if new_fact in ['Sim', 'sim', 'Não', 'não']:
                break
            else:
                print("Tente novamente. Responda com sim ou não")

        if new_fact == 'Sim' or new_fact == 'sim':
            self.facts.append(rules[0])
            rules.remove(rules[0])
            return True
        elif new_fact == 'Não' or new_fact == 'não':
            if not rules:
                return False
            else:
                rules.remove(rules[0])
                self.get_new_info(rules)
                return True

    def print_step(self, goal, indent, msg):
        self.iteration += 1
        self.output += str(self.iteration).rjust(3, " ") + ") %sObjetivo %s. " % (indent, goal) + msg + "\n"

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
                    self.output += "não aplicada, porque %s está entre os fatos. Levantando flag2.\n" % rule.right
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

    def controller(self, rules, facts, goal):
        result, self.road = self.forward_chaining(rules, facts, goal)

        if result == False:
            result = self.do_backward_chaining(goal)

        return result, self.road

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