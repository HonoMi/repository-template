def get_model_path(name: str) -> str:
    if name == 'model_01':
        return './models/model_01.pth'
    elif name == 'model_02':
        return './models/model_02.pth'
    else:
        raise ValueError(f"Unknown model: {name}")

