def solution(hallway):
    if not (str(hallway).__contains__('-') or 
        str(hallway).__contains__('<') or 
        str(hallway).__contains__('>')):
        return None
    
    short_hall = ''

    for char in hallway:
        if char == '<' or char == '>':
            short_hall += char
    
    short_hall = short_hall[short_hall.find('>'):len(short_hall)]
    short_hall = short_hall[0:short_hall.rfind('<') + 1]

    saluttes = 0
    right_workers = []

    for index in range(0, len(short_hall)):
        if short_hall[index] == '>':
            right_workers.append(index)
        
    for index in range(len(right_workers)):
        saluttes += (2 * (len(short_hall[right_workers[index]:len(short_hall)]) - (len(right_workers) - index)))

    return saluttes
