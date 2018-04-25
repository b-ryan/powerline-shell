def dict_side_effect_fn(dict_):
    def func(*args):
        return dict_[args]
    return func
