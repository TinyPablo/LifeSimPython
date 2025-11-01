def condition(x, y, w, h) -> bool:
    return ((x < w // 5 and y < h // 5) or (x > w - w // 5 and y < h // 5) or 
            (x < w // 5 and y > h - h // 5) or (x > w - w // 5 and y > h - h // 5))