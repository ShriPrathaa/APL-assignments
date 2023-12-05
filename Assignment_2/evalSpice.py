import io
import numpy as np


def valid_file(filename):
    try:  # tries to open file and checks if filename is valid
        with open(filename, "r") as msg:
            pass
    except FileNotFoundError:
        raise FileNotFoundError("Please give the name of a valid SPICE file as input")


def file_check(lines, element, dict1, dict2, dictV):
    i = 1  # initialisation of count of nodes
    listR = []  # list to avoid repetition of element if already present
    listI = []
    found_circuit = False
    end = False
    for line in lines:
        part = line.strip()  # list containing each element, its nodes and value
        parts = part.split()
        if (len(parts) > 0) and len(parts[0]) > 0:
            if parts[0] == ".circuit":
                if found_circuit == True:  # netlist within a netlist
                    raise ValueError("Malformed circuit file")
                found_circuit = True  # enters netlist
                if len(parts) > 1:
                    if parts[1][0] != "#":
                        raise ValueError("Malformed circuit file")
            elif found_circuit:
                if parts[0] == ".end":
                    end = True  # leaves netlist
                    if len(parts) > 1:
                        if parts[1][0] != "#":
                            raise ValueError("Malformed circuit file")
                    break
                if parts[0][0] not in element:  # checks for valid elements
                    raise ValueError("Only V, I, R elements are permitted")
                elif parts[0][0] == "V" or parts[0][0] == "I":
                    if parts[3] != "dc":  # checks if V and I sources are dc
                        raise ValueError("Malformed circuit file")
                    try:
                        f = float(parts[4])  # checks if numeric value is given
                    except:
                        raise ValueError("Malformed circuit file")
                    if len(parts) > 5:  # irrelevant characters present
                        if parts[5][0] != "#":
                            raise ValueError("Malformed circuit file")
                    elif len(parts) <= 4:  # necessary info not present
                        raise ValueError("Malformed circuit file")
                else:  # resistor present
                    try:
                        f = float(parts[3])
                    except ValueError:
                        raise ValueError("Malformed circuit file")
                    if len(parts) > 4:
                        if parts[4][0] != "#":  # irrelevant characters present
                            raise ValueError("Malformed circuit file")
                    elif len(parts) < 4:  # necessary info not present
                        raise ValueError("Malformed circuit file")
                if parts[1] not in dict1.values():
                    dict1[i] = parts[1]  # adds nodes to map
                    node1 = i
                    i = i + 1  # increments node count
                else:
                    for k in dict1:
                        if dict1[k] == (parts[1]):
                            node1 = k

                if parts[2] not in dict1.values():
                    dict1[i] = parts[2]  # adds nodes to map
                    node2 = i
                    i = i + 1  # increments node count
                else:
                    for k in dict1:
                        if dict1[k] == parts[2]:
                            node2 = k
                if (
                    parts[0][0] == "V"
                ):  # checks if voltage sources of different values are connected in parallel
                    if (node1, node2) in dict2["V"]:  # 2 voltage sources in parallel
                        raise ValueError("Circuit error: no solution")
                    elif (node2, node1) in dict2["V"]:
                        raise ValueError("Circuit error: no solution")
                    if parts[0] in dictV.values():  # avoids repetition of element
                        raise ValueError("Malformed circuit file")
                    dict2["V"][node1, node2] = float(parts[4])
                    dictV[node1, node2] = parts[0]
                elif parts[0][0] == "I":
                    if parts[0] in listI:  # avoids repetition of element
                        raise ValueError("Malformed circuit file")
                    if (node2, node1) in dict2["I"]:  # adds up currnt to node
                        dict2["I"][node2, node1] += float(parts[4])
                    elif (node1, node2) in dict2["I"]:
                        dict2["I"][node1, node2] -= float(parts[4])
                    else:
                        dict2["I"][node2, node1] = float(parts[4])
                    listI += parts[0]
                else:
                    if parts[0] in listR:  # avoids repetition of element
                        raise ValueError("Malformed circuit file")
                    if ((node1, node2) in dict2["R"]) and (
                        float(parts[3]) != 0
                    ):  # resistances in parallel
                        dict2["R"][node1, node2] = 1 / (
                            (1 / float(parts[3])) + (1 / dict2["R"][node1, node2])
                        )
                    elif float(parts[3]) != 0:
                        dict2["R"][node1, node2] = float(parts[3])
                    listR += parts[0]
    if not (found_circuit):
        raise ValueError("Malformed circuit file")
    elif not (end):
        raise ValueError("Malformed circuit file")
    v_calc = i  # total count of nodes
    return v_calc


