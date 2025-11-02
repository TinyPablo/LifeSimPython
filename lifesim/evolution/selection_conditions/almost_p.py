def condition(x, y, w, h):  
    upper_left_square = (x < w // 3) and (y < h // 3)
    left_edge = x < w // 12
    
    # the "almost p" shape is intentionally asymmetrical — useful for debugging grid rendering 
    # if x and y are swapped or the grid is flipped/transposed, the difference will be visible
    return upper_left_square or left_edge