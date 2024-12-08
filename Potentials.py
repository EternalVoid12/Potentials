import copy


class Equations:

    def __init__(self, t):
        lst = t.split()
        self.dE0 = float(lst[-1])
        while "+" in lst:
            lst.remove("+")
        r = lst.index("=")
        right = lst[r + 1:-1]
        left = lst[:r]
        self.right = dict()
        self.left = dict()
        for word in right:
            pair = function1(word)
            self.right[pair[1]] = pair[0]
        for word in left:
            pair = function1(word)
            self.left[pair[1]] = pair[0]

    def tostr(self):
        w = " + ".join([knull(self.left[key]) + key for key in self.left.keys()])
        u = " + ".join([knull(self.right[key]) + key for key in self.right.keys()])
        return w + " = " + u

    # print(self.left,self.right)
    def multiply(self, k):
        c = copy.deepcopy(self)
        for key in c.right.keys():
            c.right[key] *= k
        for key in c.left.keys():
            c.left[key] *= k
        return c

    def subtract(self, other):
        c = copy.deepcopy(self)
        for key in c.left.keys():
            if key in other.left.keys():
                c.left[key] -= other.left[key]
            elif key in other.right.keys():
                c.left[key] += other.right[key]

        for key in c.right.keys():
            if key in other.right.keys():
                c.right[key] -= other.right[key]
            elif key in other.left.keys():
                c.right[key] += other.left[key]
        for key in other.right.keys():
            if key not in c.right.keys() and key not in c.left.keys():
                c.left[key] = other.right[key]
        for key in other.left.keys():
            if key not in c.right.keys() and key not in c.left.keys():
                c.right[key] = other.left[key]
        d = copy.deepcopy(c.left)
        for key in c.left.keys():
            if d[key] < 0:
                c.right[key] = -c.left[key]
                d.pop(key)
            elif c.left[key] == 0:
                d.pop(key)
        c.left = d
        w = copy.deepcopy(c.right)
        for key in c.right.keys():
            if w[key] < 0:
                c.left[key] = -c.right[key]
                w.pop(key)
            elif c.right[key] == 0:
                w.pop(key)
        c.right = w
        return c

    def calc(self, T, p, t):
        results = 0
        resulth = 0
        result = ""
        for i in self.left.keys():
            #            print("Vедите состояние " + i + " :")
            #            p =
            s = t[i][p][1]
            h = t[i][p][0]
            if s == "-" or h == "-":
                #                print("NaN")
                result += "Не хVатает данных"
                return
            else:
                results -= float(s) * self.left[i]
                resulth -= float(h) * self.left[i]
        for i in self.right.keys():
            #            print("Vедите состояние " + i + " :")
            #            p = input()
            s = t[i][p][1]
            h = t[i][p][0]
            if s == "-" or h == "-":
                result = "Не хVатает данных"
                return
            else:
                results += float(s) * self.right[i]
                resulth += float(h) * self.right[i]
        #        print("dS="+str(round(results,1))+" J/mol*k","dH="+str(round(resulth,1))+" kJ/mol")
        dG = (resulth * 1000 - T * results) / 1000
        #        print("dG="+ str(round(dG,1))+" kJ/mol")

        result = str("dS=" + str(round(results, 1)) + " J/mol*k" + "\n" +
                     "dH=" + str(round(resulth, 1)) + " kJ/mol" +
                     "\n" + "dG=" + str(round(dG, 1)) + " kJ/mol")
        return result

    def calc2(self, T, states, t):
        results = float(0)
        resulth = float(0)
        result = ""
        j = 0
        for i in self.left.keys():
            p = states[j]
            #           print("Vедите состояние " + i + " :")
            #            p =
            s = t[i][p][1]
            h = t[i][p][0]
            j += 1
            if s == "-" or h == "-":
                result = "Не хVатает данных"
                return
            else:
                results -= float(s) * self.left[i]
                resulth -= float(h) * self.left[i]
        for i in self.right.keys():
            p = states[j]
            #            print("Vедите состояние " + i + " :")
            #            p = input()
            s = t[i][p][1]
            h = t[i][p][0]
            j += 1
            if s == "-" or h == "-":
                result = "Не хVатает данных"
                return
            else:
                results += float(s) * self.right[i]
                resulth += float(h) * self.right[i]
        #        print("dS="+str(round(results,1))+" J/mol*k","dH="+str(round(resulth,1))+" kJ/mol")
        dG = (resulth * 1000 - T * results) / 1000
        #        print("dG="+ str(round(dG,1))+" kJ/mol")

        result = str("dS=" + str(round(results, 1)) + " J/mol*k" + "\n" +
                     "dH=" + str(round(resulth, 1)) + " kJ/mol" +
                     "\n" + "dG=" + str(round(dG, 1)) + " kJ/mol")
        return result


