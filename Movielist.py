from bs4 import BeautifulSoup
import os,re,requests

movie_list = []

url = 'https://movies.yahoo.com.tw/chart.html'


resp = requests.get(url)
resp.encoding = 'utf-8'
soup = BeautifulSoup(resp.text,'lxml')

# parse colname 
rows = soup.find_all('div', class_='tr')
# get strings and convert into list
colname = list(rows.pop(0).stripped_strings) 

#parse rest content info
maximum_data_count=len(rows)

def view_raw():
    print (rows)

def get_all_movie():
    global movie_list    
    movie_list = []

    #print (rows)
    for row in rows:
        movie_dict = {}
        #ranks
        thisweek_rank=row.find_next('div',attrs={'class':'td'})
        updown=thisweek_rank.find_next('div')
        lastweek_rank=updown.find_next('div')

        #star
        star=''
        star_raw = row.find('h6',class_='count')    
        if star_raw:
            star=star_raw.string
        #print(star)

        #trailer
        trailer_url=''
        trailer_raw = row.find('div',class_='td icon_notice')
        if trailer_raw:
            trailer_raw = trailer_raw.find('a')
            if trailer_raw:
                trailer_url = trailer_raw.get('href','')

            #print (trailer_url)


        #movie_spec
        movie_link = movie_link=lastweek_rank.find_next('div')
        movie_url = movie_link.find('a').get('href',None)

        #parse movie_url
        resp = requests.get(movie_url)
        resp.encoding='utf-8'
        soup = BeautifulSoup(resp.text,'lxml')
        movie_specs = soup.find_all('div',class_='movie_intro_info_r')

        #movie_pic_url
        pic_specs = soup.find('div',class_="movie_intro_foto")
        pic_url = pic_specs.find('img').get('src',None)


        #movie_title
        for spec in movie_specs:
            chi_title = spec.find('h1')
            eng_title = spec.find('h3')

            #movie genre
            movie_type = []
            types = soup.find_all('div',class_='level_name')
            #print(len(types))
            for genre in types:
                genre = genre.find('a','gabtn')

                if genre:
                    genre = genre.string.strip()
                    #print(genre)
                    movie_type.append(genre)

            #date
            date_raw = spec.find_next('span')
            date_ = re.findall(r'上映日期：(.+)',date_raw.string)
            if date_!=[]:
                date = date_[0]
            else:
                date=''

            #time
            time_raw = date_raw.find_next('span')
            time_ = re.findall(r'片　　長：(.+)',time_raw.string)
            if time_!=[]:
                time=time_[0]
            else:
                time=''
            
            #company
            company_raw = time_raw.find_next('span')
            company_ = re.findall(r'發行公司：(.+)',company_raw.string)
            if company_!=[]:
                company=company_[0]
            else:
                company=''

            #imdb
            imdb_raw = company_raw.find_next('span')
            imdb_ = re.findall(r'IMDb分數：(.+)',imdb_raw.string)
            if imdb_!=[]:
                imdb=imdb_[0]
            else:
                imdb=''

            #director
            director_list = []
            
            director=''
            director_raw = soup.find('div',class_="movie_intro_list")
            if director_raw:
                director = director_raw.string

                if director:
                    director=director.strip()
                    #print(director)

            #actors
            actor_list = []
            actors_raw = director_raw.find_next('div',class_="movie_intro_list")
            if actors_raw:
                actors_item = actors_raw.find_all('a')

                for actor_item in actors_item:
                    if actor_item:
                        actor_link = actor_item.get('href','')
                        actor = actor_item.string
                        #print(actor_link,actor)
                        actor_attr = [actor,actor_link]
                        actor_list.append(actor_attr)

            #storyline
            plot=''
            story_raw = soup.find('div',class_='gray_infobox_inner')
            #print(story_raw)
            if story_raw:
                story = story_raw.find('span').string
                if story:
                    plot=story.strip()
                    #print (plot)


        movie_dict['thisweek_rank'] = thisweek_rank.string
        movie_dict['updown'] = updown.string
        movie_dict['lastweek_rank'] = lastweek_rank.string
        movie_dict['movie_url'] = movie_url
        movie_dict['chi_title'] = chi_title.string
        movie_dict['eng_title'] = eng_title.string
        movie_dict['pic_url'] = pic_url
        movie_dict['genre'] = movie_type
        movie_dict['release_date'] = date
        movie_dict['movie_time'] = time
        movie_dict['company'] = company
        movie_dict['imdb'] = imdb
        movie_dict['director'] = director
        movie_dict['actor_list']= actor_list
        movie_dict['plot'] = plot
        movie_dict['star'] = star
        movie_dict['trailer_url'] = trailer_url

        movie_list.append(movie_dict)


        #print ('{}\n{}\n\n'.format(chi_title.string,movie_dict))
    print ('已完成所有資料的建構!')
    return movie_list

