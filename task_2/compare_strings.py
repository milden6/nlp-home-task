from __future__ import division

# Hamming distance
def hammingDistance(str1, str2):
    i = 0
    count = 0

    if len(str1) != len(str2):
        # return "Length error"
        return 1

    while i < len(str1):
        if str1[i] != str2[i]:
            count += 1
        i += 1
    return count / len(str2)


# Jaro distance
def jaroDistance(str1, str2):
    str1_len = len(str1)
    str2_len = len(str2)

    if str1_len == 0 and str2_len == 0:
        return 1

    match_distance = (max(str1_len, str2_len) // 2) - 1

    s_matches = [False] * str1_len
    t_matches = [False] * str2_len

    matches = 0
    transpositions = 0

    for i in range(str1_len):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, str2_len)

        for j in range(start, end):
            if t_matches[j]:
                continue
            if str1[i] != str2[j]:
                continue
            s_matches[i] = True
            t_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0

    k = 0
    for i in range(str1_len):
        if not s_matches[i]:
            continue
        while not t_matches[k]:
            k += 1
        if str1[i] != str2[k]:
            transpositions += 1
        k += 1

    return ((matches / str1_len) +
            (matches / str2_len) +
            ((matches - transpositions / 2) / matches)) / 3


# Levenshtein distance
def levenshteinDistance(str1, str2):
    if len(str1) > len(str2):
        str1, str2 = str2, str1
    distances = range(len(str1) + 1)
    for index2, char2 in enumerate(str2):
        newDistances = [index2 + 1]
        for index1, char1 in enumerate(str1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1 + 1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]
