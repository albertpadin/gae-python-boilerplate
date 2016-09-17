def uniquify(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result


def string_to_list(raw_string, separator=','):
    raw_string = raw_string.strip()
    raw_list = raw_string.split(separator)
    final_list = []
    for raw_list_item in raw_list:
        final_list.append(raw_list_item.strip())
    return final_list
