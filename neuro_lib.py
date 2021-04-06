import re

def replace(filePath, text = ',', subs = '.', flags=0):    # функция замены символов ',' на '.' в файле
    with open(filePath, "r+") as file:
        fileContents = file.read()
        textPattern = re.compile(re.escape(text), flags)
        fileContents = textPattern.sub(subs, fileContents)
        file.seek(0)
        file.truncate()
        file.write(fileContents)
        
#########################################################################################################################################################################
        
import numpy as np
import pandas as pd

def on_off_impulse(file): # функция, которая создает колонки с ON / OFF. В качестве параметра принимает имя файла

    import numpy as np
    import pandas as pd

    f = open(file, 'r')
    line = f.readline()
    line_buf = line
    flag = 0

    #pd.options.display.max_colwidth = 1000
    res = pd.DataFrame(columns = ['N','on_start_t','on_start_V','on_end_t','on_end_V','off_start_t','off_start_V','off_end_t','off_end_V'])

    on_start = np.array([]) # создание массива ON
    i_on_start = 1

    on_end = np.array([])
    i_on_end = 1

    off_start = np.array([]) # создание массива OFF
    i_off_start = 1

    off_end = np.array([])
    i_off_end = 0

    while (line):
        if (line == "\n"):
            if (flag == 0):
                line_buf = line_buf.replace('\n', "") # удаление символа \n
                a = line_buf.split("\t")  # разбиение по \t
                res.loc[i_off_end, 'off_end_t'] = float(a[0])/1000
                res.loc[i_off_end, 'off_end_V'] = float(a[1])
                res.loc[i_off_end, 'N'] = i_off_end
                #print ('off', i_off_end, a, "\n")
                i_off_end += 1

                line = f.readline()
                if (line):
                    line = line.replace('\n', "")
                    b = line.split("\t")
                    res.loc[i_on_start, 'on_start_t'] = float(b[0])/1000
                    res.loc[i_on_start, 'on_start_V'] = float(b[1])
                    res.loc[i_on_start, 'N'] = i_on_start
                    #print ('on', i_on_start, b, "\n")
                    i_on_start += 1
                else:
                    break

                flag = 1 # переназначение FLAG
            else:
                if (flag == 1):
                    line_buf = line_buf.replace('\n', "")
                    a = line_buf.split("\t")
                    res.loc[i_on_end, 'on_end_t'] = float(a[0])/1000
                    res.loc[i_on_end, 'on_end_V'] = float(a[1])
                    res.loc[i_on_end, 'N'] = i_on_end
                    #print ('on', i_on_end, a, "\n")
                    i_on_end += 1

                    line = f.readline()
                    if (line):
                        line = line.replace('\n', "")
                        b = line.split("\t")
                        res.loc[i_off_start, 'off_start_t'] = float(b[0])/1000
                        res.loc[i_off_start, 'off_start_V'] = float(b[1])
                        res.loc[i_off_start, 'N'] = i_off_start
                        #print ('off', i_off_start, b, "\n")
                        i_off_start += 1
                    else:
                        break

                    flag = 0

        line_buf = line
        line = f.readline()
    f.close()
    return (res)
 
#########################################################################################################################################################################