def readfile(filename):
    valid_file(filename)
    with open(filename, "r") as f:  # opens the file using file object,f
        data = f.read()  # reads file object into data
        lines = data.split("\n")  # splits into valid lines ignoring empty lines
        element = ["V", "R", "I"]  # valid elements of circuit
        dict2 = {
            key: {} for key in element
        }  # dictionary of elements(keys) to node-value pairs
        dict1 = {0: "GND"}  # mapping of unique numbers to nodes
        dictV = {}  # mapping of Vsource names to nodes
        v_calc = file_check(lines, element, dict1, dict2, dictV)
        return dict1, dict2, dictV, v_calc


def non_supernode(v_calc, dict2, check, A, B):
    index = 1
    for node in range(v_calc):
        if (v_calc - index) == 0:
            break
        if check[node] == 0:  # node analysis of nodes without voltage source
            for j in dict2["R"].keys():
                if node in j:
                    if (j[0]) == node:
                        other = j[1]
                    else:
                        other = j[0]
                    A[index][node] += 1 / (
                        dict2["R"][j]
                    )  # add 1/R at columns corresponding to node considered
                    A[index][other] -= 1 / (
                        dict2["R"][j]
                    )  # add -1/R to columns corresponding to other nodes
            for g in dict2["I"].keys():
                if node == int(g[0]):  # current from node
                    B[index] -= dict2["I"][g]
                if node == int(g[1]):  # current to node
                    B[index] += dict2["I"][g]
            index += 1
    return index


def supernode(dict2, v_calc, check, A, B, index):
    for j in dict2["V"].keys():  # supernode analysis
        if (v_calc - index) == 0:
            break
        A[index][j[0]] = 1  # voltage at +ve terminal
        A[index][j[1]] = -1  # voltage at -ve terminal
        B[index] = dict2["V"][j]
        index += 1
    for node in range(v_calc):
        if (v_calc - index) > 0:  # rows update upto number of nodes
            for j in dict2["V"].keys():
                if node in j:
                    if j[0] == node:
                        other = j[1]
                    else:
                        other = j[0]
                if check[node] == 1 and check[other] == 1:
                    check[node] -= 1
                    check[other] -= 1
                    for g in dict2["I"].keys():
                        if node in g and other in g:
                            pass
                        elif node in g or other in g:
                            if node == g[0] or other == g[0]:
                                B[index] -= float(
                                    dict2["I"][g]
                                )  # current leaving supernode
                            else:
                                B[index] += float(
                                    dict2["I"][g]
                                )  # current entering supernode
                    for k in dict2["R"].keys():
                        if (node in k) and (other in k):
                            pass  # resistance between 2 nodes under consideration
                        elif node in k:
                            if node == k[0]:
                                node_inter = k[
                                    1
                                ]  # other node where resistance is connected
                            else:
                                node_inter = k[
                                    0
                                ]  # other node where resistance is connected
                            A[index][node] += 1 / float(dict2["R"][k])
                            A[index][node_inter] -= 1 / float(dict2["R"][k])

                        elif other in k:
                            if other == k[0]:
                                node_inter = k[1]
                            else:
                                node_inter = k[0]
                            A[index][other] += 1 / float(
                                dict2["R"][k]
                            )  # add 1/R at columns corresponding to nodes considered
                            A[index][node_inter] -= 1 / float(
                                dict2["R"][k]
                            )  # add -1/R to columns corresponding to other nodes
                    index += 1
                if (v_calc - index) == 0:
                    break


def V_InotinV(V, I, dict2, A, B):
    V[0] = 0  # GND voltage set to 0
    try:
        V[1:] = np.linalg.solve(
            A[1:, 1:], B[1:]
        )  # voltage computation through matrix solving
    except np.linalg.LinAlgError:
        raise ValueError("Circuit error: no solution")
    for j in dict2["I"].keys():  # current between nodes of current sources
        I[j[0]][j[1]] += dict2["I"][j]
        I[j[1]][j[0]] = -I[j[0]][j[1]]
    for j in dict2["R"].keys():  # current between nodes of resistances
        I[j[0]][j[1]] += (V[j[0]] - V[j[1]]) / float(dict2["R"][j])
        I[j[1]][j[0]] = -I[j[0]][j[1]]


