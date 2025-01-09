def delete_first_occurrence(s:str, substrings:list)->str:
    """Given a string and a list of substrings, return a string without the first occurences of each substring,
    ordering the deletions based on the order of the list
    Example: "12341234" and ["123", "34"] return "412"
    Args:
        s (str): a string
        substrings (list): a list of strings

    Returns:
        str: the new string without the substrings
    """
    for substring in substrings:
        index = s.find(substring)
        if index != -1:
            s = s[:index] + s[index + len(substring):]
    return s

def find_all_largest_common_substrings(string1:str, string2:str)->list:
    """Given two strings, gives all the largest possible common substrings,
    considering each found substring can not be part of another substring.
    Example : "1234" and "123534" will return "123".

    Args:
        string1 (str): a string
        string2 (str): an another string (order is not important)

    Returns:
        list: the list of all the largest possible common substrings. Empty list if none.
    """
    common_substrings = []
    if len(string1)>len(string2):
        shortest_s, longest_s, len_shortest = string2, string1, len(string2)
    else:
        shortest_s, longest_s, len_shortest = string1, string2, len(string1)
    for len_substring in range(len_shortest-1, 1, -1):
        for index_substring in range(1+len_shortest-len_substring):
            substring = shortest_s[index_substring:index_substring+len_substring]
            if len(substring) < len_substring:
                break # cette ligne permet de régler deux problèmes : les substrings vont trop loin, et si on raccourci la string de base, ils vont encore plus loin
            if substring in longest_s:
                common_substrings.append(substring)
                longest_s = delete_first_occurrence(longest_s, [substring])
                shortest_s = delete_first_occurrence(shortest_s, [substring])
    return common_substrings

