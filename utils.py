import math

"""
clipping 2d array around the given coordinates. when it over the length of array,
pad pad_value to them.
params: array center_x center_y height width

"""
def clip_array(array,center_x,center_y,width,height,pad_value=-1):
    start_x=center_x-width//2
    start_y=center_y-height//2
    end_x=center_x+width//2
    end_y=center_y+height//2
    if height%2==1:
        end_y+=1

    if width%2==1 :
        end_x+=1
    clipped_array=[]
    if start_y<0: # if start_y over the length
        start_padding=[[pad_value for _ in range(len(array[0]))] for __ in range(abs(start_y))]
        if end_y>len(array)-1:# if end_y over the length
            end_padding=[[pad_value for _ in range(len(array[0]))] for __ in range(end_y-len(array))]
            column_clipped=start_padding+array+end_padding
        else:

            column_clipped=start_padding+(array[0:end_y] if end_y!=0 else [array[end_y]])
    else:
        if end_y>len(array):# if end_y over the length
            end_padding=[[pad_value for _ in range(len(array[0]))] for __ in range(end_y-len(array))]
            column_clipped=array[start_y:]+end_padding
        else:
            column_clipped=array[start_y:end_y] if start_y!=end_y else [array[start_y]]
    for row in column_clipped:
        if start_x<0:
            start_padding=[pad_value for _ in range(abs(start_x))]
            if end_x>len(row)-1:
                end_padding=[pad_value for _ in range(end_x-len(row))]
                clipped_array.append(start_padding+row+end_padding)
            else:
                clipped_array.append(start_padding+(row[0:end_x]if end_x!=0 else [row[0]]))
        else:
            if end_x>len(row):
                end_padding=[pad_value for _ in range(end_x-len(row))]
                clipped_array.append(row[start_x:]+end_padding)
            else:
                clipped_array.append(row[start_x:end_x]if start_x!= end_x else [row[start_x]])

    return clipped_array

if __name__ == '__main__':
    test=[[i+k*30 for i in range(30)]for k in range(30)]
    for _ in test:
        print(["%02d"%__ for __ in _])
    res=clip_array(test,10,10,20,15)
    for _ in res:
        print(_)
