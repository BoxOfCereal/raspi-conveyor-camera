def destroy_kids(widgets):
    for widget in widgets:
        for e in widget.children:
            print(e)
            e.destroy()

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def encode_strings(string):
    """None general helper to help serialize the correct types"""
    if (string.isdigit()):
        return (int(string))
    elif (isfloat(string)):
        return float(string)
    else:
        return string


#  {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
def serialize(lst):
    dic = {lst[i]: encode_strings(lst[i + 1]) for i in range(0, len(lst), 2)}
    return dic
