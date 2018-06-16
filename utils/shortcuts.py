def compress_week_arrays(data):
    assert type(data) == list
    data.sort()
    ret = []
    pre = -1
    cur = -1
    for num in data:
        if cur + 1 == num:
            cur = num
        else:
            if pre != -1:
                if pre == cur:
                    ret.append(str(pre))
                else:
                    ret.append('{}-{}'.format(pre, cur))
            pre = num
            cur = num
    if pre != -1:
        if pre == cur:
            ret.append(str(pre))
        else:
            ret.append('{}-{}'.format(pre, cur))
    return ','.join(ret)