def function1(term):
    for i in range(len(term)):
        if not term[i].isdigit():
            if i == 0:
                return (1, term[i:])
            else:
                return (int(term[:i]), term[i:])


def knull(k):
    if k == 1:
        return ""
    else:
        return str(k)


def Gibbs(T, eq, p):
    while True:
        Equations(eq + " 0").calc(T, p, t)


g = open(r'Term.txt', 'r')
t = dict()


def get_t(g):
    t = dict()
    for line in g:
        lst = line.split()
        sub = lst[0]
        t[sub] = dict()
        if "gas" in lst:
            idx = lst.index("gas")
            t[sub]["gas"] = (lst[idx + 1], lst[idx + 2])
        if "liq" in lst:
            idx = lst.index("liq")
            t[sub]["liq"] = (lst[idx + 1], lst[idx + 2])
        if "cr" in lst:
            idx = lst.index("cr")
            t[sub]["cr"] = (lst[idx + 1], lst[idx + 2])
    return t


# print(t)


def Nernst(array, react, pH, M, C):
    import math
    result = str()
    Ox = []
    Red = []
    reactant = str.split(react)
    for line in array:
        word_list = Equations(line)

        for f in reactant:
            if f in word_list.right:
                Red.append(line)

            if f in word_list.left:
                Ox.append(line)

    for i in Ox:
        for g in Red:
            #            if i == g :

            e1 = Equations(i)
            e2 = Equations(g)

            lineOx = "Ox : " + i
            lineRed = "Red : " + g

            n = e1.left["e"]
            m = e2.left["e"]

            z = (n * m) // math.gcd(n, m)
            s1 = int(z / n)
            s2 = int(z / m)

            line3 = e1.multiply(s1).subtract(e2.multiply(s2)).tostr()

            dE = float(i.split()[-1]) - float(g.split()[-1])

            if set(reactant) == set(Equations(line3 + " 0").left.keys()):

                if pH <= 7:

                    if e1.left.get("H+") != None:

                        Eox = float(i.split()[-1]) - 0.059 * (e1.left["H+"] / n) * pH
                    else:
                        Eox = float(i.split()[-1])
                    if e2.left.get("H+") != None:
                        Ered = float(g.split()[-1]) - 0.059 * (e2.left["H+"] / m) * pH
                    else:
                        Ered = float(g.split()[-1])

                else:
                    if e1.right.get("OH-") != None:

                        Eox = float(i.split()[-1]) + 0.059 * (e1.right["OH-"] / n) * pH
                    else:
                        Eox = float(i.split()[-1])
                    if e2.right.get("OH-") != None:
                        Ered = float(g.split()[-1]) + 0.059 * (e2.right["OH-"] / m) * pH
                    else:
                        Ered = float(g.split()[-1])

                if str(C) == "CheckState.Checked":
                    if str(M) == "CheckState.Checked":
                        if Eox - Ered > 0:
                            result += str(line3 + "\n")
                    else:
                        result += str(line3 + "\n")

                #            print(set(Equations(line3+" 0").left.keys()))
                #            print(set(reactant)

                if str(M) == "CheckState.Checked" and not str(C) == "CheckState.Checked":
                    #                print(Eox - Ered)
                    if Eox - Ered > 0:
                        result += str(lineOx + "\n" +
                                      lineRed + "\n" +
                                      line3 + "\n" +
                                      "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n" +
                                      "ΔE° = " + str(round(dE, 3)) + " V" + "\n" +
                                      "ΔE (pH = " + str(pH) + ") = " + str(round(Eox - Ered, 3)) + " V" + "\n" +
                                      "ΔG = " + str(round(-1 * (Eox - Ered) * z, 3)) + "F J" + "\n" +
                                      "-----------------------------------------------------" + "\n")

                elif not str(C) == "CheckState.Checked":
                    result += str(lineOx + "\n" +
                                  lineRed + "\n" +
                                  line3 + "\n" +
                                  "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n" +
                                  "ΔE° = " + str(round(dE, 3)) + " V" + "\n" +
                                  "ΔE (pH = " + str(pH) + ") = " + str(round(Eox - Ered, 3)) + " V" + "\n" +
                                  "ΔG = " + str(round(-1 * (Eox - Ered) * z, 3)) + "F J" + "\n" +
                                  "-----------------------------------------------------" + "\n")
    return result