def I_create(dict2, v_calc, V_node, I):
    voltage_sources_copy = (
        dict2.copy()
    )  # create a copy of the dictionary as the original can't be modified
    for j in dict2.keys():
        iin = 0  # sum of all currents into the node
        if (
            V_node[j[0]] == 1
        ):  # identify nodes where only one volage source is connected to find current leaving node
            for k in range(
                v_calc
            ):  # iterate across nodes to find currents flowing to them
                if (
                    k != j[1]
                ):  # while calculating currents from node i to j include currents from all nodes except j to i
                    iin += I[k][j[0]]
            if iin != 0:
                I[j[0]][j[1]] += iin
                I[j[1]][j[0]] = -I[j[0]][j[1]]
            else:
                I[j[0]][j[1]] += I[j[0]][j[1]]
                I[j[1]][j[0]] -= I[j[1]][j[0]]
            V_node[j[0]] -= 1  # the node count is decremented
            V_node[j[1]] -= 1
            del voltage_sources_copy[j]
        elif (
            V_node[j[1]] == 1
        ):  # identify nodes where only one volage source is connected to find current entering node
            for k in range(
                v_calc
            ):  # iterate across nodes to find currents flowing from them
                if (
                    k != j[0]
                ):  # while calculating currents from node i to j include currents from all nodes except j to i
                    # exception:if there are just 2 nodes effectively
                    iin += I[k][j[1]]
            if iin != 0:
                I[j[0]][j[1]] -= iin
                I[j[1]][j[0]] = -I[j[0]][j[1]]
            else:
                I[j[0]][j[1]] += I[j[0]][j[1]]
                I[j[1]][j[0]] -= I[j[1]][j[0]]
            del voltage_sources_copy[j]
            V_node[j[0]] -= 1  # the node count is decremented
            V_node[j[1]] -= 1
    if voltage_sources_copy == dict2:  # a loop of voltage sources are present
        raise ValueError("Circuit error: no solution")
    if (
        len(voltage_sources_copy) != 0
    ):  # recursive call until all supernodes are eliminated
        I_create(voltage_sources_copy, v_calc, V_node, I)


def IinVsources(dict2, v_calc, dict1, V, I, dictV):
    V_dict = {}  # dictionary of voltage at nodes
    I_dict = {}  # dictionary of current through voltage sources
    V_node = {}  # count of voltage sources connected to node(key)
    for j in dict2["V"].keys():
        for k in j:
            if k in V_node:
                V_node[k] += 1
            else:
                V_node[k] = 1
    I_create(dict2["V"], v_calc, V_node, I)  # total current between all nodes
    C = np.zeros(len(dict2["V"]))  # total current between supernodes
    v = sorted(dict2["V"])  # used to iterate through dictionary
    X = np.zeros(
        len(v)
    )  # current between supernodes through resistances and current sources
    i2 = 0
    for i in v:
        C[i2] = I[i[0]][i[1]]
        C[i2] = -1 * I[i[1]][i[0]]
        i2 += 1
    i2 = 0
    for j in v:
        for i in dict2["R"]:
            if i == j or (i[0] == j[1] and i[1] == j[0]):  # current through resistances
                X[i2] += (V[j[0]] - V[j[1]]) / float(dict2["R"][i])
        i2 += 1
    i2 = 0
    for j in v:
        for i in dict2["I"]:
            if i == j:
                X[i2] += dict2["I"][j]  # current due to current sources
            elif i[0] == j[1] and i[1] == j[0]:
                X[i2] -= dict2["I"][i]
        i2 += 1
    for i in range(v_calc):
        V_dict[dict1[i]] = V[i]  # dictionary of voltage at nodes
    i2 = 0
    for j in v:
        I_dict[dictV[j]] = C[i2] - X[i2]  # current through the voltage source
        i2 += 1
    return V_dict, I_dict


def evalSpice(f):
    dict1, dict2, dictV, v_calc = readfile(f)
    A = np.zeros((v_calc, v_calc))  # admittance matrix
    B = np.zeros(v_calc)  # current matrix
    check = np.zeros(v_calc)  # count of how many voltage sources, node is connected to
    I = np.zeros((v_calc, v_calc))  # current between nodes
    V = np.zeros(v_calc)  # voltage at each node
    for node in range(v_calc):
        for j in dict2["V"].keys():
            if node in j:
                check[node] += 1
    index = non_supernode(v_calc, dict2, check, A, B)
    supernode(dict2, v_calc, check, A, B, index)
    V_InotinV(V, I, dict2, A, B)
    V_dict, I_dict = IinVsources(dict2, v_calc, dict1, V, I, dictV)
    return V_dict, I_dict