def get_movie(index):
    global movie_list    
    movie_list = []

    #parse rest content info
    maximum_data_count=len(rows)

    try:
        index = int(index)
    except:
        index = 1

    #print ("電影排名：{}".format(index))
    if int(index) > maximum_data_count:
        return None

    else:
    #print (rows)
        row = rows[index-1]
        #print (row)


    #for row in rows:
        movie_dict = {}
        #ranks
        thisweek_rank=row.find_next('div',attrs={'class':'td'})
        updown=thisweek_rank.find_next('div')
        lastweek_rank=updown.find_next('div')

        #star
        star=''
        star_raw = row.find('h6',class_='count')    
        if star_raw:
            star=star_raw.string
        #print(star)

        #trailer
        trailer_url=''
        trailer_raw = row.find('div',class_='td icon_notice')
        if trailer_raw:
            trailer_raw = trailer_raw.find('a')
            if trailer_raw:
                trailer_url = trailer_raw.get('href','')

            #print (trailer_url)


        #movie_spec
        movie_link = movie_link=lastweek_rank.find_next('div')
        movie_url = movie_link.find('a').get('href',None)

        #parse movie_url
        resp = requests.get(movie_url)
        resp.encoding='utf-8'
        soup = BeautifulSoup(resp.text,'lxml')
        movie_specs = soup.find_all('div',class_='movie_intro_info_r')

        #movie_pic_url
        pic_specs = soup.find('div',class_="movie_intro_foto")
        pic_url = pic_specs.find('img').get('src',None)


        #movie_title
        for spec in movie_specs:
            chi_title = spec.find('h1')
            eng_title = spec.find('h3')

            #movie genre
            movie_type = []
            types = soup.find_all('div',class_='level_name')
            #print(len(types))
            for genre in types:
                genre = genre.find('a','gabtn')

                if genre:
                    genre = genre.string.strip()
                    #print(genre)
                    movie_type.append(genre)

            #date
            date_raw = spec.find_next('span')
            date_ = re.findall(r'上映日期：(.+)',date_raw.string)
            if date_!=[]:
                date = date_[0]
            else:
                date=''

            #time
            time_raw = date_raw.find_next('span')
            time_ = re.findall(r'片　　長：(.+)',time_raw.string)
            if time_!=[]:
                time=time_[0]
            else:
                time=''
            
            #company
            company_raw = time_raw.find_next('span')
            company_ = re.findall(r'發行公司：(.+)',company_raw.string)
            if company_!=[]:
                company=company_[0]
            else:
                company=''

            #imdb
            imdb_raw = company_raw.find_next('span')
            imdb_ = re.findall(r'IMDb分數：(.+)',imdb_raw.string)
            if imdb_!=[]:
                imdb=imdb_[0]
            else:
                imdb=''

            #director
            director_list = []
            
            director_raw = soup.find('div',class_="movie_intro_list")
            #format 1 (without url)
            if director_raw:                
                director = director_raw.string

                if director:                    
                    #director=director.strip()
                    #director_list.append([director,''])

                    directors = director.split('、')
                    for i in directors:
                        if i.strip()!='':   

                            tem_list = []                         
                            for j in director_list:
                                tem_list.append(j[0])
                                
                            if not i.strip() in tem_list:
                                director_list.append([i.strip(),''])
                            
                    #print(director_list)            

            #format 2 (with url)
            director_raw_2 = director_raw.find('a')
            if director_raw_2:
                director_2 = director_raw_2.string
                director_2_url = director_raw_2.get('href')

                #print (director_2_url)

                if director_2:
                    if director_2_url:
                        director_list.append([director_2,director_2_url])

                    else:
                        director_list.append([director_2,''])



            #actors
            actor_list = []
            actors_raw = director_raw.find_next('div',class_="movie_intro_list")
            if actors_raw:
                #format 1 (without url)
                if actors_raw.string:
                    actors = actors_raw.string
                    #print (actors)

                    if re.findall(r'\w+',actors)!=[]:
                        #print (re.findall(r'\w+',actors))

                        for i in re.findall(r'\w+',actors):
                            #actor_list.append([i,''])
                            pass
                    #print(actors)


                #format 2 (with url)
                actors_item = actors_raw.find_all('a')

                for actor_item in actors_item:
                    if actor_item:
                        actor_link = actor_item.get('href','')

                        tem_list = [] #過濾重複人名
                        for j in range(len(actor_list)):
                            tem_list.append(actor_list[j][0])

                        if not actor_item.string in tem_list:
                            actor = actor_item.string
                            #print(actor_link,actor)
                            actor_attr = [actor,actor_link]
                            actor_list.append(actor_attr)

                #format 3 (without url)
                if actors_raw.contents:
                    #print(actors_raw.contents)
                    for i in actors_raw.contents:
                        if i.string:
                            #print(i.string)
                            #print (re.findall(r'[\w\(\)-]+\s*[\w\(\)-]+',i.string))
                            #print (i.string)
                            raw_list = i.string.split('、')
                            
                            for i in range(len(raw_list)):
                                raw_list[i] = raw_list[i].strip()
                                #print (i,raw_list[i])


                            #print (actor_list)
                            tem_list = [] #過濾重複人名
                            for j in range(len(actor_list)):
                                tem_list.append(actor_list[j][0])
                            #print (tem_list)

                            #print (len(raw_list))
                            for i in raw_list:
                                if not i in tem_list and i.strip()!='':
                                    actor_list.append([i,''])                         



            #storyline
            plot=''
            story_raw = soup.find('div',class_='gray_infobox_inner')
            #print(story_raw)

            #format 1
            if story_raw:
                story = story_raw.find('span').string
                if story:
                    plot=story.strip()
                    #print (plot)

            #format 2
            if plot=='':
                #print (story_raw.find('span').get('title2'))
                if story_raw.find('span').contents:
                    stories = story_raw.find('span').contents

                    story = ''
                    for i in stories:
                        if i.string:
                            #print (i)
                            story += i.string.strip()

                    plot = story
                    #print (story)


        movie_dict['thisweek_rank'] = thisweek_rank.string
        movie_dict['updown'] = updown.string
        movie_dict['lastweek_rank'] = lastweek_rank.string
        movie_dict['movie_url'] = movie_url
        movie_dict['chi_title'] = chi_title.string
        movie_dict['eng_title'] = eng_title.string
        movie_dict['pic_url'] = pic_url
        movie_dict['genre'] = movie_type
        movie_dict['release_date'] = date
        movie_dict['movie_time'] = time
        movie_dict['company'] = company
        movie_dict['imdb'] = imdb
        movie_dict['director'] = director
        movie_dict['director_list'] = director_list
        movie_dict['actor_list']= actor_list
        movie_dict['plot'] = plot
        movie_dict['star'] = star
        movie_dict['trailer_url'] = trailer_url

        movie_list.append(movie_dict)

        #print ("電影名稱：{}\n".format(movie_dict['chi_title']))
        #print ("導演：{}\n".format(movie_dict['director']))

        #print ('{}\n{}\n\n'.format(chi_title.string,movie_dict))
        #print ('已完成所有資料的建構!')
        return movie_dict

if __name__ =='__main__':
    #view_raw()
    #print(get_all_movie())
    #print(get_movie(7)['director_list'])

    #for i in range(20):
    print (get_movie(1))