def Nernst_2(array, react, pH, M, C, act):
    import math
    result = str()
    Ox = []
    Red = []
    reactant = str.split(react)

    for line in array:
        word_list = Equations(line)

        for f in reactant:
            if f in word_list.right:
                Red.append(line)

            if f in word_list.left:
                Ox.append(line)

    for i in Ox:
        for g in Red:
            if i != g:

                e1 = Equations(i)
                e2 = Equations(g)

                lineOx = "Ox : " + i
                lineRed = "Red : " + g

                n = e1.left["e"]
                m = e2.left["e"]

                z = (n * m) // math.gcd(n, m)
                s1 = int(z / n)
                s2 = int(z / m)

                line3 = e1.multiply(s1).subtract(e2.multiply(s2)).tostr()

                dE = float(i.split()[-1]) - float(g.split()[-1])

                if set(reactant) == set(Equations(line3 + " 0").left.keys()):

                    if pH <= 7:

                        if e1.left.get("H+") != None:

                            Eox = float(i.split()[-1]) - 0.059 * (e1.left["H+"] / n) * pH
                        else:
                            Eox = float(i.split()[-1])
                        if e2.left.get("H+") != None:
                            Ered = float(g.split()[-1]) - 0.059 * (e2.left["H+"] / m) * pH
                        else:
                            Ered = float(g.split()[-1])

                    else:
                        if e1.right.get("OH-") != None:

                            Eox = float(i.split()[-1]) + 0.059 * (e1.right["OH-"] / n) * pH
                        else:
                            Eox = float(i.split()[-1])
                        if e2.right.get("OH-") != None:
                            Ered = float(g.split()[-1]) + 0.059 * (e2.right["OH-"] / m) * pH
                        else:
                            Ered = float(g.split()[-1])

                    if str(C) == "CheckState.Checked":
                        if str(M) == "CheckState.Checked":
                            if Eox - Ered > 0:
                                result += str(line3 + "\n")
                        else:
                            result += str(line3 + "\n")

                    #            print(set(Equations(line3+" 0").left.keys()))
                    #            print(set(reactant)

                    if str(M) == "CheckState.Checked" and not str(C) == "CheckState.Checked":
                        #                print(Eox - Ered)
                        if Eox - Ered > 0:
                            result += str(lineOx + "\n" +
                                          lineRed + "\n" +
                                          line3 + "\n" +
                                          "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n" +
                                          "ΔE° = " + str(round(dE, 3)) + " V" + "\n" +
                                          "ΔE (pH = " + str(pH) + ") = " + str(round(Eox - Ered, 3)) + " V" + "\n" +
                                          "ΔG = " + str(round(-1 * (Eox - Ered) * z, 3)) + "F J" + "\n" +
                                          "-----------------------------------------------------" + "\n")

                    elif not str(C) == "CheckState.Checked":
                        result += str(lineOx + "\n" +
                                      lineRed + "\n" +
                                      line3 + "\n" +
                                      "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n" +
                                      "ΔE° = " + str(round(dE, 3)) + " V" + "\n" +
                                      "ΔE (pH = " + str(pH) + ") = " + str(round(Eox - Ered, 3)) + " V" + "\n" +
                                      "ΔG = " + str(round(-1 * (Eox - Ered) * z, 3)) + "F J" + "\n" +
                                      "-----------------------------------------------------" + "\n")
    return result
