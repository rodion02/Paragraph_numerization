import re
from roman_numeral import *
import logging

roman_numbers = 'IVXLCDM'

def parse(text, txt_path, log_path='myapp.log'):
   logging.basicConfig(filename=log_path, level=logging.DEBUG, 
      format=f'%(asctime)s %(levelname)s module: %(name)s line num: %(lineno)s func: %(funcName)s %(message)s \nText path: {txt_path}\n')
   logger=logging.getLogger(__name__)

   js = []
   lst = []
   for elem in text.keys():
      if elem == 'Paragraphs':
         js.append(text[elem])
         lst.append([])
      elif elem == 'Tables':
         for table in text[elem]:
            buf = []
            for cell in table['Rows']:
               buf.append(cell['Cells'][0]["Paragraphs"][0])
            js.append(buf)
            lst.append([])
   
   sign, counter, data_type = 1, 0, None
   first_elements = {
      'number': {'.': '1', ')': '1', '()': '1', 'таблица': '1', 'рисунок': '1', 'рис': '1', 'схема': '1', 'приложение': '1', 'NaN': '1'}, 
      'ru_up_letter': {'.': 'А', ')': 'А', '()': 'А', 'таблица': 'А', 'рисунок': 'А', 'рис': 'А', 'приложение': 'А', 'схема': 'А'}, 
      'en_up_letter': {'.': 'A', ')': 'A', '()': 'A', 'таблица': 'A', 'рисунок': 'A', 'рис': 'A', 'приложение': 'A', 'схема': 'A'},
      'ru_low_letter': {'.': 'а', ')': 'а', '()': 'а', 'таблица': 'а', 'рисунок': 'а', 'рис': 'а', 'приложение': 'а', 'схема': 'а'},
      'en_low_letter': {'.': 'a', ')': 'a', '()': 'a', 'таблица': 'a', 'рисунок': 'a', 'рис': 'a', 'приложение': 'a', 'схема': 'a'},
      'roman': {'.': 'I', ')': 'I', '()': 'I', 'таблица': 'I', 'рисунок': 'I', 'рис': 'I', 'схема': 'I', 'приложение': 'I'},
   }
   n = 0
   for entity in js:
      for string in entity:
         if string['Index'] == 20:
            print()
         txts = string["Text"]
         if string["IsToc"] and not string["Numbering"]:
            if not re.search(re.compile(r"(^|(?<=^\s)\s*)[Тт]аблица [№]?\d+", re.ASCII), txt):
               counter += len(txt)+1
               continue
         if string.get('Vanish'):
            if string["Vanish"]:
               counter += len(txt)+1
               continue
         if string["Numbering"]:
            txts = string["Numbering"] + ' ' + txts
         try:
            counter = len(txts.split('\n')[0])+1
            txts = txts.split('\n')[1:]
            for txt in txts:
               begin = True
               f_elem = True
               while txt and sign:
                  txt = re.sub(r'\u00A0', ' ', txt)
                  while not (txt[0].isdigit() or txt[0].isalpha()):
                     txt = txt[1:]
                     counter+=1
                     if txt == '':
                        break
                  if txt == '':
                     counter+=1
                     break
                  list_findings = [[re.search(re.compile(r"((?<=\s)|(?<=^))(((\d+[.])+\d+)|((([a-zA-Zа-яА-Я])|(\d)+|([IVXLCDM])+)[.]))", re.ASCII), txt), ".", None, None],
                              [re.search(re.compile(r"((?<=\s)|(?<=^))(((\d+[.])+\d+)|([a-zA-Zа-яА-Я])|(\d)+|([IVXLCDM])+)[)]((?=\s)|(?=\w))", re.ASCII), txt), ")", None, None],
                              [re.search(re.compile(r"(^|(?<=^\s)\s*)[Тт]аблица [№]?\d+([.]\d+)*", re.ASCII), txt) if begin else None, "таблица", None, None],
                              [re.search(re.compile(r"(^|(?<=^\s)\s*)[Рр]исунок [№]?\d+([.]\d+)*", re.ASCII), txt) if begin else None, "рисунок", None, None],
                              [re.search(re.compile(r"(^|(?<=^\s)\s*)[Рр]ис[.]? [№]?\d+([.]\d+)*", re.ASCII), txt) if begin else None, "рис", None, None],
                              [re.search(re.compile(r"(^|(?<=^\s)\s*)[Сс]хема [№]?\d+([.]\d+)*", re.ASCII), txt) if begin else None, "схема", None, None],
                              [re.search(re.compile(r"((?<=\s)|(?<=^))[(]((\d+[.]?)+|([a-zA-Zа-яА-Я])|(\d)+|([IVXLCDM])+)[)]((?=\s)|(?=\w))", re.ASCII), txt), "()", None, None],
                              [re.search(re.compile(r"(^\d+)|((?<=^\s)\s*\d+)", re.ASCII), txt) if begin else None, "NaN", None, None],
                              [re.search(re.compile(r"((?<=\s)|(?<=^))[A-Za-zА-Яа-я][.](((\d+[.])+\d+)|(\d+))[.]*", re.ASCII), txt), ".", None, None]]

                  begin = False 
                  list_findings = list(filter(lambda x: x[0] is not None, list_findings))
                  if list_findings:
                     list_findings = sorted(list(map(lambda x: [x[0], x[1], x[0].span()[0], x[0].span()[1]], list_findings)), key = lambda x: x[2])         
                     posx = list_findings[0][2]
                     posy = list_findings[0][3]
                     list_findings = sorted(list(filter(lambda x: x[2] == posx, list_findings)), key = lambda x: x[3], reverse=True)
                     sign = list_findings[0][1]
                     pos = list_findings[0][3]

                     posx = list_findings[0][2]
                     posy = list_findings[0][3]
                  else:
                     counter+=len(txt)+1
                     break

                  name = list_findings[0][0].group()
                  while re.search('\s', name[0]):
                     name = name[1:]
                  while re.search('\s', name[-1]):
                     name = name[:-1]
                  if re.search(f'{name}[.]', txt) and name[0].isdigit():
                     name+='.'

                  paragraph = list_findings[0][0].group()
                  if re.search("\D.\d", paragraph):
                     paragraph = re.sub(re.compile(r"\D[.]", re.ASCII), "", paragraph)
                  paragraph = re.sub(r"^\s\s*", "", paragraph)
                  if sign == "()":
                     paragraph = paragraph[1:len(paragraph)-1]
                  elif sign == ")":
                     paragraph = paragraph[:-1]
                  elif paragraph[-1] == "." and paragraph.count(".") == 1:
                     paragraph = paragraph[:-1]
                  elif sign != ".":
                     paragraph = paragraph.split(" ")[-1].replace("№", "")
                  elif sign == "":
                     paragraph = re.sub("\t", "", paragraph)
                  
                  if paragraph == "п" and sign == ".":
                     buf = re.search("(\d+[.]?)+", txt[pos:])
                     if buf:
                        if buf.span()[0]-pos < 3:
                           txt = txt[pos+buf.span()[1]:]
                           counter+=(pos+buf.span()[1])
                           continue

                  #& Обработчик исключений для чисел
                  error = False
                  try:
                     if paragraph[0] == '0':
                        error = True
                     if paragraph[0].isdigit():
                        if '.' in paragraph:
                              for i in paragraph.split('.'):
                                 if len(i) >= 3:
                                    error = True
                                    break
                                 if i:
                                    if i[0] == '0' and len(i) > 1:
                                       error = True
                                       break
                     
                        if txt[pos-1] == '.' or txt[pos-1] == ')':
                           if not re.search("\s|[A-Za-zА-Яа-я]", txt[pos]):   
                              error = True

                        if txt[pos] == ' ':
                           if not re.search("\w|\s", txt[pos]):
                              error = True
                  except:
                        pass
                  
                  if error:
                     txt = txt[pos:]
                     counter+=(pos)
                     continue

                  cut = txt[:pos][::-1]
                  if sign == ')' and cut.count('(') == cut.count(')'):
                     txt = txt[pos:]
                     counter+=(pos)
                     continue

                  p=None
                  if sign == ')':
                     p = '(?<=[^А-Яа-яA-Za-z0-9])|^' + paragraph + '[)]'
                  elif sign == '()':
                     p = '[(]' + paragraph + '[)]'
                  elif sign == '.':
                     p = paragraph.replace('.', '[.]')
                  else:
                     p = txt[posx:pos]

                  if sign in '.()':
                     ##-----------------Отлавливаю тире справа-------------------
                     tire = re.search('[-—–]', txt[re.search(p, txt).span()[1]:])
                     if tire:
                        if tire.span()[0] < 2:
                           txt = txt[pos:]
                           counter+=(pos)
                           continue
                     ##-----------------Отлавливаю тире слева-------------------
                     tire = re.search('[-—–]', txt[:re.search(p, txt).span()[0]])
                     if tire:
                        if tire.span()[0] < 2:
                           txt = txt[pos:]
                           counter+=(pos)
                           continue
                     ##-----------------------------------------------------------

                  pos1 = re.search(p, txt).span()[0]

                  if pos1 >= 3 and lst and not f_elem:
                     pos0 = re.findall('[\w]', txt[:pos1])
                     pos0 = len(txt[:pos1])-txt[:pos1][::-1].index(pos0[-1]) if pos0 else 0 
                     if not re.search('([\t\r]+)|([.:!?;]\W+)', txt[pos0:pos1]):
                        try:
                           if ord(paragraph) - ord(lst[-1]) <= 3:
                              pass
                        except:
                           txt = txt[pos:]
                           counter+=(pos)
                           continue  
                  


                  pos0 = list(re.finditer('(п[.]|пункт|параграф|р[.]|раздел)', txt[:pos1]))
                  if pos0:
                     if pos1 - pos0[-1].span()[1] < 5:
                        txt = txt[pos:]
                        counter+=(pos)
                        continue

                  if f_elem:
                     if re.search("\w", txt[0:list_findings[0][2]]):
                        counter+=len(txt)+1
                        break
                     f_elem = False   
                     
                  if all(i in roman_numbers for i in list(paragraph)):
                     data_type = 'roman'
                     elem = first_elements[data_type][sign]

                     if Roman2Num(paragraph) - Roman2Num(elem) > 7:
                        txt = txt[pos:]
                        counter+=(pos)
                        continue 
                     else:
                        first_elements[data_type][sign] = paragraph
                  elif paragraph.isalpha():
                     if 1040 <= ord(paragraph) <= 1103:
                        data_type = 'ru_up_letter' if paragraph.isupper() else 'ru_low_letter'
                     else:
                        data_type = 'en_up_letter' if paragraph.isupper() else 'en_low_letter'

                     elem = first_elements[data_type][sign]
                     if ord(paragraph) - ord(elem) > 5:
                        txt = txt[pos:]
                        counter+=(pos)
                        continue 
                     else:
                        first_elements[data_type][sign] = paragraph
                  else:
                     data_type = 'numbers' if (paragraph.split('.')[-1].isdigit() and len(paragraph.split('.')) > 1) or (len(paragraph.split('.')) > 2 and paragraph.split('.')[-1]=="") else 'number'
                     if data_type == "number":
                        elem = first_elements[data_type][sign]
                        if int(paragraph) - int(elem) > 7:
                           txt = txt[pos:]
                           counter+=(pos)
                           continue 
                        else:
                           first_elements[data_type][sign] = paragraph

                  txt = txt[pos:]
                  # res_pos = counter+posx
                  paragraph = paragraph[:-1] if paragraph[-1] == '.' else paragraph
                  lst[n].append((paragraph, sign, string["Index"], data_type, (counter+posx, counter+posy), name))
                  counter+=(pos)
                  if txt == "":
                     counter+=1
         except Exception as err:
            logger.error(err)
      n+=1

   return lst